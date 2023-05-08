import requests
import re

MYRIAD_API_BASE_URL = "https://api.myriad.social"
MYRIAD_BASE_URL = "https://app.myriad.social"

# strategy 1 = using search
def get_myriad_post_by_twitter_url(twitter_post_id):
    url = f"{MYRIAD_API_BASE_URL}/search?platform=twitter&referenceId={twitter_post_id}"
    response = requests.get(url)

    if response.status_code == 200:
        json_response = response.json()
        return json_response
    else:
        return None

#strategy 2 = using the id (could only get the user)
def get_myriad_post_by_twitter_url2(twitter_post_id):
    url = f"{MYRIAD_API_BASE_URL}/posts/{twitter_post_id}/importers/twitter"
    response = requests.get(url)

    if response.status_code == 200:
        return response.json()
    elif response.status_code == 404:
        return None
    else:
        raise Exception(f"Unexpected response status code: {response.status_code}")


def extract_twitter_post_id(url):
    post_id = None
    pattern = r"twitter\.com\/(?:\#!\/)?(\w+)\/status(?:es)?\/(\d+)"
    match = re.search(pattern, url)

    if match:
        post_id = match.group(2)

    return post_id


def main():
    while True:
        print("Please enter a Twitter URL (or type 'quit' to exit):")
        url = input().strip()

        if url.lower() == "quit":
            break

        twitter_post_id = extract_twitter_post_id(url)

        if twitter_post_id:
            myriad_post = get_myriad_post_by_twitter_url2(twitter_post_id)

            if myriad_post:
                myriad_post_data = myriad_post['data'][0]
                print(myriad_post_data)
                print(f"Myriad post link: {MYRIAD_BASE_URL}/profile/{myriad_post_data['id']}")
            else:
                print("Post has not been imported.")
        else:
            print("Invalid Twitter URL. Please try again.")

if __name__ == "__main__":
    main()
