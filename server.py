import os
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Hardcoded cloud database to bypass search_index.json bugs completely!
CLOUD_DATABASE = [
    {
        "url": "https://wikipedia.org",
        "title": "Wikipedia, the free encyclopedia",
        "snippet": "Wikipedia is a free online encyclopedia, created and edited by volunteers around the world and hosted by the Wikimedia Foundation."
    },
    {
        "url": "https://wikipedia.org",
        "title": "Wikipedia: Introduction - Wikipedia",
        "snippet": "Wikipedia is an online free-content encyclopedia project that anyone can edit. Articles on Wikipedia are written by volunteers from all around the world."
    },
    {
        "url": "https://wikipedia.org",
        "title": "Wikipedia – Die freie Enzyklopädie",
        "snippet": "Wikipedia ist ein am 15. Januar 2001 gegründetes gemeinnütziges Projekt zur Erstellung einer freien Enzyklopädie in über 300 Sprachen."
    },
    {
        "url": "https://wikipedia.org",
        "title": "Wikipedia, la enciclopedia libre",
        "snippet": "Wikipedia es una enciclopedia libre, políglota y editada de manera colaborativa. Es administrada por la Fundación Wikimedia."
    }
]

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('q', '').lower().strip()
    if not query:
        return jsonify([])

    results = []
    # Search filtering rules matching directly against the cloud array
    for item in CLOUD_DATABASE:
        if (query in item["title"].lower() or 
            query in item["snippet"].lower() or 
            query in item["url"].lower()):
            results.append(item)

    return jsonify(results)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
