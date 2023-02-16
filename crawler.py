
import os
import requests
from ruamel.yaml import YAML
from bs4 import BeautifulSoup

BASE_URL = 'https://stackoverflow.com/questions/tagged/c'
SORT = '?sort=votes'