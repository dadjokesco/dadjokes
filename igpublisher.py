import requests
import json

def get_instagram_token(token_file_path):
    with open(token_file_path, 'r') as file:
        data = json.load(file)
    return data.get("token")

class InstagramPublisher:
    def __init__(self, 
                 access_token=get_instagram_token('exclude/igtoken.json'), 
                 user_id='17841470194015758'):
        self.access_token = access_token
        self.user_id = user_id

    def __create_media(self, image_url):
        response = requests.post(
            f'https://graph.facebook.com/v16.0/{self.user_id}/media',
            params={
                'image_url': image_url,
                'access_token': self.access_token
            }
        )
        response_data = response.json()
        media_id = response_data.get('id')

        if not media_id:
            print(f"Error creating media object for {image_url}: {response_data}")
            return None
        return media_id

    def __create_carousel(self, hook_media_id, punchline_media_id):
        response = requests.post(
            f'https://graph.facebook.com/v16.0/{self.user_id}/media',
            params={
                'media_type': 'CAROUSEL',
                'children': f'{hook_media_id},{punchline_media_id}',
                'access_token': self.access_token
            }
        )
        response_data = response.json()
        carousel_media_id = response_data.get('id')

        if not carousel_media_id:
            print(f"Error creating carousel container: {response_data}")
            return None
        return carousel_media_id

    def __publish_post(self, carousel_media_id):
        response = requests.post(
            f'https://graph.facebook.com/v16.0/{self.user_id}/media_publish',
            params={
                'creation_id': carousel_media_id,
                'access_token': self.access_token
            }
        )
        response_data = response.json()

        if 'id' in response_data:
            print(f"Post published successfully with ID: {response_data['id']}")
            return response_data['id']
        else:
            print(f"Error publishing post: {response_data}")
            return None

    def publish_ig_post(self, hook_img_url, punchline_img_url):
        # Create media objects for the hook and punchline images
        hook_media_id = self.__create_media(hook_img_url)
        punchline_media_id = self.__create_media(punchline_img_url)

        # Check if both media objects were created successfully
        if not hook_media_id or not punchline_media_id:
            print("Error creating media objects. Exiting.")
            return

        # Create Carousel Container
        carousel_media_id = self.__create_carousel(hook_media_id, punchline_media_id)
        if not carousel_media_id:
            print("Error creating carousel container. Exiting.")
            return

        # Publish Carousel Post
        self.__publish_post(carousel_media_id)


# Example usage
if __name__ == "__main__":
    ACCESS_TOKEN = 'EAAX67n8g3UQBO2VmlioIikHPhScjpzvwQPZBjBwZCsJPPPIxB6x9Ooted1bM9YVCK21ISNL5mVFyDYEWl5Rlr5Rzwp5P9U7B4icZBKFZCjwgmw52ItPFa32oZCdGp6ZAtN2Lo7MRon1AYd3WJ1zjGH0K92sglAhIlSDbjSln071GI0c19l1gAqizcIgiyt5aIoASYU1AZDZD'
    INSTAGRAM_USER_ID = '17841470194015758'

    # Initialize the InstagramPublisher class
    instagram_publisher = InstagramPublisher(ACCESS_TOKEN, INSTAGRAM_USER_ID)

    # URLs of the images for hook and punchline
    hook_img_url = 'https://example.com/hook_image.jpg'
    punchline_img_url = 'https://example.com/punchline_image.jpg'

    # Publish the Instagram post
    instagram_publisher.publish_ig_post(hook_img_url, punchline_img_url)
