from unittest import result
import requests

def query_unsplash(query, api_key):
    API_ENDPOINT = "https://api.unsplash.com/search/photos?page=1&orientation=landscape&query="
    results = requests.get(API_ENDPOINT + query, headers={"Authorization": f"Client-ID {api_key}"}).json()
    if 'errors' in results:
        return None
    return results['results']

def get_image_by_query(query, api_key):
    results = query_unsplash(query, api_key)
    return results[0]['urls']['regular']
