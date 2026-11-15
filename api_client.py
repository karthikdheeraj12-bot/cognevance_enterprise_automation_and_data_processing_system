
import requests

from config import (
    API_BASE_URL,
    POSTS_ENDPOINT,
    USERS_ENDPOINT,
    REQUEST_TIMEOUT
)


def validate_api_data(data):
    """Validate that an API response contains the expected structure."""

    if not isinstance(data, list):
        raise ValueError("Expected a list of records.")

    for record in data:
        if not isinstance(record, dict):
            raise ValueError("Invalid record format.")

    return data


def fetch_posts():
    """Fetch all posts from the API."""

    url = API_BASE_URL + POSTS_ENDPOINT

    try:
        response = requests.get(
            url,
            timeout=REQUEST_TIMEOUT
        )

        response.raise_for_status()

        posts = validate_api_data(response.json())

        print(f"Successfully fetched {len(posts)} posts.")

        return posts

    except requests.exceptions.Timeout:
        print("Error: API request timed out.")

    except requests.exceptions.ConnectionError:
        print("Error: Unable to connect to the API.")

    except requests.exceptions.HTTPError as error:
        print(f"HTTP Error: {error}")

    except requests.exceptions.RequestException as error:
        print(f"API Request Error: {error}")

    except ValueError:
        print("Error: Invalid JSON response.")

    return []


def fetch_users():
    """Fetch all users from the API."""

    url = API_BASE_URL + USERS_ENDPOINT

    try:
        response = requests.get(
            url,
            timeout=REQUEST_TIMEOUT
        )

        response.raise_for_status()

        users = validate_api_data(response.json())

        print(f"Successfully fetched {len(users)} users.")

        return users

    except requests.exceptions.Timeout:
        print("Error: API request timed out.")

    except requests.exceptions.ConnectionError:
        print("Error: Unable to connect to the API.")

    except requests.exceptions.HTTPError as error:
        print(f"HTTP Error: {error}")

    except requests.exceptions.RequestException as error:
        print(f"API Request Error: {error}")

    except ValueError:
        print("Error: Invalid JSON response.")

    return []


def fetch_post_by_id(post_id):
    """Fetch a specific post using its ID."""

    url = f"{API_BASE_URL}{POSTS_ENDPOINT}/{post_id}"

    try:
        response = requests.get(
            url,
            timeout=REQUEST_TIMEOUT
        )

        response.raise_for_status()

        post = response.json()

        print("Post fetched successfully.")

        return post

    except requests.exceptions.RequestException as error:
        print(f"Unable to fetch post: {error}")

    except ValueError:
        print("Error: Invalid JSON response.")

    return None


def display_posts(posts):
    """Display fetched posts."""

    if not posts:
        print("No posts available.")
        return

    print("\n========== API POSTS ==========")

    for post in posts:
        print(f"\nPost ID: {post['id']}")
        print(f"User ID: {post['userId']}")
        print(f"Title: {post['title']}")
        print(f"Body: {post['body']}")

    print("\n================================")


def display_users(users):
    """Display fetched users."""

    if not users:
        print("No users available.")
        return

    print("\n========== API USERS ==========")

    for user in users:
        print(f"\nID: {user['id']}")
        print(f"Name: {user['name']}")
        print(f"Username: {user['username']}")
        print(f"Email: {user['email']}")
        print(f"City: {user['address']['city']}")

    print("\n================================")
