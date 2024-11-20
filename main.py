
from cloudevents.http import CloudEvent
import functions_framework
import random
from googlesheets import JokeSheetHandler
from imageprocessor import JokeImageCreator
from googlestorage import GoogleCloudStorage
from igpublisher import InstagramPublisher

# Triggered from a message on a Cloud Pub/Sub topic.
@functions_framework.cloud_event
def subscribe(cloud_event: CloudEvent) -> None:
   # Print out the data from Pub/Sub, to prove that it worked
   print(
      "Subscribe Works!"
   )

   gcs = GoogleCloudStorage("exclude/storage-credentials.json","dadjokes-haha")
   jokesheet = JokeSheetHandler()
   jokeimagecreator = JokeImageCreator()
   igpub = InstagramPublisher()

   joke, index = jokesheet.get_first_unposted_joke()

   if joke:
      # Now that `joke` is correctly unpacked, you can access it as a dictionary
      hook_text = joke['Hook']
      punchline_text = joke['Punchline']
      
      # Continue processing
      print(f"Found joke with hook: {hook_text} and punchline: {punchline_text}")
   else:
      print("No unposted jokes found.")

   hook_text = joke['Hook']
   punchline_text = joke['Punchline']

   # random number to pick a background
   bg = random.randint(1, 10)
   bg = bg * 2 - 1

   bg_hook_img = f"backgrounds/{bg}.jpg"
   bg_punch_img = f"backgrounds/{bg+1}.jpg" 

   hookimgpath = jokeimagecreator.create_image(hook_text, "/tmp/hook_image.jpg", bg_hook_img )
   punchimgpath = jokeimagecreator.create_image(punchline_text, "/tmp/punchline_image.jpg", bg_punch_img)

   hookblob = f"hook-img-{joke['ID']}.jpg"
   punchblob = f"punchline-img-{joke['ID']}.jpg"

   hookimgpublic = gcs.upload_image(hookimgpath, hookblob)
   punchimgpublic = gcs.upload_image(punchimgpath,punchblob)

   igpub.publish_ig_post(hookimgpublic,punchimgpublic)
   jokesheet.update_posted_date(joke['ID'])
   
   gcs.delete_image(hookblob)
   gcs.delete_image(punchblob)

   return

def mock_cloud_event():
    return {
        "data": {
            "message": {
                "data": "Hello, this is a test message!"
            }
        },
        "context": {
            "event_id": "123456789",
            "timestamp": "2022-10-21T17:32:00.847Z",
            "event_type": "google.pubsub.topic.publish",
            "resource": {
                "service": "pubsub.googleapis.com",
                "name": "projects/sample-project/topics/sample-topic"
            }
        }
    }

if __name__ == "__main__":
   subscribe('')