### IF SAVED ON BQ

from google.oauth2 import service_account
from google.cloud import bigquery
import db_dtypes
import json

class DatasetLoader:

    def __init__(self, bq_path, selected_columns, gcp_credentials_raw):

        self.bq_path = bq_path
        self.selected_columns = selected_columns

        gcp_credentials = json.loads(gcp_credentials_raw)
        gcp_credentials = service_account.Credentials.from_service_account_info(gcp_credentials)
        self.gcp_credentials = gcp_credentials

        self.dataset = self.load()

    def load(self):

        try:
            query = f"""
                SELECT {",".join(self.selected_columns)}
                FROM {self.bq_path}
            """

            client = bigquery.Client(credentials = self.gcp_credentials)
            query_job = client.query(query)
            results = query_job.result()
            dataset = results.to_dataframe()

            print('✅ Dataset loaded')

            return dataset

        except Exception as e:

            print('🚨 Exception occurred while training the model.')
            print(e)

            return None


# IF SAVED LOCALLY

# import pandas as pd

# class DatasetLoader:

#     def __init__(self, path):
#         self.path = path
#         self.dataset = self.import_dataset()

#     def load(self):
#         self.dataset = pd.read_csv(self.path)
#         self.dataset = self.dataset.sample(frac=1, random_state=42).reset_index(drop=True)
#         print("✅ Dataset loaded")
#         return self.dataset
