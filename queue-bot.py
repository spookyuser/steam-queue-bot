import http.client, urllib.parse
import uuid
import json
import os


class SteamQueue:
    def __init__(self, steam_remember_login, steam_login_secure, steam_machine_auth):
        self.steam_machine_auth = steam_machine_auth
        self.steam_login_secure = steam_login_secure
        self.steam_remember_login = steam_remember_login
        self.session_id = uuid.uuid4().hex
        self.payload = {"sessionid": self.session_id}
        self.connection = http.client.HTTPSConnection("store.steampowered.com")
        self.headers = self.generate_headers()

    def generate_cookie(self):
        machine_auth_number = self.steam_login_secure.split("%7C")[0]
        cookie = (
            f"steamMachineAuth{machine_auth_number}={self.steam_machine_auth};"
            f"steamRememberLogin={self.steam_remember_login};"
            f"steamLoginSecure={self.steam_login_secure};"
            f"sessionid={self.session_id};"
        )
        return {"cookie": cookie}

    def generate_headers(self):
        headers = {
            "connection": "keep-alive",
            "accept": "*/*",
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
        }
        cookie = self.generate_cookie()
        headers.update(cookie)
        return headers

    def get_explore_queue(self):
        self.connection.request(
            "POST",
            "/explore/generatenewdiscoveryqueue",
            urllib.parse.urlencode(self.payload),
            self.headers,
        )
        response = self.connection.getresponse()
        if response.status == 200:
            data = response.read()
            print("Game queue generated")
            return json.loads(data.decode("utf-8"))["queue"]
        else:
            print(
                f"Failed to generate queue (steam responded with code {response.status})"
            )
            exit()
            

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
    queue = SteamQueue(
        os.getenv("STEAM_REMEMBER_LOGIN"),
        os.getenv("STEAM_LOGIN_SECURE"),
        os.getenv("STEAM_MACHINE_AUTH"),
    )
    app_ids = queue.get_explore_queue()
    queue.clear_queue(app_ids)
