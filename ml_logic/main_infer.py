from .params import *
from .modelling.predictor import Predictor
from .registry.wgscraper import ScraperWg
from .registry.tidescraper import TideScraper
#from .registry.modelstoragemanager import ModelStorageManager
from .processing.graphgenerator import TideGraphGenerator
from datetime import date, datetime, timedelta
import plotly.io as pio
import joblib

# RUN FROM TERMINAL
# make run_update_all
# python -m ml_logic.main_infer

def update_forecast():

    try:

        # Scrape Windguru weather forecast (new X)
        scraper = ScraperWg(WG_URL)
        forecast_df = scraper.scrape(NUM_PREV)

        # Select features (new X)
        X_forecast = forecast_df[FEATURE_NAMES_RAW]

        # Import model
        local_model_path = os.path.join(LOCAL_MODEL_DIR_PATH, 'model.pkl')
        model = joblib.load(local_model_path)
        #storagemanager = ModelStorageManager(BUCKET_NAME, CREDS_GCP, target_gcp = TARGET_GCP)
        #model = storagemanager.load_latest_model(LOCAL_MODEL_DIR_PATH)

        # Predict surf condition
        predictor = Predictor(model)
        y_pred = predictor.predict(X_forecast)['response']
        forecast_df['note'] = y_pred

        update_day = date.today()

        for day_count in range(1,NUM_DAYS+1):
            target_date = update_day + timedelta(days=day_count)
            target_day = int(target_date.day)

            forecast = forecast_df[(forecast_df['number_day'] == target_day)]

            if forecast.empty:
                print(f"No data found for date {target_date}. Skipping JSON creation.")
                continue

            path = os.path.join(TEMP_WF_DIR_PATH, f'forecasts{day_count}.json')
            forecast.to_json(path, orient='records', indent=4)
            print(f"Saved weather forecast for date {target_date} to {path}")

        return None

    except Exception as e:

        # Debugging
        print(f'🚨 Exception occurred during execution: {str(e.__str__)}')

        return None

def update_tide_forecasts(start_hour=7, end_hour=21):

    try:

        # Scrape maree.info for tides
        tidescraper = TideScraper(TIDE_URL)
        tides_x, tides_y = tidescraper.scrape()

        update_day = date.today()

        # Filter tides day per day
        for day_count in range(1,NUM_DAYS+1):

            start_zoom = datetime(update_day.year, update_day.month, update_day.day, start_hour, 0) + timedelta(days = day_count)
            end_zoom = datetime(update_day.year, update_day.month, update_day.day, end_hour, 0) + timedelta(days = day_count)

            filtered_tides_x = [x for x in tides_x if start_zoom <= x <= end_zoom]
            filtered_tides_y = [y for x, y in zip(tides_x, tides_y) if start_zoom <= x <= end_zoom]

            graphgenerator = TideGraphGenerator(filtered_tides_x, filtered_tides_y)

            html_path = os.path.join(TEMP_TF_DIR_PATH, f'tidegraph{day_count}.html')
            with open(html_path, 'w') as f:
                html_graph = pio.to_html(graphgenerator.plot, full_html=False, include_plotlyjs='cdn', config={'displayModeBar': False})
                f.write(html_graph)

            png_path = os.path.join(TEMP_TF_DIR_PATH, f'tidegraph{day_count}.png')
            pio.write_image(graphgenerator.plot, png_path, format="png")

            print(f"Saved tide graph for period {day_count}")

    except Exception as e:

        print(f'🚨 Exception occurred during execution: {str(e.__str__)}')

    return None

if __name__ == '__main__':

    update_forecast()
    update_tide_forecasts()
