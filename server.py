import json
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
@app.route("/search", methods=["GET"])
def search():
    query = request.args.get("q", "").lower().strip()
    if not query:
        return jsonify([])

    # Load crawled database index
    try:
        with open("search_index.json", "r", encoding="utf-8") as f:
            database = json.load(f)
    except FileNotFoundError:
        return jsonify(
            [{"title": "Database Empty", "snippet": "Run crawler.py first!", "url": ""}]
        )

    # Search filtering rules (Check match in title or snippet text)
    results = []
    for item in database:
        if query in item["title"].lower() or query in item["snippet"].lower():
            results.append(item)

    return jsonify(results)


if __name__ == "__main__":
    app.run(port=5000, debug=True)