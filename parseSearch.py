import requests
from bs4 import BeautifulSoup
import csv
import datetime as d
import json
import whois
import random
import time


search = str(input('Поиск: '))
data = ' ' + str(d.date.today())

FILE_g = search + ' google' + data + '.csv'
FILE_y = search + ' yandex' + data + '.csv'

FILE_g_js = 'json/' + search + ' google' + data + '.json'
FILE_y_js = 'json/' + search + ' yandex' + data + '.json'

search_ = search.replace(' ', '+')
URL_g = 'https://www.google.com/search?q=' + search_ + '&&start='
URL_y = 'https://www.yandex.ru/search/?clid=2186620&text=' + search_ +'&lr=54&p='
HEADERS = {'user-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:84.0)\
 Gecko/20100101 Firefox/84.0', 'accept': '*/*'}

def get_html(url, headers, params=None):
	r = requests.get(url, headers=headers, params=params)
	return r

def get_content_g(html):
	soup = BeautifulSoup(html, 'html.parser')
	items = soup.find_all('div', class_='yuRUbf')

	posGoogle = [] #словарь
	for item in items:
		link = str(item.find('a').get('href'))
		try:
			if whois.whois(link):
				res = whois.whois(link)
				domain_name = res.domain_name
				registrar = res.registrar

				if isinstance(res.creation_date, d.datetime):
					creation_date = str(res.creation_date)
				else:
					creation_date = str(res.creation_date[0]) + ', ' + str(res.creation_date[1])

				if isinstance(res.expiration_date, d.datetime):
					expiration_date = str(res.expiration_date)
				else:
					expiration_date = str(res.expiration_date[0]) + ', ' + str(res.expiration_date[1])
		except:
			res = 'not'
			domain_name = 'not'
			registrar = 'not'
			creation_date = 'not'
			expiration_date = 'not'

		posGoogle.append({
			'Name': item.find('div', class_='TbwUpd NJjxre').get_text(),
			'Link': item.find('a').get('href'),
			'About': item.find('span').get_text(),
			'Domain_name': domain_name,
			'Registrar': registrar,
			'Creation_date': creation_date,
			'Expiration_date': expiration_date
			})

	return posGoogle

def get_pages_count_g(html):
	soup = BeautifulSoup(html, 'html.parser')
	pagination = soup.find_all('td')
	if pagination:
		if pagination[-2].get_text() == 'среда':
			return pagination[-16].get_text()
		else:
			return pagination[-2].get_text()
	else:
		return 1

def get_content_y(html):
	soup = BeautifulSoup(html, 'html.parser')
	items = soup.find_all('div', class_='organic typo typo_text_m typo_line_s i-bem')

	posYandex = [] #словарь
	for item in items:
		link = str(item.find('a').get('href'))
		try:
			if whois.whois(link):
				res = whois.whois(link)
				domain_name = res.domain_name
				registrar = res.registrar

				if isinstance(res.creation_date, d.datetime):
					creation_date = str(res.creation_date)
				else:
					creation_date = str(res.creation_date[0]) + ', ' + str(res.creation_date[1])

				if isinstance(res.expiration_date, d.datetime):
					expiration_date = str(res.expiration_date)
				else:
					expiration_date = str(res.expiration_date[0]) + ', ' + str(res.expiration_date[1])
		except:
			res = 'not'
			domain_name = 'not'
			registrar = 'not'
			creation_date = 'not'
			expiration_date = 'not'

		t = random.randint(0, 5)
		time.sleep(t)
		
		posYandex.append({
			'Name': item.find('div', class_='organic__path').get_text(),
			'Link': item.find('a').get('href'),
			'About': item.find('div', class_='organic__url-text').get_text(),
			'Domain_name': domain_name,
			'Registrar': registrar,
			'Creation_date': creation_date,
			'Expiration_date': expiration_date
			})
	return posYandex

def get_pages_count_y(html):
	soup = BeautifulSoup(html, 'html.parser')
	pagination = soup.find_all('a', class_='link_theme_none')
	if pagination:
		return pagination[-5].get_text()
	else:
		return 1

def get_pages(html):
	soup = BeautifulSoup(html, 'html.parser')
	pagination = soup.find_all('td')
	if pagination:
		for x in range(0, 10):
			print(pagination[x].get_text())

def save_file(items, path):
	with open(path, 'w', newline='') as file:
		writer = csv.writer(file, delimiter=';')
		writer.writerow(['Cайт', 'Ссылка', 'Описание', 'Имя домина','Сервер регистрации', 'Дата создания', 'Дата завершения'])
		for item in items:
			writer.writerow([item['Name'], item['Link'], item['About'], item['Domain_name'], item['Registrar'], item['Creation_date'], item['Expiration_date']])

def parse_google():
	html_g = get_html(URL_g, HEADERS)
	print(html_g.status_code)
	print('Google: ')
	if html_g.status_code == 200:
		posGoogle = []
		pagGoogle = int(get_pages_count_g(html_g.text))
		URL_gN = ''
		page = 0
		while page < pagGoogle:
			print(f'Парсинг страницы {page+1} из {pagGoogle}...')
			URL_gN = URL_g + str(page)
			html_g = get_html(URL_gN, HEADERS)
			if pagGoogle < 10:
				pagGoogle = int(get_pages_count_g(html_g.text))
			posGoogle.extend(get_content_g(html_g.text))
			page = page + 1
		save_file(posGoogle, FILE_g)
		with open(FILE_g_js, 'w', encoding="utf-8") as file:
			json.dump(posGoogle, file, indent = 3, ensure_ascii=False)

	else:
		print('Error')

def parse_yandex():
	html_y = get_html(URL_y, HEADERS)
	print(html_y.status_code)
	print('Яндекс: ')
	if html_y.status_code == 200:
		posYandex = []
		pagYandex = int(get_pages_count_y(html_y.text))
		URL_yN = ''
		page = 0
		while page < pagYandex:
			print(f'Парсинг страницы {page+1} из {pagYandex}...')
			URL_yN = URL_y + str(page)
			html_y = get_html(URL_yN, HEADERS)
			if pagYandex < 10:
				pagYandex = int(get_pages_count_y(html_y.text))
			posYandex.extend(get_content_y(html_y.text))
			page = page + 1
		save_file(posYandex, FILE_y)
		with open(FILE_y_js, 'w', encoding="utf-8") as file:
			json.dump(posYandex, file, indent = 3, ensure_ascii=False)
	else:
		print('Error')

parse_google()
parse_yandex()