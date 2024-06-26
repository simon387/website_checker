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
