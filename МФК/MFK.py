import requests
from bs4 import BeautifulSoup
import csv
import datetime as d
import json
import whois
import random
import time
import re

URL = 'https://lk.msu.ru/course?page='
data = '-' + str(d.date.today())

FILE = 'МФК' + data + '.csv'
FILE_js = 'МФК' + data + '.json'

HEADERS = {'user-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:84.0)\
 Gecko/20100101 Firefox/84.0', 'accept': '*/*'}

def get_html(url, headers, params=None):
	r = requests.get(url, headers=headers, params=params)
	return r

def get_content(html):
	soup = BeautifulSoup(html, 'html.parser')
	items = soup.find_all('div', class_='row')

	course = [] #словарь
	for item in items:
		Name = item.find('a', class_='').get_text()
		Faculty = item.find('small', class_='course-item-faculty').get_text()
		Format = item.find('span', class_='label label-success').get_text()

		Teacher = item.find('div', class_='col-md-3').get_text()
		Teacher = re.sub('\n', '', Teacher)
		Teacher = re.sub('                            ', '', Teacher)
		Teacher = re.sub('Курс читают', '', Teacher)

		About = item.find('p').get_text()
		About = re.sub('\n', '', About)
		About = re.sub('\xa0', '', About)
		About = re.sub('Online-курс', '', About)
		About = re.sub('\r', '', About)
		About = re.sub('                            ', '', About)
		course.append({
			'Name': Name,
			'Faculty': Faculty,
			'Format': Format,
			'Teacher': Teacher,
			'About': About
			})

	return course

def exp(html):
	soup = BeautifulSoup(html, 'html.parser')
	items = soup.find_all('div', class_='row')

	course = [] #словарь
	for item in items:
		Teacher = item.find('div', class_='col-md-3').get_text()
		course.append({
			'Teacher': Teacher
			})
	print(course)

def save_file(items, path):
	with open(path, 'w', newline='') as file:
		writer = csv.writer(file, delimiter=';')
		writer.writerow(['МФК', 'Факультет', 'Формат', 'Курс читают', 'Описание'])
		for item in items:
			writer.writerow([item['Name'], item['Faculty'], item['Format'], item['Teacher'], item['About']])

def parse():
	html = get_html(URL, HEADERS)
	print(html.status_code)
	if html.status_code == 200:
		course = []
		last_page = 8
		URL_N = ''
		page = 1
		while page <= last_page:
			print(f'Парсинг страницы {page} из {last_page}...')
			URL_N = URL + str(page)
			html = get_html(URL_N, HEADERS)
			course.extend(get_content(html.text))
			page = page + 1
		print(course)
		save_file(course, FILE)
		with open(FILE_js, 'w', encoding="utf-8") as file:
			json.dump(course, file, indent = 3, ensure_ascii=False)

	else:
		print('Error')

parse()