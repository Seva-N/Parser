import json
import datetime as d

search = str(input('Запрос: '))
poisk = str(input('Поисковик: '))
file = search + '-' + poisk

y1 = int(input('Год 1: '))
m1 = int(input('Месяц 1: '))
d1 = int(input('Число 1: '))


y2 = int(input('Год 2: '))
m2 = int(input('Месяц 2: '))
d2 = int(input('Число 2: '))

data_1 = str(d.date(y1, m1, d1))
data_2 = str(d.date(y2, m2, d2))
data = str(d.date.today())

file_1 = 'json/' + file + '-' + data_1 + '.json'
file_2 = 'json/' + file + '-' + data_2 + '.json'

file_js = 'Drops/' + file + '-' + 'дроп' + '-' + data + '.json'

with open(file_1, 'r', encoding="utf-8") as file:
	json_1 = json.load(file)

with open(file_2, 'r', encoding="utf-8") as file:
	json_2 = json.load(file)

if len(json_1) <= len(json_2):
	m = len(json_1)
	M = len(json_2)
else:
	m = len(json_2)
	M = len(json_1)

i1 = 0
i2 = 0
Name1 = []
Name2 = []
Drops = []
for item1 in json_1:
	i2 = 0
	Name1.append(item1)
	for item2 in json_2:
		Name2.append(item2)
		if i1 == i2:  
			if Name1 == Name2:
				print(i1, 'True: ', item1)
		#print(item['Name'], ': ', item['Link'])
			else:
				print(i1, 'False:', data_1,' - ', item1['Link'], '; ', data_2,' - ', item2['Link'])
				Drops.append({
					'Site': str(i1), 
					data_1 : item1,
					data_2 : item2
					 })
		Name2 = []
		i2 = i2 + 1
	Name1 = []
	i1 = i1 + 1

with open(file_js, 'w', encoding="utf-8") as file:
	json.dump(Drops, file, indent = 3, ensure_ascii=False)