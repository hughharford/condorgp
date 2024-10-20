from datetime import datetime
from google.cloud import storage
client = storage.Client()

source_file_path = "diary-entry.txt"
bucket_name = "cgp_dl"

today = datetime.today()
year, month, day = today.strftime("%Y"), today.strftime("%m"), today.strftime("%d")

target_gcs_path = f"datasets/raw/diary-entries/{year}/{month}/{day}/diary-entry.txt"

bucket = client.get_bucket(bucket_name)
blob = bucket.blob(target_gcs_path)
blob.upload_from_filename(source_file_path)
