import argparse
import requests
import json
import config

# Set base URL and endpoints
BASE_URL = "http://192.168.64.2:30000"
TOKEN_ENDPOINT = "/token"

class InvalidCreds(Exception):
    pass
class APIError(Exception):
    pass


class Client:
    def __init__(self):
        self.creds = config.load()

    def login(self) -> None:
        """Fetches the access token from the API.

        Raises:
            LoginError: if credentials are invalid.
            APIError: if the API returns an error.
        """
        # Load credentials from the config file
        # Send a POST request to the token endpoint
        url = f"{BASE_URL}{TOKEN_ENDPOINT}"
        headers = {
            "accept": "application/json",
            "Content-Type": "application/x-www-form-urlencoded",
        }
        data = f"username={self.creds.username}&password={self.creds.password}"

        response = requests.post(url, headers=headers, data=data)

        if response.status_code == 401:
            raise InvalidCreds
        if not response.ok:
            raise APIError

        # Extract the access token from the response, save it to the config file, and return it
        self.creds.access_token = response.json()["access_token"]
        config.save(self.creds)
        print("Login successful.")

    def request(self, method: str, endpoint: str, body) -> dict:
        """Sends a request to the API. If the access token has expired, it will attempt to re-login.
        Raises:
            requests.exceptions: if the API returns an error."""
        url = f"{BASE_URL}{endpoint}"
        headers = {"Authorization": f"Bearer {self.creds.access_token}"}

        response = requests.request(method, url, headers=headers, data=body)

        if response.status_code == 401:
            print("Error: Token expired. Attempting to re-login.")
            # Re-login and update the access token
            self.login()
            return self.request(method, endpoint, body)
        
        response.raise_for_status()
        return response.json()



# Main function
def main():
    parser = argparse.ArgumentParser(description="API Client")
    parser.add_argument("endpoint")
    args = parser.parse_args()

    client = Client()
    items = client.request("GET", args.endpoint, None)
    print(json.dumps(items, indent=2))

if __name__ == "__main__":
    main()
