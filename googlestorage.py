from google.cloud import storage
import os

class GoogleCloudStorage:
    def __init__(self, credentials_path, bucket_name):
        # Set up credentials
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path

        # Initialize the storage client
        self.storage_client = storage.Client()

        # Get the bucket
        self.bucket = self.storage_client.bucket(bucket_name)
    
    def upload_image(self, source_file_name, destination_blob_name):
        # Create a blob in the bucket (this represents the object in the bucket)
        blob = self.bucket.blob(destination_blob_name)

        # Upload the file to the blob
        blob.upload_from_filename(source_file_name)

        # Print the public URL
        public_url = blob.public_url
        print(f"File {source_file_name} uploaded to {destination_blob_name} and available at {public_url}")

        return public_url

    def delete_image(self, blob_name):
        # Get the blob from the bucket
        blob = self.bucket.blob(blob_name)

        # Delete the blob
        blob.delete()

        # Print confirmation
        print(f"File {blob_name} deleted from bucket {self.bucket.name}")

# Example usage:
if __name__ == "__main__":
    # Initialize the GoogleCloudStorage class
    credentials_path = "exclude/storage-credentials.json"
    bucket_name = "dadjokes-haha"
    
    gcs = GoogleCloudStorage(credentials_path, bucket_name)

    # Upload an image
    source_file = "backgrounds/1.jpg"
    destination_blob = "/tmp/hook_image_1.jpg"
    gcs.upload_image(source_file, destination_blob)

    # Delete an image
    gcs.delete_image(destination_blob)
