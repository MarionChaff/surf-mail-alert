### surf-mail-alert
Machine learning pipeline for surf condition forecasting, integrating data collection, model training, inference, and automated email alerts.

This pipeline scrapes weather & tide data, trains a model to predict surf conditions, and sends automated alerts when conditions are favorable. 

Key components:
- ml_logic/: core logic for model training (main_train.py), inference (main_infer.py), and daily updates (main_daily.py);
- ml_logic/registry/: handles data loading (datasetloader.py), scraping (tidescraper.py, wgscraper.py), and model storage;
- ml_logic/processing/: preprocessing utilities for feature engineering, scaling, and graph generation;
- ml_logic/modelling/: model building (modelbuilder.py), training (trainer.py), and prediction (predictor.py);
- ml_logic/automation/: handles email notifications for surf alerts.

Dataset contains: 
- swell_height (float): refers to the wave height in meters;
- swell_period (int): refers to the swell period in seconds;
- wind_dir (int): refers to the wind direction in degrees, measured as an angle from north (ranging from 1° to 360°);
- swell_dir (int): refers to the direction from which the swell is coming, measured in degrees from north (ranging from 1° to 360°);
- wind_speed (int): refers to the wind speed in knots, calculated as the average of the constant wind speed and gust speed;
- note (int): 'real-life' weather conditions rating ranging from 0 to 3.
