import os
from google.cloud import storage


os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'gc-api-keys.json'
storage_client = storage.Client()
bucket_name = "vta_qa_model"
destination_directory = os.path.join(os.getcwd(), "vta_qa_model")
model_root_dir =  os.path.abspath('./vta_qa_model')

def ensure_model_local():
    if not os.path.exists(model_root_dir):
        os.makedirs(model_root_dir, exist_ok=True)

        try:
            bucket =  storage_client.bucket( bucket_name)
            blobs = bucket.list_blobs()

            for blob in blobs:
                local_file_path = os.path.join(destination_directory, blob.name)
                local_directory = os.path.dirname(local_file_path)
                if not os.path.exists(local_directory):
                    os.makedirs(local_directory)
                blob.download_to_filename(local_file_path)
                print(f"Downloaded {blob.name} to {local_file_path}")
        except Exception as e:
            print(f"Error downloading model files: {e}")

ensure_model_local()