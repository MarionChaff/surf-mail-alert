from google.oauth2 import service_account
from google.cloud import storage
import joblib
import time
import json
import glob
import os

# python -m predictions.ml_logic.registry.modelstoragemanager

class ModelStorageManager:

    def __init__(self, bucket_name, gcp_credentials_raw, target_gcp):

        self.bucket_name = bucket_name
        self.target_gcp = target_gcp

        if target_gcp:
            gcp_credentials_raw = json.loads(gcp_credentials_raw)
            gcp_credentials = service_account.Credentials.from_service_account_info(gcp_credentials_raw)
            client = storage.Client(credentials=gcp_credentials)
            self.bucket = client.bucket(self.bucket_name)

    def save_model(self, model, local_model_dir):

        """
        Save a machine learning model to a local directory and optionally
        (if target_gcp set to True) to Google Cloud Storage (GCS).
        """

        local_model_path = os.path.join(local_model_dir, 'model.pkl')
        #local_model_path = os.path.join(local_model_dir, filename)

        try:
            joblib.dump(model, local_model_path)
            print('✅ Model saved locally')
        except Exception:
            print('🚨 Error saving the model locally')

        if self.target_gcp:
            try:
                timestamp = time.strftime("%Y%m%d-%H%M")
                filename = f'model_{timestamp}.pkl' # Only for GCP
                blob = self.bucket.blob(f'model/{filename}')
                blob.upload_from_filename(local_model_path)
                print('✅ Model saved to GCS')
            except Exception:
                print('🚨 Error saving the model to GCS')

        return None

    def load_latest_model(self, local_model_dir):

        """
        Download and save the latest machine learning model from either Google
        Cloud Storage (GCS) or a local directory.
        """

        print(self.target_gcp)

        if self.target_gcp:

            try:
                print('ca simprime')
                blobs = list(self.bucket.list_blobs(prefix='model/model'))
                latest_blob = max(blobs, key=lambda x: x.updated)
                latest_model_path_to_save = os.path.join(local_model_dir, 'model.pkl')
                latest_blob.download_to_filename(latest_model_path_to_save)
                model = joblib.load(latest_model_path_to_save)
                print('✅ Latest model downloaded from GCP')
                return model

            except Exception:
                print('🚨 Error loading the model from GCP')
                return None

        else:
            try:
                local_model_paths = glob.glob(f"{local_model_dir}/*")
                if not local_model_paths:
                    print('🚨 Model not found locally')
                    return None
                most_recent_local_model_path = sorted(local_model_paths)[-1]
                model = joblib.load(most_recent_local_model_path)
                print('✅ Model uploaded locally')
                return model

            except Exception:
                print('🚨 Error loading the model locally')
                return None
