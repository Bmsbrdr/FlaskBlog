import json
import os
from flask import Flask, render_template
import _json

app = Flask(__name__)


@app.route('/')
def index():
    json_data = open(os.path.join("static", "BlogEntry.json"),"r")
    blog_entries = []
    entries = json.load(json_data)
    for entry in entries:
        blog_entries.append(BlogEntry(entry["id"], entry["author"], entry["title"], entry["content"]))
    return render_template('index.html', blogentries=blog_entries)


class BlogEntry:
    def __init__(self, author_id, author, title, content):
        self.author_id = author_id
        self.title = title
        self.author = author
        self.content = content

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)