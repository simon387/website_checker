import logging as log
import smtplib
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from logging.handlers import RotatingFileHandler

import requests

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


def check_website(url, text, is_down):
	try:
		response = requests.get(url)
		response.raise_for_status()  # Raise an HTTPError for bad responses
		if text in response.text:
			log.info(f"The text '{text}' was found on the website. The site is up and running!")
			if not is_down:
				log.info(f"The server is up or Email already sent, skipping")  # mail already sent
			else:
				send_email(is_down)
			return False
		else:
			log.error(f"The text '{text}' was not found on the website! SITE MAY BE DOWN!")
			if is_down:
				log.info(f"Email already sent, skipping")  # mail already sent
			else:
				send_email(is_down)
			return True
	except requests.exceptions.RequestException as e:
		log.info(f"An error occurred: {e}")


def send_email(is_down):
	msg = MIMEMultipart()
	msg['From'] = Constants.MAIL_FROM
	msg['To'] = Constants.MAIL_TO  # if > 1, comma separate it
	if is_down:
		msg['Subject'] = Constants.MAIL_SUBJECT_DOWN
		msg.attach(MIMEText(Constants.MAIL_BODY_DOWN, 'plain'))
	else:
		msg['Subject'] = Constants.MAIL_SUBJECT_UP
		msg.attach(MIMEText(Constants.MAIL_BODY_UP, 'plain'))

	try:
		server = smtplib.SMTP(Constants.SMTP_SERVER, int(Constants.SMTP_PORT))
		server.starttls()
		server.login(Constants.MAIL_APP_NAME, Constants.MAIL_APP_PASS)
		text = msg.as_string()
		server.sendmail(Constants.MAIL_FROM, Constants.MAIL_TO, text)
		server.quit()
		log.info("Email sent successfully")
	except Exception as e:
		log.error(f"Error on sending email: {e}")


if __name__ == '__main__':
	is_server_down = False
	while True:
		is_server_down = check_website(Constants.URL, Constants.TEXT, is_server_down)
		time.sleep(int(Constants.SLEEP))
