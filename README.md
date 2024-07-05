# website_checker

Checks if givens sites are up and running, and mail notify using a google account (goole cloud needed)

## setup

Python's libraries needed:

```
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
```

Create a google cloud up, turn on gmail api, create an user, obtains credentials.

```credentials.json``` from google console looks like this:

```json
{
	"installed": {
		"client_id": "",
		"project_id": "",
		"auth_uri": "https://accounts.google.com/o/oauth2/auth",
		"token_uri": "https://oauth2.googleapis.com/token",
		"auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
		"client_secret": "",
		"redirect_uris": [
			"http://localhost"
		]
	}
}
```
## config.properties

```
[application]
log.level=info
urls=www.sito.com,www.other.com
# for now, comma in text is not supported!
texts=fool,bar
# wait time (seconds) between website checks
sleep=60
#
mail_from=
mail_to=mail1@gmail.com,mail2@gmail.com
mail_subject_down=down!
mail_body_down=potrebbe essere down!
mail_subject_up=up!
mail_body_up=è tornato up!
```

## TODO

+ multisito
+ log più corti
+ pulizia properties non usate
