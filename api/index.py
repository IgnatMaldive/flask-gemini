from flask import Flask, render_template, abort
import os
import markdown
import frontmatter

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/blog')
def blog():
    posts = []
    blog_posts_dir = os.path.join(app.root_path, 'blog_posts')
    for filename in os.listdir(blog_posts_dir):
        if filename.endswith('.md'):
            filepath = os.path.join(blog_posts_dir, filename)
            with open(filepath, 'r', encoding='utf-8') as f:
                post = frontmatter.load(f)
                slug = filename.replace('.md', '')
                
                # Generate a snippet from the content
                snippet = "".join(post.content.splitlines()[:3]) # Take first 3 lines as snippet
                if len(post.content.splitlines()) > 3:
                    snippet += "..."
                
                posts.append({
                    'title': post.metadata.get('title', slug.replace('-', ' ').title()),
                    'slug': slug,
                    'content': markdown.markdown(post.content),
                    'snippet': markdown.markdown(snippet), # Convert snippet to HTML
                    'date': post.metadata.get('date'),
                    'featured_image': post.metadata.get('featured_image'),
                    'tags': post.metadata.get('tags', [])
                })
    # Sort posts by date, newest first
    posts.sort(key=lambda x: x['date'] if x['date'] else '', reverse=True)
    return render_template('blog.html', posts=posts)

@app.route('/blog/<slug>')
def post(slug):
    filepath = os.path.join(app.root_path, 'blog_posts', f'{slug}.md')
    if not os.path.exists(filepath):
        abort(404)

    with open(filepath, 'r', encoding='utf-8') as f:
        post = frontmatter.load(f)
        html_content = markdown.markdown(post.content)
        title = post.metadata.get('title', slug.replace('-', ' ').title())
        date = post.metadata.get('date')
        featured_image = post.metadata.get('featured_image')
        tags = post.metadata.get('tags', [])

    return render_template('post.html', title=title, content=html_content, date=date, featured_image=featured_image, tags=tags)