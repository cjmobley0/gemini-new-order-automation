import os
import configparser

config = configparser.ConfigParser()

try:
    # For demo purposes, the app_config.cfg has already been attached to this project
    # In a production/staging environment, the cfg file containing api keys and urls
    # should be unique to each person
    config.read(os.path.join(os.getcwd(), '../app_config.cfg'))
    GEMINI_API_KEY = config.get(section='KEYS', option='GEMINI_API_KEY')
    GEMINI_API_SECRET = config.get(section='KEYS', option='GEMINI_API_SECRET')
    GEMINI_BASE_URL = config.get(section='ENV_URL', option='SANDBOX')
except Exception as e:
    print(f"Confirm that api_crendentails.cfg exists in utils\n Error: {e}")
