import requests

class Client:
    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url
        self.headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}

    def handle_request(self, method: str, endpoint: str, params=None, data=None):
        url = f"{self.base_url}/{endpoint}"
        response = requests.request(
            method=method,
            url=url,
            headers=self.headers,
            params=params,
            json=data
        )

        if not response.ok:
            response.raise_for_status()

        if response.status_code == 204:
            return None
        
        return response.json()
