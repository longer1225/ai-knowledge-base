
from backend.config.backend_base_settings import API_BASE_URL
import requests

class RequestUtil:
    def __init__(self, state):
        self.state = state

    def headers(self):
        h = {"Content-Type": "application/json"}
        if self.state["token"]:
            h["Authorization"] = f"Bearer {self.state['token']}"
        return h

    def get(self, url):
        return requests.get(API_BASE_URL + url, headers=self.headers()).json()

    def post(self, url, data):
        return requests.post(API_BASE_URL + url, json=data, headers=self.headers()).json()

    def delete(self, url):
        return requests.delete(API_BASE_URL + url, headers=self.headers()).json()

    def stream_post(self, url, data):
        res = requests.post(
            API_BASE_URL + url,
            json=data,
            headers=self.headers(),
            stream=True
        )
        for chunk in res.iter_content(chunk_size=8, decode_unicode=True):
            if chunk:
                yield chunk