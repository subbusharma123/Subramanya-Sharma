from jinja2 import Template
import os

# Full resume data from your updated PDF
resume_data = {
    'name': 'Subramanya Sharma B G',
    'title': 'Data Engineer | Analyst | Problem Solver',
    'contact': {
        'email': 'subramanyasharma987@gmail.com',
        'phone': '+919901526720',
        'linkedin': 'linkedin.com/in/subramanya-sharma-b-g',
        'location': 'Bengaluru, India'
    },
    'highlights': {
        'posts': [
            {'title': 'Shared Analytical Dashboards Project', 'date': 'Oct 2024', 'desc': 'Posted about developing Python-based dashboards with Elasticsearch, Kibana, and SQL for executive insights.'},
            {'title': 'Kyndryl AIOps Team Update', 'date': 'Sep 2024', 'desc': 'Shared leadership in process improvements and ticket closure for Data Team – TnI (AIOps).'}
        ],
        'certs': [
            {'title': 'AWS Certified Developer - Associate', 'issuer': 'Amazon Web Services', 'issue_date': 'Aug 2024', 'expire_date': 'Aug 2027'},
            {'title': 'SQL for Data Analysis', 'issuer': 'LinkedIn Learning', 'issue_date': 'Jul 2024', 'expire_date': 'None'}
        ]
    },
    'experience': [
        {'company': 'KYND RYL SOLUTIONS | DATA ENGINEER (FULL-TIME)', 'period': 'Sept 2023 – Present | Bengaluru, India', 'desc': 'Analyzed large datasets with Elastic, Kibana, and SQL, delivering insights that enhanced customer deliverables and informed strategy.'},
        {'desc': 'Designed intuitive Kibana dashboards to present clear, actionable data visualizations, enabling stakeholders to drive efficient and informed business strategies.'},
        {'desc': 'Ensured data accuracy and quality through rigorous validation, ETL processes, SQL scripting in databases like Elasticsearch, reducing processing times and enhancing operational efficiency for client deliverables.'},
        {'desc': 'Collaborated with support teams using ServiceNow (SNOW) for ticket tracking and incident resolution, escalating over 150 technical support issues related to production and PSE environments, while integrating Logstash for streamlined data pipelines.'},
        {'company': 'AIRBAY LOGISTIQUE | INTERN (PART-TIME)', 'period': 'Aug 2022 – Sep 2022 | Bengaluru, India', 'desc': 'Applied knowledge of Incoterms (FOB, EXW) to streamline logistics processes, ensuring accurate and efficient coordination for air export shipments.'},
        {'desc': 'Supported sales targeting Pharma, Automotive, and Aerospace industries, boosting client acquisition.'},
        {'desc': 'Streamlined operations by assisting with online bookings, airway bill preparation, and airline coordination.'},
        {'desc': 'Prepared accurate documentation for air exports, ensuring compliance and smooth customs processes.'}
    ],
    'projects': [
        {'title': 'ANALYTICAL DASHBOARDS | DEVELOPED AND OPTIMIZED ANALYTICAL DASHBOARDS TO DELIVER STRATEGIC INSIGHTS FOR EXECUTIVE DECISION-MAKING', 'period': 'Nov 2023 – Present | Bengaluru, India', 'desc': 'Built and maintained Python-based dashboards (POS, Inventory, Global Resiliency, CSI) using Elasticsearch, Kibana, and SQL for data modeling, equipping executives with precise, actionable visualizations in agile sprints.'},
        {'desc': 'Enhanced multiple dashboards with Python collation scripts, ETL integrations, enabling accurate reporting and control functions for strategic planning and production support.'},
        {'title': 'SERVICE MANAGEMENT | SPEARHEADED ISSUE RESOLUTION, ENHANCING CUSTOMER SATISFACTION AND OPERATIONAL EFFICIENCY', 'period': 'Sep 2023 – Present | Bengaluru, India', 'desc': 'Resolved 150+ ServiceNow (SNOW) incident/RITM tickets, fixing data visualization/control issues for reliable production support and customer deliverables.'},
        {'desc': 'Led account onboarding/offboarding processes, collaborated with support teams to streamline agile workflows, strengthening client trust and operational efficiency.'}
    ],
    'education': [
        {'degree': 'REVA UNIVERSITY, BCA', 'period': 'Sep 2020 - April 2023 | Bengaluru, India', 'gpa': 'Cum. GPA: 8.2 / 10.0'},
        {'degree': 'JAIN UNIVERSITY, MCA', 'period': 'Jan 2024 - Present | Bengaluru, India'}
    ],
    'skills': {
        'programming': ['Python (2+ years active development in applications and control functions)', 'SQL', 'Java (Basics)', 'C++'],
        'data_tools': ['Elasticsearch', 'Kibana', 'Logstash', 'ETL', 'SAP', 'SAP HANA', 'SAP T-Codes'],
        'databases': ['SAP HANA', 'Oracle', 'MySQL Workbench', 'Elasticsearch', 'Azure', 'AWS']
    },
    'societies': [
        'Data Team – TnI Team (AIOps), Kyndryl Solutions (Led team in process improvement and ticket closure)',
        'Volunteer Data Analyst, Kyndryl Solutions (Contributed to off-boarding ticket closure and process optimization)'
    ],
    'links': [
        {'name': 'Github', 'url': 'https://github.com/SubramanyaSharmaBG'},
        {'name': 'LinkedIn', 'url': 'https://www.linkedin.com/in/subramanya-sharma-b-g'},
        {'name': 'CodeChef', 'url': 'https://www.codechef.com/users/subramanyasharmabg'}
    ]
}

# Home template (with highlights)
home_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ name }} - Home</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <header>
        <nav>
            <a href="experience.html">Experience</a>
            <a href="projects.html">Projects</a>
            <a href="education.html">Education</a>
            <a href="skills.html">Skills</a>
            <a href="societies.html">Societies</a>
            <a href="links.html">Links</a>
            <a href="contact.html">Contact</a>
        </nav>
        <h1>{{ name }}</h1>
        <p>{{ title }}</p>
        <p>{{ contact.email }} | {{ contact.phone }} | {{ contact.location }}</p>
    </header>

    <section id="welcome">
        <h2>Welcome to My Portfolio</h2>
        <p>Discover my journey in data engineering. Navigate to sections or filter highlights below.</p>
    </section>

    <div class="filters">
        <h3>Filter Highlights</h3>
        <select id="highlight-filter">
            <option value="all">All Highlights</option>
            <option value="posts">My Posts</option>
            <option value="certs">Certifications</option>
        </select>
    </div>

    <main class="highlights-container">
        <section id="posts" class="highlight-section visible">
            <h3>My Recent Posts</h3>
            <ul>
                {% for post in highlights.posts %}
                <li>
                    <strong>{{ post.title }}</strong> ({{ post.date }})<br>
                    {{ post.desc }}
                </li>
                {% endfor %}
            </ul>
        </section>

        <section id="certs" class="highlight-section visible">
            <h3>LinkedIn Certifications</h3>
            <ul>
                {% for cert in highlights.certs %}
                <li>
                    <strong>{{ cert.title }}</strong><br>
                    Issued by: {{ cert.issuer }} | Date: {{ cert.issue_date }} {% if cert.expire_date != 'None' %} (Expires: {{ cert.expire_date }}) {% endif %}
                </li>
                {% endfor %}
            </ul>
        </section>
    </main>

    <footer>
        <p>&copy; 2025 {{ name }}. Explore more via navigation.</p>
    </footer>

    <script src="script.js"></script>
</body>
</html>
"""

# Section template (point-wise lists)
section_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ name }} - {{ page_title }}</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <header>
        <nav>
            <a href="index.html">Home</a>
            <a href="experience.html">Experience</a>
            <a href="projects.html">Projects</a>
            <a href="education.html">Education</a>
            <a href="skills.html">Skills</a>
            <a href="societies.html">Societies</a>
            <a href="links.html">Links</a>
            <a href="contact.html">Contact</a>
        </nav>
        <h1>{{ name }} - {{ page_title }}</h1>
        <p>{{ title }}</p>
    </header>

    <main class="section-content">
        <h2 onclick="toggleContent(this)">{{ page_title }}</h2>
        <div class="content active">
            {{ content_html | safe }}
        </div>
    </main>

    <footer>
        <p>&copy; 2025 {{ name }}. <a href="index.html">Back to Home</a></p>
    </footer>

    <script src="script.js"></script>
</body>
</html>
"""

# Generate home
home_t = Template(home_template)
with open('index.html', 'w') as f:
    f.write(home_t.render(resume_data))

# Generate section pages
pages = {
    'experience': {'title': 'Experience', 'content': '<ul>{% for item in experience %}<li>{% if item.company %}<strong>{{ item.company }}</strong> - {{ item.period }}<br>{% endif %}{{ item.desc }}</li>{% endfor %}</ul>'},
    'projects': {'title': 'Projects', 'content': '<ul>{% for item in projects %}<li>{% if item.title %}<strong>{{ item.title }}</strong> - {{ item.period }}<br>{% endif %}{{ item.desc }}</li>{% endfor %}</ul>'},
    'education': {'title': 'Education', 'content': '<ul>{% for item in education %}<li><strong>{{ item.degree }}</strong> - {{ item.period }}{% if item.gpa %}<br>{{ item.gpa }}{% endif %}</li>{% endfor %}</ul>'},
    'skills': {'title': 'Skills', 'content': '<h3>Programming</h3><ul>{% for skill in skills.programming %}<li>{{ skill }}</li>{% endfor %}</ul><h3>Data Tools and Enterprise Tools</h3><ul>{% for skill in skills.data_tools %}<li>{{ skill }}</li>{% endfor %}</ul><h3>Databases and Cloud Platforms</h3><ul>{% for skill in skills.databases %}<li>{{ skill }}</li>{% endfor %}</ul>'},
    'societies': {'title': 'Societies', 'content': '<ul>{% for society in societies %}<li>{{ society }}</li>{% endfor %}</ul>'},
    'links': {'title': 'Links', 'content': '<ul>{% for link in links %}<li><a href="{{ link.url }}" target="_blank">{{ link.name }}: {{ name }}</a></li>{% endfor %}</ul>'},
    'contact': {'title': 'Contact', 'content': '<p>Let\'s connect! Reach out via email at <a href="mailto:{{ contact.email }}">{{ contact.email }}</a> or phone at {{ contact.phone }}. Download my full resume <a href="Subramanya Resume.pdf" download>here</a>.</p>'}
}

for page, data in pages.items():
    t = Template(data['content'])
    content_html = t.render(resume_data)
    page_data = {**resume_data, 'page_title': data['title'], 'content_html': content_html}
    sec_t = Template(section_template)
    with open(f"{page}.html", 'w') as f:
        f.write(sec_t.render(page_data))

print("Generated updated multi-page site from your resume PDF!")