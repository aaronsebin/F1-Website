import requests

BASE_URL = "https://f1api.dev/api"


class F1APIError(Exception):
    pass


def get_f1_data(endpoint):
    url = f"{BASE_URL}/{endpoint.lstrip('/')}"

    try:
        response = requests.get(url, timeout=15)
        print(f"F1 API URL: {url}")
        print(f"F1 API STATUS: {response.status_code}")
        response.raise_for_status()
        return response.json()

    except (requests.RequestException, ValueError) as error:
        print(f"F1 API FAILURE: {url} — {error}")
        raise F1APIError(
            f"Unable to retrieve Formula 1 data from {url}"
        ) from error