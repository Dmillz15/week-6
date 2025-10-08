import requests
import pandas as pd

class Genius:
    def __init__(self, access_token):
        """Initialize the Genius object and store the access token."""
        self.access_token = access_token
        self.base_url = "https://api.genius.com"

    def _get(self, endpoint, params=None):
        """Helper method to make GET requests to the Genius API."""
        headers = {"Authorization": f"Bearer {self.access_token}"}
        response = requests.get(f"{self.base_url}{endpoint}", headers=headers, params=params)
        response.raise_for_status()
        return response.json()

    def search(self, search_term, per_page=10):
        """Search the Genius API for a given term."""
        params = {"q": search_term, "per_page": per_page}
        json_data = self._get("/search", params=params)
        return json_data["response"]["hits"]

    def get_artist(self, search_term):
        """
        Exercise 2:
        Given an artist name, find the primary artist ID from the first hit,
        and return detailed info about that artist.
        """
        hits = self.search(search_term, per_page=1)
        if not hits:
            print(f"No results found for '{search_term}'.")
            return None

        # Extract the primary artist ID
        artist_id = hits[0]["result"]["primary_artist"]["id"]

        # Get artist details from the Genius API
        artist_data = self._get(f"/artists/{artist_id}")
        return artist_data["response"]["artist"]

    def get_artists(self, search_terms):
        """
        Exercise 3:
        Given a list of artist names, return a DataFrame containing:
        - search_term
        - artist_name
        - artist_id
        - followers_count
        """
        data = []
        for term in search_terms:
            artist_info = self.get_artist(term)
            if artist_info:
                data.append({
                    "search_term": term,
                    "artist_name": artist_info.get("name"),
                    "artist_id": artist_info.get("id"),
                    "followers_count": artist_info.get("followers_count", None)
                })
            else:
                data.append({
                    "search_term": term,
                    "artist_name": None,
                    "artist_id": None,
                    "followers_count": None
                })

        return pd.DataFrame(data)
