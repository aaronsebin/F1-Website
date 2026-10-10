
import requests

BASE_URL = "https://f1api.dev/api"


class F1APIError(Exception):
    """Raised when the F1 API request fails."""
    pass


def get_f1_data(endpoint):
    url = f"{BASE_URL}/{endpoint.lstrip('/')}"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()

    except (requests.RequestException, ValueError) as error:
        raise F1APIError(
            "Unable to retrieve Formula 1 data."
        ) from error
