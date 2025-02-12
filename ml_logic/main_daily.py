from .main_infer import update_forecast, update_tide_forecasts
from .automation.emailnotifier import EmailNotifier
from datetime import datetime
from .params import *
import json

# RUN FROM TERMINAL
# make run_daily_update
# python -m ml_logic.main_daily

def daily_update():

    update_forecast()
    update_tide_forecasts()

    path = os.path.join(TEMP_WF_DIR_PATH, f'forecasts1.json')

    with open(path, 'r') as file:
        forecasts = json.load(file)

    condition = sum(item["note"] for item in forecasts) > 0

    if condition:

        alert = EmailNotifier(SMTP_SERVER, SMTP_PORT, EMAIL_USER, APP_PASSWORD)

        subject = 'Alerte surf !'

        update_day = datetime.today().strftime("%d/%m/%Y, %Hh%M")

        filtered_forecasts = [f for f in forecasts if f["note"] > 0]
        alert_list = ""
        for forecast in filtered_forecasts:
            alert_list += f"- {forecast['day']}. {forecast['number_day']} à {forecast['hour']}h : note {forecast['note']}/3<br>"

        html_body = f"""
        <!DOCTYPE html>
        <html lang="fr">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Alerte surf !</title>
            </head>
            <body>
                <p>Ceci est une alerte importante. Veuillez prendre les dispositions nécessaires.</p>
                <p>Créneaux demain :</p>
                <p>{alert_list}</p>
                <p>Graphique des marées en pièce-jointe</p>
                <p>Date et heure de l'alerte : {update_day}</p>
            </body>
        </html>
        """

        with open(REQUEST_EMAIL_PATH, 'r') as file:
            email_list = json.load(file)

        for email in email_list:
            alert.send_email(email, subject, html_body,image_path = 'temp_files/saved_tide_forecasts/tidegraph1.png')

    return None

if __name__ == '__main__':

    daily_update()
