		run_train:
			python -c 'from predictions.ml_logic.main_train import train; train()'

		run_update_forecast:
			python -c 'from predictions.ml_logic.main_infer import update_forecast; update_forecast()'

		run_update_tides:
			python -c 'from predictions.ml_logic.main_infer import update_tide_forecasts; update_tide_forecasts()'

		run_update_all: run_update_forecast run_update_tides

		run_all: run_train run_update_all

		run_daily_update:
			python -c 'from predictions.ml_logic.main_daily import daily_update; daily_update()'
