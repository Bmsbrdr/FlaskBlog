import json
import os
from flask import Flask, render_template, request, redirect, url_for
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

@app.route('/add', methods=['GET', 'POST'])
def add():


    if request.method == 'POST':
        with open(os.path.join("static", "BlogEntry.json"), "r") as json_data:
            entries = json.load(json_data)
        id_counter = len(entries)
        author = request.form['author']
        title = request.form['title']
        content = request.form['content']
        new_post ={
            "id" : id_counter+1,
            "author" : author,
            "title" : title,
            "content" : content
        }
        #{"id": 1, "author": "John Doe", "title": "First Post", "content": "This is my first post."}
        entries.append(new_post)
        with open(os.path.join("static", "BlogEntry.json"),"w") as f:
            json.dump(entries,f, indent=4)
        return redirect(url_for('index'))
    elif request.method == 'GET':
        json_data = open(os.path.join("static", "BlogEntry.json"), "r")
        entries = json.load(json_data)
        return render_template('add.html', entries=entries)
    return render_template('add.html')

class BlogEntry:
    def __init__(self, author_id, author, title, content):
        self.author_id = author_id
        self.title = title
        self.author = author
        self.content = content

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)