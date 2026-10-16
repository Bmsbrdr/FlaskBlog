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
        blog_entries.append(BlogEntry(
            entry["id"],
            entry["author"],
            entry["title"],
            entry["content"],
            entry.get("likes", 0)  # Likes auslesen
        ))
    return render_template('index.html', blogentries=blog_entries)


@app.route('/like/<int:post_id>', methods=['POST'])
def like_post(post_id):
    json_path = os.path.join("static", "BlogEntry.json")

    with open(json_path, "r", encoding="utf-8") as f:
        entries = json.load(f)

    for entry in entries:
        if entry.get("id") == post_id:
            # Falls das Feld noch nicht existiert, bei 0 starten
            if "likes" not in entry:
                entry["likes"] = 0
            entry["likes"] += 1
            break

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(entries, f, indent=4, ensure_ascii=False)

    return redirect(url_for('index'))

@app.route('/delete/<int:post_id>', methods=['POST'])
def delete(post_id):
    with open(os.path.join("static", "BlogEntry.json"), "r") as json_data:
        entries = json.load(json_data)
    for(entry) in entries:
        if entry["id"] == post_id:
            entries.remove(entry)
            break
    with open(os.path.join("static", "BlogEntry.json"), "w") as f:
        json.dump(entries, f, indent=4)
    return redirect(url_for('index'))
@app.route('/update/<int:post_id>')
def update(post_id):
    with open(os.path.join("static", "BlogEntry.json"), "r", encoding="utf-8") as json_data:
        entries = json.load(json_data)

    # Den passenden Eintrag anhand der ID suchen
    blogentry = None
    for entry in entries:
        if entry.get("id") == post_id:
            blogentry = entry
            break

    if not blogentry:
        return "Eintrag nicht gefunden", 404

    # WICHTIG: return nutzen und blogentry an das Template übergeben!
    return render_template("update.html", blogentry=blogentry)

@app.route('/edit/<int:post_id>', methods=['POST', 'GET'])
def edit(post_id):
    with open(os.path.join("static", "BlogEntry.json"), "r") as json_data:
        entries = json.load(json_data)

    if request.method == 'POST':
        entries[post_id-1]["author"] = request.form['author']
        entries[post_id-1]["title"] = request.form['title']
        entries[post_id-1]["content"] = request.form['content']
        with open(os.path.join("static", "BlogEntry.json"), "w", encoding="utf-8") as json_file:
            json.dump(entries, json_file, indent=4, ensure_ascii=False)

        return redirect(url_for('index'))

    elif request.method == 'GET':
        blogentry = entries[post_id]
        return render_template("edit.html", blogentry=blogentry, post_id=post_id)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        highest_id = 0
        with open(os.path.join("static", "BlogEntry.json"), "r") as json_data:
            entries = json.load(json_data)

        id_counter = get_highest_id(entries)+1
        author = request.form['author']
        title = request.form['title']
        content = request.form['content']
        new_post ={
            "id" : id_counter,
            "author" : author,
            "title" : title,
            "content" : content
        }
        entries.append(new_post)
        with open(os.path.join("static", "BlogEntry.json"),"w") as f:
            json.dump(entries,f, indent=4)
        return redirect(url_for('index'))
    elif request.method == 'GET':
        json_data = open(os.path.join("static", "BlogEntry.json"), "r")
        entries = json.load(json_data)
        return render_template('add.html', entries=entries)
    return render_template('add.html')

def get_highest_id(entries) -> int:
    highest_id = 0
    for (entry) in entries:
        if entry["id"] > highest_id:
            highest_id = entry["id"]
    return highest_id

class BlogEntry:
    def __init__(self, author_id, author, title, content, likes=0):
        self.author_id = author_id
        self.title = title
        self.author = author
        self.content = content
        self.likes = likes

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)