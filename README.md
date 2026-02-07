# Subramanya Sharma - Portfolio Website

Welcome to the repository for **Subramanya Sharma's Personal Portfolio**. This project showcases my professional experience, skills, projects, and certifications as a Data Engineer. It is a single-page application (SPA) built with **Flask**, **HTML5**, **CSS3**, and **Vanilla JavaScript**.

## 🚀 Features

-   **SPA Architecture**: Seamless navigation without full page reloads using the History API and `fetch`.
-   **Interactive Skills Section**: Click on skills to reveal detailed usage descriptions in a modal.
-   **Responsive Design**: Optimized for desktops, tablets, and mobile devices.
-   **Dark/Light Mode**: User preference support with local storage persistence.
-   **Dynamic Content**: Resume viewing and downloadable resources.

## 🛠 Tech Stack

-   **Backend**: Python (Flask)
-   **Frontend**: HTML5, CSS3 (Custom Variables & Animations), JavaScript (ES6+)
-   **Styling**: Font Awesome, Google Fonts (Inter, Playfair Display)
-   **Deployment**: Ready for deployment on platforms like Vercel, Heroku, or Render.

## 📂 Project Structure

```text
Subramanya-Sharma/
├── static/
│   ├── css/
│   │   └── spa.css       # Main stylesheet variables, animations, and responsive rules
│   ├── js/
│   │   └── spa.js        # SPA routing, modal logic, data for skills, and theme toggle
│   ├── img/              # Images and assets
│   │   ├── avatar.jpg
│   │   └── certs/        # Certification images
│   └── docs/             # Document files like Resume
├── templates/            # HTML Templates
│   ├── base.html         # Base layout with navbar and footer
│   ├── index.html        # Landing page
│   ├── about.html        # About Me section
│   ├── experience.html   # Work experience timeline
│   ├── projects.html     # Technical projects showcase
│   ├── skills.html       # Interactive skills grid
│   ├── certifications.html # Certificates gallery
│   ├── contact.html      # Contact information
│   └── resume.html       # Resume viewer
├── app.py                # Flask application entry point
├── requirements.txt      # Python dependencies
└── README.md             # Project documentation
```

## 🔧 Installation & Running

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/subbusharma123/Subramanya-Sharma.git
    cd Subramanya-Sharma
    ```

2.  **Create a virtual environment** (optional but recommended):
    ```bash
    python -m venv venv
    # Windows
    venv\Scripts\activate
    # macOS/Linux
    source venv/bin/activate
    ```

3.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the application**:
    ```bash
    python app.py
    ```

5.  **View locally**:
    Open your browser and navigate to `http://127.0.0.1:5000`.

## 🤝 Contributing

This is a personal portfolio, but suggestions and feedback are always welcome!
1.  Fork the repository.
2.  Create your feature branch (`git checkout -b feature/AmazingFeature`).
3.  Commit your changes (`git commit -m 'Add some AmazingFeature'`).
4.  Push to the branch (`git push origin feature/AmazingFeature`).
5.  Open a Pull Request.

## 📬 Contact

**Subramanya Sharma B.G.**
-   **GitHub**: [subbusharma123](https://github.com/subbusharma123)
-   **LinkedIn**: [Subramanya Sharma](https://www.linkedin.com/in/subramanya-sharma-b-g-7a0a0a1a0/)

---
*© 2026 Subramanya Sharma B.G. All Rights Reserved.*
