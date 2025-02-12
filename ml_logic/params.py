import os

##################  VARIABLES  ##################

WG_URL = os.environ.get('WG_URL')

TIDE_URL = os.environ.get('TIDE_URL')

NUM_PREV = 60

NUM_DAYS = 1

TARGET_GCP = False

##################  CONSTANTS  ##################

FEATURE_NAMES_RAW = ['wind_speed','swell_height', 'swell_period', 'wind_dir', 'swell_dir']

TARGET_NAME_RAW = ['note']

TARGET_CATEGORIES_RAW = ['0', '1', '2', '3']

DTYPES_RAW = {
    'wind_speed' : 'int16',
    'swell_height' : 'float16',
    'swell_period' : 'int16',
    'wind_dir' : 'int16',
    'swell_dir' : 'int16',
    'note' : 'int16'
}

##################  PATHS  ##################

LOCAL_MODEL_PATH = os.path.join('ml_model', 'model.pkl')

LOCAL_MODEL_DIR_PATH = os.path.join('ml_model')

TEMP_WF_DIR_PATH = os.path.join('temp_files', 'saved_weather_forecasts')

TEMP_TF_DIR_PATH = os.path.join('temp_files', 'saved_tide_forecasts')

REQUEST_CONDITIONS_PATH = os.path.join('temp_files', 'request_conditions', 'conditions.json')

REQUEST_EMAIL_PATH = os.path.join('temp_files', 'request_emails', 'emails.json')

LOCAL_DATA_PATH = os.path.join('data', 'dataset_rochebonne.csv')

##################  CLOUD  ##################

CREDS_GCP = os.environ.get('CREDS_GCP')

TARGET_GCP = os.environ.get('TARGET_GCP')

BQ_DATASET_PATH = os.environ.get('BQ_DATASET_PATH')

BUCKET_NAME = os.environ.get('BUCKET_NAME')

INSTANCE = os.environ.get('INSTANCE')

##################  PW / KEYS  ##################

# Email alert
SMTP_SERVER = os.environ.get('SMTP_SERVER')
SMTP_PORT = os.environ.get('SMTP_PORT')
EMAIL_USER = os.environ.get('EMAIL_USER')
APP_PASSWORD = os.environ.get('APP_PASSWORD')
