from flask import Flask, render_template, send_from_directory, redirect, url_for
import os

app = Flask(__name__)

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

if __name__ == '__main__':
    app.run(debug=True)
