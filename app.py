from flask import Flask, render_template, abort, request, send_from_directory
import markdown
import os

app = Flask(__name__)

# Path to your markdown blog posts
CONTENT_DIR = 'content'

# Helper to get all posts
def get_posts():
    posts = []
    for filename in os.listdir(CONTENT_DIR):
        if filename.endswith('.md'):
            slug = filename[:-3]
            with open(os.path.join(CONTENT_DIR, filename), 'r', encoding='utf-8') as f:
                title = f.readline().strip().replace('# ', '')
            posts.append({'slug': slug, 'title': title})
    return posts

@app.route('/')
def index():
    posts = get_posts()
    return render_template('index.html', posts=posts, title="Home - Niche Blog")

@app.route('/post/<slug>')
def post(slug):
    path = os.path.join(CONTENT_DIR, f'{slug}.md')
    if not os.path.exists(path):
        abort(404)
    with open(path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        title = lines[0].strip().replace('# ', '')
        content = ''.join(lines)
        html = markdown.markdown(content)
    return render_template('post.html', content=html, title=title)

@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory('static', filename)

# SEO metadata injection
@app.context_processor
def inject_meta():
    return {
        'meta_description': "A developer-friendly blog sharing tools, guides, and insights on niche tech topics.",
        'meta_keywords': "Flask blog, Python tools, developer guides, affiliate marketing"
    }

if __name__ == '__main__':
    os.makedirs('content', exist_ok=True)
    os.makedirs('static', exist_ok=True)
    # Create a sample post if it doesn't exist
    sample_post_path = os.path.join(CONTENT_DIR, 'getting-started.md')
    if not os.path.exists(sample_post_path):
        with open(sample_post_path, 'w', encoding='utf-8') as f:
            f.write("""# Getting Started with Flask Niche Blog

Welcome to your new Flask-powered niche content blog!

## What's Included:
- Markdown post support
- SEO-friendly templates
- Affiliate-ready layout

## Next Steps:
- Write your own content in `content/`
- Add affiliate links
- Promote on Reddit, Quora, Twitter

Happy blogging!

[Try Hostinger for ₹79/month](https://hostinger.in) ← Example affiliate link
""")

    # Create a basic CSS file
    css_path = os.path.join('static', 'style.css')
    if not os.path.exists(css_path):
        with open(css_path, 'w', encoding='utf-8') as f:
            f.write("""
body {
    font-family: Arial, sans-serif;
    max-width: 700px;
    margin: 40px auto;
    padding: 0 20px;
    line-height: 1.6;
    background: #f9f9f9;
    color: #333;
}

header h1 a {
    text-decoration: none;
    color: #222;
}

ul {
    list-style: none;
    padding: 0;
}

ul li {
    margin: 10px 0;
}

article a {
    color: #0077cc;
    text-decoration: underline;
}

footer {
    text-align: center;
    margin-top: 50px;
    font-size: 0.9em;
    color: #777;
}
""")

    app.run(debug=True)
