from logging.handlers import RotatingFileHandler

import requests
import time
import logging as log
import Constants

log.basicConfig(
	handlers=[
		RotatingFileHandler(
			'_PersonalTelegramOrganizer.log',
			maxBytes=10240000,
			backupCount=5
		),
		log.StreamHandler()
	],
	format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
	level=Constants.LOG_LEVEL
)


def check_website(url, text):
	try:
		response = requests.get(url)
		response.raise_for_status()  # Raise an HTTPError for bad responses
		if text in response.text:
			log.info(f"The text '{text}' was found on the website. The site is up and running!")
		else:
			log.error(f"The text '{text}' was not found on the website! SITE MAY BE DOWN!")
	except requests.exceptions.RequestException as e:
		log.info(f"An error occurred: {e}")


if __name__ == '__main__':
	while True:
		check_website(Constants.URL, Constants.TEXT)
		time.sleep(60)
