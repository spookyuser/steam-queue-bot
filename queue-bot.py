import http.client, urllib.parse
import json
import os


def parse_cookie(cookie):
    cookie = cookie.split(";")
    cookie = [c.strip() for c in cookie]
    cookie = [c.split("=") for c in cookie]
    cookie = {c[0]: c[1] for c in cookie}
    return cookie


class SteamQueue:
    def __init__(self, cookie_string: str):
        self.cookie = parse_cookie(cookie_string)
        session_id = self.cookie.get("sessionid")
        if not session_id:
            raise Exception("Session ID not found in cookie")
        self.payload = {"sessionid": session_id, "queuetype": "0"}
        self.connection = http.client.HTTPSConnection("store.steampowered.com")
        self.headers = self.generate_headers()

    def generate_headers(self):
        headers = {
            "connection": "keep-alive",
            "accept": "*/*",
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Cookie": "; ".join([f"{k}={v}" for k, v in self.cookie.items()]),
        }
        print(headers)
        return headers

    def get_explore_queue(self):
        self.connection.request(
            "POST",
            "/explore/generatenewdiscoveryqueue",
            urllib.parse.urlencode(self.payload),
            headers=self.headers,
        )
        response = self.connection.getresponse()
        if response.status == 200:
            data = response.read()
            print(data)
            print("Game queue generated")
            return json.loads(data.decode("utf-8"))["queue"]
        else:
            raise Exception(
                f"Failed to generate queue (steam responded with code {response.status})"
            )

    def clear_queue(self, app_ids):
        print("Visiting games in queue")
        for index, app_id in enumerate(app_ids):
            self.payload.update({"appid_to_clear_from_queue": app_id})
            self.connection.request(
                "POST", "/app/60", urllib.parse.urlencode(self.payload), self.headers
            )
            self.connection.getresponse().read()
            print(f"Game {index+1}/{len(app_ids)} visited")
        print("Queue successfully cleared")


if __name__ == "__main__":
    cookie = os.environ.get("STEAM_COOKIE")
    if not cookie:
        raise Exception("STEAM_COOKIE environment variable not set")
    queue = SteamQueue(cookie)
    app_ids = queue.get_explore_queue()
    queue.clear_queue(app_ids)
