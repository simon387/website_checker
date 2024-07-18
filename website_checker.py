import base64
import logging as log
import os.path
import time
import uuid
from email.mime.text import MIMEText
from email.utils import formatdate
from logging.handlers import RotatingFileHandler

import requests
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from pyrogram import Client

import Constants

log.basicConfig(
	handlers=[
		RotatingFileHandler(
			'_website_checker.log',
			maxBytes=10240000,
			backupCount=5
		),
		log.StreamHandler()
	],
	format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
	level=Constants.LOG_LEVEL
)

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/gmail.send"]


def check_website(url, text, already_down):
	try:
		response = requests.get(url)
		response.raise_for_status()  # Raise an HTTPError for bad responses
		if text in response.text:
			log_message = f"Text '{text}' found on {url}."
			if not already_down:
				log_message += f" Is up or mail already sent"  # mail already sent
			else:
				send_alert(url, False)
			log.info(log_message)
			return False
		else:
			log_message = f"Text '{text}' not found on {url}! WEBSITE MAY BE DOWN!"
			if already_down:
				log_message += f" Email already sent, skipping"  # mail already sent
			else:
				send_alert(url, True)
			log.error(log_message)
			return True
	except requests.exceptions.RequestException as e:
		log.info(f"An error occurred: {e}")
		if already_down:
			log.info(f"Email already sent, skipping")  # mail already sent
		else:
			send_alert(url, already_down)
		return True


def send_alert(url, is_down):
	if Constants.USE_TELEGRAM == 'true':
		log.info(f"Using telegram!")
		send_telegram(url, is_down)
	else:
		log.info(f"Using email!")
		send_email(url, is_down)


def send_email(url, is_down):  # sends an email with the Gmail API.
	creds = None
	# The file token.json stores the user's access and refresh tokens, and is
	# created automatically when the authorization flow completes for the first
	# time.
	if os.path.exists("token.json"):
		creds = Credentials.from_authorized_user_file("token.json", SCOPES)
	# If there are no (valid) credentials available, let the user log in.
	if not creds or not creds.valid:
		if creds and creds.expired and creds.refresh_token:
			creds.refresh(Request())
		else:
			flow = InstalledAppFlow.from_client_secrets_file(
				"credentials.json", SCOPES
			)
			creds = flow.run_local_server(port=0)
		# Save the credentials for the next run
		with open("token.json", "w") as token:
			token.write(creds.to_json())

	try:
		service = build("gmail", "v1", credentials=creds)  # Call the Gmail API
		sender = Constants.MAIL_FROM
		to = Constants.MAIL_TO  # if > 1, comma separate it
		cleaned_url = url.replace("https://", "").replace("www.", "")  # for better email spam control
		if is_down:
			subject = f"{cleaned_url} {Constants.MAIL_SUBJECT_DOWN}"
			message_text = f"{cleaned_url} {Constants.MAIL_BODY_DOWN}"
		else:
			subject = f"{cleaned_url} {Constants.MAIL_SUBJECT_UP}"
			message_text = f"{cleaned_url} {Constants.MAIL_BODY_UP}"

		message = create_message(sender, to, subject, message_text)
		send_message(service, "me", message)
	except HttpError as error:
		log.error(f"An error occurred: {error}")


def create_message(sender, to, subject, message_text):
	message = MIMEText(message_text)
	message['To'] = to
	message['From'] = sender
	message['Subject'] = subject
	message['Date'] = formatdate(localtime=True)
	message['Message-ID'] = f'<{uuid.uuid4()}@gmail.com>'
	raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
	return {'raw': raw}


def send_message(service, user_id, message):
	try:
		message = service.users().messages().send(userId=user_id, body=message).execute()
		log.info(f'Message sent, Id: {message["id"]}')
		return message
	except HttpError as error:
		log.error(f"Can't send the message, an error occurred: {error}")
		return None


def send_telegram(url, is_down):
	if is_down:
		message_text = f"{url} {Constants.MAIL_BODY_DOWN}"
	else:
		message_text = f"{url} {Constants.MAIL_BODY_UP}"
	#
	app = Client("default_session", Constants.API_ID, Constants.API_HASH)
	with app:
		user = app.get_me()
		print(f"Logged in as {user.first_name} (ID: {user.id})")

		# Replace 'me' with your user ID if using bot
		chat_id =  user.id
		# Send the message
		app.send_message("me", "Hello, this is a test message!")
		app.mark_chat_unread("me")
		# app.send_message("me", message_text)
		log.info(f"Message sent using telegram API, text: {message_text}")


if __name__ == '__main__':
	urls = Constants.URLS.split(",")
	texts = Constants.TEXTS.split(",")
	is_server_already_down_array = [False] * len(urls)
	#
	if len(urls) != len(texts):
		log.error("config.properies's data is inconsistent!")
	else:
		while True:
			for i in range(len(urls)):
				is_server_already_down_array[i] = check_website(urls[i], texts[i], is_server_already_down_array[i])
				time.sleep(int(Constants.SLEEP))
