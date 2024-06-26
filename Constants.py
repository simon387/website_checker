import configparser
import logging

config = configparser.RawConfigParser()
config.read("config.properties")

APPLICATION = "application"
case = config.get(APPLICATION, "log.level")
if case == "info":
	LOG_LEVEL = logging.INFO
elif case == "debug":
	LOG_LEVEL = logging.DEBUG
elif case == "error":
	LOG_LEVEL = logging.ERROR
else:
	LOG_LEVEL = logging.DEBUG

URL = config.get(APPLICATION, "url")
TEXT = config.get(APPLICATION, "text")
SLEEP = config.get(APPLICATION, "sleep")
#
MAIL_APP_NAME = config.get(APPLICATION, "mail_app_name")
MAIL_APP_PASS = config.get(APPLICATION, "mail_app_pass")
#
SMTP_SERVER = config.get(APPLICATION, "smtp_server")
SMTP_PORT = config.get(APPLICATION, "smtp_port")
#
MAIL_FROM = config.get(APPLICATION, "mail_from")
MAIL_TO = config.get(APPLICATION, "mail_to")
MAIL_SUBJECT_DOWN = config.get(APPLICATION, "mail_subject_down")
MAIL_BODY_DOWN = config.get(APPLICATION, "mail_body_down")
MAIL_SUBJECT_UP = config.get(APPLICATION, "mail_subject_up")
MAIL_BODY_UP = config.get(APPLICATION, "mail_body_up")
