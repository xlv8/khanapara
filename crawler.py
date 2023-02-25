
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

def crawl_pages(num_pages):
	start = 1
	current_page = start
	end = start + num_pages
	while current_page != end:
		try:
			page_url = BASE_URL + SORT + PAGE + str(current_page) + PAGE_SIZE_URL + str(PAGE_SIZE)
			source_code = requests.get(page_url, headers=headers, timeout=10).text
			soup = BeautifulSoup(source_code, 'html.parser')
			print('crawling page ' + str(current_page) + ': ' + page_url)
			q_no = 0
			for link in soup.find_all('a', {'class': 'question-hyperlink'}):
				if q_no == PAGE_SIZE:
					break
				url = 'http://stackoverflow.com/' + link.get('href')
				title = link.get_text()
				print("------------------------------")
				print(title)
				parse_question(url, title)
				q_no += 1
			current_page += 1
		except (KeyboardInterrupt, EOFError, SystemExit):
			print("\nStopped by user!")
			break