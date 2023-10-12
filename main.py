from flask import Flask, request
from token_generator import generate_token
import urllib.request
import json

app = Flask(__name__)

def parse_opened_pr_comments_url(request):
    request_type = request.json["action"]
    if request_type != "opened":
        return

    return request.json["pull_request"]["comments_url"]


def _build_basic_opener(bearer_token):
    """
    Build and return an opener with Bearer HTTP Authentication
    """
    opener = urllib.request.build_opener()
    opener.addheaders.append(("Authorization", f"Bearer {bearer_token}"))
    opener.addheaders.append(("Accept", "application/vnd.github+json"))
    return opener

def _build_token_opener(bearer_token):
    """
    Build and return an opener with Bearer HTTP Authentication
    """
    opener = urllib.request.build_opener()
    opener.addheaders.append(("Authorization", f"token {bearer_token}"))
    opener.addheaders.append(("Accept", "application/vnd.github+json"))
    return opener

def generate_api_token():
    installation_endpoint = "https://api.github.com/app/installations"

    token = generate_token()
    opener = _build_basic_opener(token)

    req = urllib.request.Request(installation_endpoint)
    with opener.open(req) as response:
        json_content = json.loads(response.read())
        # TODO: There is only one app for now, but this should be resolved with APP ID
        access_tokens_url = json_content[0]["access_tokens_url"]

    req = urllib.request.Request(access_tokens_url, method = "POST")
    with opener.open(req) as response:
        json_content = json.loads(response.read())
        api_token = json_content["token"]

    print(api_token)
    return api_token

def comment_image(comments_url, api_token):
    image_link = "https://i.imgflip.com/82bvfj.jpg"
    opener = _build_token_opener(api_token)

    data = json.dumps({"body": f"![Image description]({image_link})"})
    encoded_data = data.encode('utf-8')
    print(encoded_data)
    req = urllib.request.Request(comments_url, data=encoded_data, method="POST")
    with opener.open(req) as reponse:
        pass


@app.route('/', methods=["POST"])
def hello_world():
    pr_comments_url = parse_opened_pr_comments_url(request)

    api_token = generate_api_token()

    comment_image(pr_comments_url, api_token)

    return "", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=True)
