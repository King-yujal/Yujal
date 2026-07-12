import json
import os
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
# Explicitly open up the server to accept all incoming traffic from GitHub Pages
CORS(app, resources={r"/*": {"origins": "*"}})


@app.route("/search", methods=["GET"])
def search():
    query = request.args.get("q", "").lower().strip()
    if not query:
        return jsonify([])

    # Load crawled database index safely
    try:
        with open("search_index.json", "r", encoding="utf-8") as f:
            database = json.load(f)
    except FileNotFoundError:
        return jsonify([
            {
                "title": "Database Empty",
                "snippet": "Fill search_index.json on GitHub!",
                "url": "",
            }
        ])

    # Search filtering rules (Converts inputs and data loops to lowercase)
    results = []
    for item in database:
        if (
            query in item["title"].lower()
            or query in item["snippet"].lower()
            or query in item["url"].lower()
        ):
            results.append(item)

    return jsonify(results)


if __name__ == "__main__":
    # Dynamically bind to Render's internal cloud port settings
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
