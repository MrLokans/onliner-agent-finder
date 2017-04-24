import json

from flask import Flask, jsonify
app = Flask(__name__)


@app.route("/api/agents/<agent_url>")
def agent_data(agent_url):
    with open('agent_response.json', 'r') as f:
        data = json.load(f)
        return jsonify(data)


if __name__ == "__main__":
    app.run(debug=True)
