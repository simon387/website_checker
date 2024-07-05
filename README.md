# website_checker

## setup

```
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
```

```credentials.json``` from google console:

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
url=www.sito.com
text=
sleep=60
#
mail_app_name=website_checker
mail_app_pass=
#
smtp_server=smtp.gmail.com
smtp_port=587
#
mail_from=
mail_to=
mail_subject_down=sito.com down!
mail_body_down=Il sito sito.com di prod potrebbe essere down!
mail_subject_up=sito.com up!
mail_body_up=Il sito sito.com di prod è tornato up!
```

## TODO

+ multisito
