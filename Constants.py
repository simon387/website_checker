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
#
URLS = config.get(APPLICATION, "urls")
TEXTS = config.get(APPLICATION, "texts")  # for now, comma in text is not supported!
SLEEP = config.get(APPLICATION, "sleep")
#
MAIL_FROM = config.get(APPLICATION, "mail_from")
MAIL_TO = config.get(APPLICATION, "mail_to")
MAIL_SUBJECT_DOWN = config.get(APPLICATION, "mail_subject_down")
MAIL_BODY_DOWN = config.get(APPLICATION, "mail_body_down")
MAIL_SUBJECT_UP = config.get(APPLICATION, "mail_subject_up")
MAIL_BODY_UP = config.get(APPLICATION, "mail_body_up")
