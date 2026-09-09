from flask import Flask, render_template
from posts import posts
import markdown


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

@app.route ('/blog/<slug>')
def blog_post(slug):
    post = next((p for p in posts if p['slug'] == slug), None)
    if post:
        with open(f'blog_post/{post["slug"]}.md', 'r', encoding='utf-8') as f:
            post['content_html'] = markdown.markdown(f.read(), extensions=['fenced_code'])
    return render_template('post.html', post=post)

if __name__ == '__main__':
    app.run(debug=True)