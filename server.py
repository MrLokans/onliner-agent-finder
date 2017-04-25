from collections import Counter
import json

from flask import Flask, abort, jsonify
app = Flask(__name__)


@app.route("/api/agents/<agent_url>")
def agent_data(agent_url):
    if agent_url == 'doesnotexist':
        abort(404)

    bulletins = []
    data = {}
    with open('bulletins.json') as f:
        bulletins = json.load(f)
        urls = [d['url'].split('/')[-1] for d in bulletins]
        c = Counter(urls)

        user_links = c.get(agent_url)
        if user_links is None or int(user_links) < 2:
            data = {'is_agent_probability': -1,
                    'post_count': 0,
                    "posts": []}
        else:
            posts = [d['origin_url'] for d in bulletins if agent_url in d['url']]
            data = {'is_agent_probability': 100,
                    'post_count': int(user_links),
                    "posts": posts}
        return jsonify(data)


if __name__ == "__main__":
    app.run(debug=True)
