
import os
import requests
from ruamel.yaml import YAML
from bs4 import BeautifulSoup

BASE_URL = 'https://stackoverflow.com/questions/tagged/c'
SORT = '?sort=votes'
PAGE = '&page='
PAGE_SIZE_URL = '&pageSize='

PAGE_SIZE = 15
NUM_ANSWERS = 3

headers = {
	'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'
}