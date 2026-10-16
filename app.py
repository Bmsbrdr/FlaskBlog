from dataclasses import dataclass
import json
import os
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
JSON_PATH = os.path.join("static", "BlogEntry.json")


@dataclass
class BlogEntry:
    id: int
    author: str
    title: str
    content: str
    likes: int = 0


def _load_raw_entries() -> list[dict]:
    if not os.path.exists(JSON_PATH):
        return []
    with open(JSON_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def _save_raw_entries(entries: list[dict]) -> None:
    with open(JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(entries, f, indent=4, ensure_ascii=False)


@app.route('/')
def index():
    entries = _load_raw_entries()
    blog_entries = [
        BlogEntry(
            id=entry["id"],
            author=entry["author"],
            title=entry["title"],
            content=entry["content"],
            likes=entry.get("likes", 0)
        )
        for entry in entries
    ]
    return render_template('index.html', blogentries=blog_entries)


@app.route('/like/<int:id>', methods=['POST'])
def like_entry(id):
    entries = _load_raw_entries()
    for entry in entries:
        if entry.get("id") == id:
            entry["likes"] = entry.get("likes", 0) + 1
            break
    _save_raw_entries(entries)
    return redirect(url_for('index'))


@app.route('/delete/<int:id>', methods=['POST'])
def delete_entry(id):
    entries = _load_raw_entries()
    entries = [entry for entry in entries if entry.get("id") != id]
    _save_raw_entries(entries)
    return redirect(url_for('index'))


@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_entry(id):
    entries = _load_raw_entries()

    if request.method == 'POST':
        for entry in entries:
            if entry.get("id") == id:
                entry["author"] = request.form['author']
                entry["title"] = request.form['title']
                entry["content"] = request.form['content']
                break
        _save_raw_entries(entries)
        return redirect(url_for('index'))

    blogentry = next((entry for entry in entries if entry.get("id") == id), None)
    if not blogentry:
        return "Eintrag nicht gefunden", 404

    return render_template("update.html", blogentry=blogentry)


@app.route('/add', methods=['GET', 'POST'])
def add_entry():
    if request.method == 'POST':
        entries = _load_raw_entries()
        highest_id = max([entry["id"] for entry in entries], default=0)

        new_post = {
            "id": highest_id + 1,
            "author": request.form['author'],
            "title": request.form['title'],
            "content": request.form['content'],
            "likes": 0
        }
        entries.append(new_post)
        _save_raw_entries(entries)
        return redirect(url_for('index'))

    return render_template('add.html')


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)