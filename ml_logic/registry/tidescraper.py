import numpy as np
from datetime import datetime, date
import calendar
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.common.exceptions import TimeoutException

class TideScraper:

    def __init__(self, url):
        self.url = url
        self.driver = webdriver.Chrome()
        self.driver.get(self.url)

    def scrape(self):

        # Wait for the page to load before scraping
        try:
            myElem = WebDriverWait(self.driver, 5).until(expected_conditions.presence_of_element_located((By.XPATH, '//*[@id="MareeJours_0"]/th/a')))
        except TimeoutException:
            None

        # Store the scaped items
        slack_tides = []
        tide_x = []
        tide_y = []

        # Current date, to infer month and year later
        current_date = datetime.now()
        current_year = current_date.year
        current_month = current_date.month
        nb_days_in_current_month = calendar.monthrange(current_year, current_month)[1]

        try:

            # Extract dates in datetime format - scrape one additional day to get a full period

            day_list = ['//*[@id="MareeJours_0"]/th/a', '//*[@id="MareeJours_1"]/th/a', '//*[@id="MareeJours_2"]/th/a', '//*[@id="MareeJours_3"]/th/a', '//*[@id="MareeJours_4"]/th/a', '//*[@id="MareeJours_5"]/th/a', '//*[@id="MareeJours_6"]/th/a']
            times_list = ['//*[@id="MareeJours_0"]/td[1]', '//*[@id="MareeJours_1"]/td[1]', '//*[@id="MareeJours_2"]/td[1]', '//*[@id="MareeJours_3"]/td[1]', '//*[@id="MareeJours_4"]/td[1]', '//*[@id="MareeJours_5"]/td[1]', '//*[@id="MareeJours_6"]/td[1]']
            levels_list = ['//*[@id="MareeJours_0"]/td[2]', '//*[@id="MareeJours_1"]/td[2]', '//*[@id="MareeJours_2"]/td[2]', '//*[@id="MareeJours_3"]/td[2]', '//*[@id="MareeJours_4"]/td[2]', '//*[@id="MareeJours_5"]/td[2]', '//*[@id="MareeJours_6"]/td[2]']

            for day_xpath, times_xpath, levels_xpath in zip(day_list, times_list, levels_list):

                # scrap the dates
                date_element = self.driver.find_element(By.XPATH, day_xpath)
                parsed_day = int(date_element.text.split('\n')[1])
                parsed_date = date(current_year, current_month, parsed_day)

                # scrap the times
                time_element = self.driver.find_element(By.XPATH, times_xpath)
                time_list = time_element.text.split('\n')

                # scrap the respective tide levels
                tide_element = self.driver.find_element(By.XPATH, levels_xpath)
                tide_list = tide_element.text.split('\n')

                for time, tide in zip(time_list, tide_list):
                    parsed_time = datetime.strptime(time, '%Hh%M').time()
                    combined_datetime = datetime.combine(parsed_date, parsed_time)
                    tide_level = float(tide.strip('m').replace(',','.'))
                    slack_tides.append((combined_datetime, tide_level))

                # change the current month and current year if relevant
                if parsed_day == nb_days_in_current_month:
                    current_month = current_month % 12 + 1
                    if current_month == 1:
                        current_year += 1

            for k in range(0,len(slack_tides)-1):

                start_timestamp = slack_tides[k][0].timestamp()
                end_timestamp = slack_tides[k+1][0].timestamp()

                start_tide_level = slack_tides[k][1]
                end_tide_level = slack_tides[k+1][1]

                x_values = np.arange(start_timestamp, end_timestamp, 60)
                x_values_datetime = [datetime.fromtimestamp(ts) for ts in x_values]

                amplitude = (end_tide_level - start_tide_level) / 2
                frequency = np.pi / (start_timestamp - end_timestamp)

                y_values = start_tide_level + amplitude * (1 + np.sin(frequency * (x_values - start_timestamp) - np.pi / 2))

                tide_x.extend(x_values_datetime[:-1]) # don't count the high/low tide value twice
                tide_y.extend(y_values[:-1])

            print("✅ Tides scraped")

        except Exception as e:
            print('Exception occurred during scraping')
            print(e)

        return tide_x, tide_y
