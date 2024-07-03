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
			'_test.log',
			maxBytes=10240000,
			backupCount=5
		),
		log.StreamHandler()
	],
	format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
	level=Constants.LOG_LEVEL
)


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
	send_email(True)
