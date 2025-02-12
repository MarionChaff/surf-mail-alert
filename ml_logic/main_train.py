from .params import *
from .registry.datasetloader import DatasetLoader
#from .registry.modelstoragemanager import ModelStorageManager
from .processing.splitter import Splitter
from .modelling.modelbuilder import ModelBuilder
from .modelling.trainer import Trainer
import joblib

# RUN FROM TERMINAL
# python -m ml_logic.main_train
# make run_train

def train():

    try:

        # Get data
        loader = DatasetLoader(bq_path = BQ_DATASET_PATH, selected_columns = FEATURE_NAMES_RAW + TARGET_NAME_RAW, gcp_credentials_raw = CREDS_GCP)
        #loader = DatasetLoader(path = LOCAL_DATA_PATH)
        dataset = loader.dataset
        dataset = dataset.astype(DTYPES_RAW)

        # Split dataset
        splitter = Splitter(features = FEATURE_NAMES_RAW, target = TARGET_NAME_RAW)
        X_train, X_test, y_train, y_test = splitter.create_train_and_test_set(dataset)

        # Define model
        modelbuilder = ModelBuilder()
        model = modelbuilder.build_model()

        # Train model
        trainer = Trainer(model, target_categories = TARGET_CATEGORIES_RAW)
        model = trainer.fit_and_score(X_train, X_test, y_train, y_test)

        # Save model
        local_model_path = os.path.join(LOCAL_MODEL_DIR_PATH, 'model.pkl')

        try:
            joblib.dump(model, local_model_path)
            print('✅ Model saved locally')
        except Exception:
            print('🚨 Error saving the model locally')

        return None

    except Exception as e:

        # Debugging
        print(f'🚨 Exception occurred during execution: {str(e.__str__)}')

        return None


if __name__ == '__main__':

    train()
