import os
import tempfile
from pathlib import Path
from typing import Dict, List, Optional

import numpy as np
import streamlit as st
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain.tools import tool
from langchain_community.document_loaders import (
	CSVLoader,
	Docx2txtLoader,
	PyPDFLoader,
	TextLoader,
)
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.utilities import GoogleSearchAPIWrapper
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_text_splitters import RecursiveCharacterTextSplitter


st.set_page_config(page_title="Portfolio AI Agent", layout="centered")
st.title("Portfolio AI Assistant")
st.caption("Ask about Subramanya's work, upload files for analysis, or request current events.")


SUPPORTED_EXTENSIONS = {".pdf", ".txt", ".docx", ".csv"}


def _load_document(path: Path):
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


@st.cache_resource
def init_portfolio_retriever(static_dir: str):
	docs = []
	root = Path(static_dir)

	if root.exists():
		for file_path in root.rglob("*"):
			if file_path.is_file() and file_path.suffix.lower() in SUPPORTED_EXTENSIONS:
				try:
					docs.extend(_load_document(file_path))
				except Exception:
					# Skip any file that cannot be parsed without failing app startup.
					continue

	if not docs:
		return None

	splitter = RecursiveCharacterTextSplitter(chunk_size=700, chunk_overlap=120)
	chunks = splitter.split_documents(docs)
	embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
	vectors = embeddings.embed_documents([doc.page_content for doc in chunks])
	matrix = np.array(vectors, dtype="float32")
	norms = np.linalg.norm(matrix, axis=1, keepdims=True)
	norms[norms == 0] = 1.0
	matrix = matrix / norms
	return {"docs": chunks, "embeddings": embeddings, "matrix": matrix}


def retrieve_portfolio_docs(index, query: str, k: int = 4):
	if not index:
		return []

	query_vector = np.array(index["embeddings"].embed_query(query), dtype="float32")
	q_norm = np.linalg.norm(query_vector)
	if q_norm == 0:
		return []

	query_vector = query_vector / q_norm
	scores = index["matrix"] @ query_vector
	if scores.size == 0:
		return []

	top_idx = np.argsort(scores)[-k:][::-1]
	return [index["docs"][int(i)] for i in top_idx if scores[int(i)] > 0]


GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY", "").strip()
GOOGLE_CSE_ID = os.environ.get("GOOGLE_CSE_ID", "").strip()

if not GOOGLE_API_KEY:
	st.error("Missing GOOGLE_API_KEY environment variable.")
	st.stop()

portfolio_retriever = init_portfolio_retriever("static")


@tool
def query_portfolio_knowledge_base(query: str) -> str:
	"""Use this when the question is about Subramanya's portfolio, resume, skills, experience, education, or projects."""
	if not portfolio_retriever:
		return "No local portfolio data is available yet."
	docs = retrieve_portfolio_docs(portfolio_retriever, query, k=4)
	if not docs:
		return "I did not find relevant details in the local portfolio files."
	return "\n\n".join(doc.page_content for doc in docs)


@tool
def search_the_live_web(query: str) -> str:
	"""Use this when the user asks for current affairs, latest news, or real-time information from the web."""
	if not GOOGLE_CSE_ID:
		return "Live web search is not configured. Please set GOOGLE_CSE_ID on the server."
	try:
		search = GoogleSearchAPIWrapper(google_api_key=GOOGLE_API_KEY, google_cse_id=GOOGLE_CSE_ID)
		return search.run(query)
	except Exception:
		return "Web search failed at runtime. Please try again shortly."


tools = [query_portfolio_knowledge_base, search_the_live_web]

llm = ChatGoogleGenerativeAI(
	model="gemini-2.0-flash",
	google_api_key=GOOGLE_API_KEY,
	temperature=0.2,
)

prompt = ChatPromptTemplate.from_messages(
	[
		(
			"system",
			"You are an assistant embedded in Subramanya Sharma's portfolio. "
			"Be professional, concise, and accurate. "
			"Use tools for portfolio-specific facts and current events. "
			"If the answer is uncertain, say so clearly.",
		),
		MessagesPlaceholder(variable_name="chat_history"),
		("human", "{input}"),
		MessagesPlaceholder(variable_name="agent_scratchpad"),
	]
)

agent = create_tool_calling_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=False)


def _extract_uploaded_context(uploaded_file) -> str:
	suffix = Path(uploaded_file.name).suffix.lower()
	if suffix not in SUPPORTED_EXTENSIONS:
		return ""

	temp_path = None
	try:
		with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_file:
			temp_file.write(uploaded_file.getbuffer())
			temp_path = Path(temp_file.name)

		chunks = _load_document(temp_path)
		return "\n\n".join(chunk.page_content for chunk in chunks)
	except Exception:
		return ""
	finally:
		if temp_path and temp_path.exists():
			temp_path.unlink(missing_ok=True)


uploaded_file = st.file_uploader(
	"Upload a file to analyze (PDF, TXT, DOCX, CSV)",
	type=["pdf", "txt", "docx", "csv"],
)

uploaded_context = ""
if uploaded_file:
	uploaded_context = _extract_uploaded_context(uploaded_file)
	if uploaded_context:
		st.success(f"Processed {uploaded_file.name} successfully.")
	else:
		st.warning("File uploaded, but text extraction returned no readable content.")

if "messages" not in st.session_state:
	st.session_state.messages = []
if "history_log" not in st.session_state:
	st.session_state.history_log = []

for message in st.session_state.messages:
	with st.chat_message(message["role"]):
		st.write(message["content"])

if user_input := st.chat_input("Ask about portfolio work, world events, or your uploaded file"):
	st.session_state.messages.append({"role": "user", "content": user_input})
	with st.chat_message("user"):
		st.write(user_input)

	full_query = user_input
	if uploaded_context:
		full_query = (
			"User uploaded file content:\n"
			f"{uploaded_context}\n\n"
			f"User question: {user_input}"
		)

	with st.chat_message("assistant"):
		with st.spinner("Thinking..."):
			response = agent_executor.invoke(
				{
					"input": full_query,
					"chat_history": st.session_state.history_log,
				}
			)
			output = response.get("output", "I could not generate a response.")
			st.write(output)

	st.session_state.messages.append({"role": "assistant", "content": output})
	st.session_state.history_log.append(HumanMessage(content=user_input))
	st.session_state.history_log.append(AIMessage(content=output))
