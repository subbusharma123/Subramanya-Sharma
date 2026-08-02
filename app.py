from pathlib import Path
import re
import threading

from flask import Flask, jsonify, render_template, request, send_from_directory, redirect, url_for
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

SUPPORTED_EXTENSIONS = {".pdf", ".txt", ".docx", ".csv"}
_agent_executor = None
_agent_lock = threading.Lock()


def _load_document(path: Path):
    from langchain_community.document_loaders import CSVLoader, Docx2txtLoader, PyPDFLoader, TextLoader

    ext = path.suffix.lower()
    if ext == ".pdf":
        return PyPDFLoader(str(path)).load()
    if ext == ".txt":
        return TextLoader(str(path), encoding="utf-8").load()
    if ext == ".docx":
        return Docx2txtLoader(str(path)).load()
    if ext == ".csv":
        return CSVLoader(str(path)).load()
    return []


def _build_portfolio_retriever(static_dir: str = "static"):
    from langchain_text_splitters import RecursiveCharacterTextSplitter

    root = Path(static_dir)
    if not root.exists():
        return None

    docs = []
    for file_path in root.rglob("*"):
        if file_path.is_file() and file_path.suffix.lower() in SUPPORTED_EXTENSIONS:
            try:
                docs.extend(_load_document(file_path))
            except Exception:
                continue

    if not docs:
        return None

    splitter = RecursiveCharacterTextSplitter(chunk_size=700, chunk_overlap=120)
    chunks = splitter.split_documents(docs)
    tokenized = [_tokenize(doc.page_content) for doc in chunks]
    return {"docs": chunks, "tokens": tokenized}


def _retrieve_portfolio_docs(index, query: str, k: int = 4):
    if not index:
        return []

    query_tokens = _tokenize(query)
    if not query_tokens:
        return []

    scored = []
    for i, doc_tokens in enumerate(index["tokens"]):
        if not doc_tokens:
            continue
        overlap = len(query_tokens & doc_tokens)
        if overlap == 0:
            continue
        score = overlap / len(query_tokens)
        scored.append((score, i))

    if not scored:
        return []

    scored.sort(reverse=True)
    top_idx = [i for _, i in scored[:k]]
    return [index["docs"][i] for i in top_idx]


def _tokenize(text: str):
    return set(re.findall(r"[a-z0-9]+", (text or "").lower()))


def _build_agent_executor():
    from langchain.agents import AgentExecutor, create_tool_calling_agent
    from langchain.tools import tool
    from langchain_community.utilities import GoogleSearchAPIWrapper
    from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
    from langchain_google_genai import ChatGoogleGenerativeAI

    google_api_key = os.environ.get("GOOGLE_API_KEY", "").strip()
    google_cse_id = os.environ.get("GOOGLE_CSE_ID", "").strip()
    if not google_api_key:
        raise RuntimeError("GOOGLE_API_KEY is missing")

    retriever = _build_portfolio_retriever()

    @tool
    def query_portfolio_knowledge_base(query: str) -> str:
        """Use for questions about Subramanya's profile, resume, projects, skills, education, or achievements."""
        if not retriever:
            return "No local portfolio data is available right now."
        docs = _retrieve_portfolio_docs(retriever, query, k=4)
        if not docs:
            return "No relevant portfolio context found for that question."
        return "\n\n".join(doc.page_content for doc in docs)

    @tool
    def search_the_live_web(query: str) -> str:
        """Use for current affairs, live news, or real-time facts from the web."""
        if not google_cse_id:
            return "Live web search is not configured. Set GOOGLE_CSE_ID in environment variables."
        try:
            search = GoogleSearchAPIWrapper(google_api_key=google_api_key, google_cse_id=google_cse_id)
            return search.run(query)
        except Exception:
            return "Web search failed at runtime. Try again in a moment."

    tools = [query_portfolio_knowledge_base, search_the_live_web]
    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", google_api_key=google_api_key, temperature=0.2)
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are an assistant embedded in Subramanya Sharma's portfolio website. "
                "Be concise, professional, and factual. Use tools for portfolio facts and current events.",
            ),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ]
    )
    agent = create_tool_calling_agent(llm, tools, prompt)
    return AgentExecutor(agent=agent, tools=tools, verbose=False)


def _get_agent_executor():
    global _agent_executor
    if _agent_executor is None:
        with _agent_lock:
            if _agent_executor is None:
                _agent_executor = _build_agent_executor()
    return _agent_executor


@app.context_processor
def inject_ai_chat_url():
    ai_chat_url = os.environ.get("AI_CHAT_URL", "").strip()
    if ai_chat_url and "embed=true" not in ai_chat_url:
        separator = "&" if "?" in ai_chat_url else "?"
        ai_chat_url = f"{ai_chat_url}{separator}embed=true"
    return {
        "ai_chat_url": ai_chat_url,
        "use_native_ai_chat": os.environ.get("USE_NATIVE_AI_CHAT", "1") == "1",
    }

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/portfolio')
def portfolio():
    return render_template('portfolio.html')

@app.route('/experience')
def experience():
    return render_template('experience.html')

@app.route('/skills')
def skills():
    return render_template('skills.html')

@app.route('/certifications')
def certifications():
    return render_template('certifications.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/resume-view')
def resume_view():
    docs_dir = os.path.join(app.static_folder, 'docs')
    for fname in ['Subramanya_Sharma_B_G_Resume.pdf', 'SubramanyaResume.pdf']:
        if os.path.exists(os.path.join(docs_dir, fname)):
            return send_from_directory(docs_dir, fname)
    return redirect(url_for('about'))


@app.route('/api/ai-chat', methods=['POST'])
def ai_chat():
    payload = request.get_json(silent=True) or {}
    user_input = str(payload.get('message', '')).strip()
    history = payload.get('history', [])

    if not user_input:
        return jsonify({"error": "message is required"}), 400

    try:
        from langchain_core.messages import AIMessage, HumanMessage

        chat_history = []
        for item in history:
            role = str(item.get('role', '')).lower()
            content = str(item.get('content', '')).strip()
            if not content:
                continue
            if role == 'user':
                chat_history.append(HumanMessage(content=content))
            elif role == 'assistant':
                chat_history.append(AIMessage(content=content))

        executor = _get_agent_executor()
        result = executor.invoke({"input": user_input, "chat_history": chat_history})
        return jsonify({"reply": result.get("output", "I could not generate a response.")})
    except ModuleNotFoundError:
        return jsonify({"error": "Missing AI dependencies. Install requirements.txt and retry."}), 503
    except RuntimeError as exc:
        return jsonify({"error": str(exc)}), 503
    except Exception as exc:
        app.logger.exception("AI chat request failed")
        body = {"error": "AI service failed unexpectedly. Please try again."}
        if app.debug:
            body["detail"] = str(exc)
        return jsonify(body), 500

if __name__ == '__main__':
    app.run(debug=True)
