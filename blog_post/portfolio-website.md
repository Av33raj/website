# Building My Own Portfolio Website with Flask


## The problem

I needed somewhere to actually show off the projects I've been building. A CV can list "Python, security tooling, networking" as bullet points, but it can't demonstrate any of it. I wanted a site I'd built myself, from scratch, that could double as proof of the skills it was describing — a working full-stack project, not just a static page listing my other projects.

The requirements were fairly simple on paper: a homepage, an About page, a Projects page, and a blog where I could write up each project in more depth as I finish it. The tricky part turned out to be less "can I build a webpage" and more "how do I structure this so it's easy to keep adding to."

## Approach

I built the site with **Flask**, a lightweight Python web framework. I picked it over a plain static site mainly because I already had some Python experience, and because a Flask project is itself a decent thing to point to on a CV — it shows routing, templating, and basic backend logic, not just HTML and CSS.

### Templates and structure

Rather than repeating the same navbar and footer HTML on every page, I used Jinja2's template inheritance. A single `base.html` holds the shared layout — nav bar, `<head>`, footer — with a `{% block content %}` placeholder in the middle. Every other page (`index.html`, `about.html`, `projects.html`, `blog.html`, `post.html`) extends that base and only fills in its own content block:

```html
{% extends "base.html" %}
{% block title %}About{% endblock %}
{% block content %}
    <h1>About Me</h1>
    <p>...</p>
{% endblock %}
```

This kept things DRY, but it also caused one of my first real bugs: a page not extending correctly because `{% extends %}` has to be the very first line in the file, with nothing above it — not even a blank line. Easy to miss, annoying to debug the first time it happens.

### Styling with CSS variables

Instead of hardcoding colours throughout the stylesheet, I defined them once under `:root` and referenced them everywhere with `var(--name)`:

```css
:root {
    --colour-body: #222;
    --colour-bg: url('../background.jpg');
    --colour-nav: #46567a;
    --colour-nav-a: white;
    --colour-footer: #777;
}
```

This paid off almost immediately — when I wanted to darken the whole site's theme, it was a one-line change instead of hunting through every rule. It also caught me out once: I set a background image through a variable but applied it to `background-color` instead of `background-image`. `background-color` silently ignores anything that isn't a plain colour, so the image just never appeared, with no error to point at the mistake. Swapping to `background-image: var(--colour-bg);` fixed it.

### Layout: centering vs. offsetting

Getting the page content to behave consistently across screen sizes took more trial and error than I expected. My first attempt styled the heading and paragraphs separately, each with their own `max-width` and `margin: auto` — which centered them, but as two *different* widths, so they only lined up by coincidence at one particular window size. Resizing the browser made them drift apart.

The fix was wrapping everything — heading included — inside a single container div (`.page_content`) with one shared `max-width` and `margin: auto`, so the whole block moves and re-centers as one unit no matter the screen size. Where I wanted the heading offset slightly to the left of the paragraphs, I used a negative `margin-left` on just the `h1` inside that container — small enough to stay within the container's own padding rather than escaping the box (which happened when I first tried it with `width: fit-content` sized too tightly).

### A custom font and background image

I added a variable font using `@font-face`:

```css
@font-face {
    font-family: 'Telma';
    src: url('Telma-Variable.ttf');
}
```

and a fixed background image behind the whole page:

```css
body {
    background-image: var(--colour-bg);
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
    background-repeat: no-repeat;
}
```

`background-attachment: fixed` keeps the image still while the page content scrolls over it, which reads a lot more polished than a background scrolling with everything else. To keep text readable on top of it, I gave the content container a semi-transparent background using `rgba(255, 255, 255, 0.85)` rather than a solid colour — enough contrast for the text, while still letting a hint of the image show through underneath.

### The blog itself

This is the part I iterated on the most. My first version stored each post as a plain Python string inside a list in `posts.py` — workable for two short placeholder entries, but clearly not going to scale once a write-up has headings, code blocks, and several paragraphs. Editing one giant one-line string inside a Python file is not a pleasant experience.

I restructured it so `posts.py` only holds metadata:

```python
posts = [
    {
        "slug": "port-scanner",
        "title": "Python Port Scanner",
        "summary": "A tool built with python-nmap to scan and export results.",
    },
]
```

and each post's actual write-up lives in its own `.md` file inside a `blog_post/` folder, named after its slug. The Flask route reads the matching file and converts it from markdown to HTML on the fly:

```python
import markdown

@app.route('/blog/<slug>')
def blog_post(slug):
    post = next((p for p in posts if p['slug'] == slug), None)
    if post:
        with open(f'blog_post/{post["slug"]}.md', 'r', encoding='utf-8') as f:
            post['content_html'] = markdown.markdown(f.read(), extensions=['fenced_code'])
    return render_template('post.html', post=post)
```

`post.html` then renders that converted HTML directly, using Jinja2's `| safe` filter so Flask doesn't escape the tags (Flask auto-escapes HTML by default as a security measure, which would otherwise print raw `<h2>` tags as visible text instead of rendering them):

```html
{{ post.content_html | safe }}
```

The `fenced_code` extension means triple-backtick code blocks in the markdown get wrapped in proper `<pre><code>` tags rather than rendering as plain paragraph text.

Along the way I also managed to define the same `/blog/<slug>` route twice in the Flask app — once from an early version, once from the rewrite — which Flask refused to start over with an `AssertionError` about overwriting an existing endpoint. A reminder that copy-pasting new route logic in without checking what's already there can leave duplicates behind.

## What went wrong (and what I'd do differently)

- **Slugs need to be URL-safe from the start.** I initially used titles-with-spaces as slugs (`"Portfolio website"`), which produces awkward URLs like `/blog/Portfolio website`. Lowercase, hyphenated slugs from the beginning would have saved a cleanup pass later.
- **Silent CSS failures are the hardest to debug.** Both the `background-color` vs `background-image` mix-up and a mismatched CSS variable name failed with no error message at all — just nothing happening. Browser DevTools' Styles panel (checking whether a rule is crossed out/overridden) ended up being the fastest way to actually diagnose these.
- **Decide the content format before writing content.** Restructuring from inline strings to separate markdown files after I'd already started writing posts meant redoing work. Picking the markdown-file approach from the start would have avoided that.

## What's next

A few things I'd like to add:
- A working contact form
- A downloadable PDF version of my CV linked from the About page
- Syntax highlighting inside code blocks (currently just plain monospace formatting)
- Possibly deploying it live via Render or PythonAnywhere, so it's not just running locally

## Code

The full project is on GitHub, and this write-up itself is one of the posts running on the live site.
