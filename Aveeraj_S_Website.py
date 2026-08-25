from flask import Flask, render_template
from posts import posts

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/projects')
def projects():
    return render_template('projects.html')

@app.route('/blog')
def blog():
    return render_template('blog.html', posts=posts)

@app.route('/blog/<slug>')
def blog_post(slug):
    post = next((p for p in posts if p['slug'] == slug), None)
    return render_template('post.html', post=post)

if __name__ == '__main__':
    app.run(debug=True)