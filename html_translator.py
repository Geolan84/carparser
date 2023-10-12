from bs4 import BeautifulSoup
from random import shuffle
import json

def get_car_links(search_text, links, down_limit):
    soup = BeautifulSoup(search_text, 'lxml')
    cars = soup.find_all('div', {"class": 'item-horizontal lots-search'})
    temp = []
    for car in cars:
        try:
            car_link = car.find('div', {'class': 'item-info'}).find('div', {'class': 'item-title'}).find('a').attrs['href']
            temp.append(car_link)
        except:
            continue
    temp = temp[down_limit*50:]
    # Перемешивание ссылок.
    shuffle(temp)
    # Кладём всё в очередь.
    for car in temp:
        links.put(car)



def get_car_info_new(item_text):
    result = []
    soup = BeautifulSoup(item_text, 'lxml')
    # Забор json из текста страницы.
    try:
        car_json = json.loads(str(soup.find_all('script', {'type': 'application/ld+json'})[-1].string))
    except:
        raise Exception('Нет json-представления автомобиля!')
    # Забор заголовка из страницы.
    try:
        title = soup.find('div', class_='header-content item-header')
        car_title_text = title.h1.text.split(',')
    except:
        raise Exception('Ошибка! Заголовок не обнаружен!')

    try:
        # Год, марка+линейка.
        car_year, car_line = car_title_text[0].split(' ', 1)
    except:
        try:
            car_year = car_json['vehicleModelDate']
            car_line = f'{car_json["manufacturer"]} {car_json["model"]}'
        except:
            raise Exception('Нет возможности определить модель авто со страницы!')
    result.extend([car_year, car_line])

    try:
        # Модель.
        car_model = '' if len(car_title_text) <2 else car_title_text[1].strip()
    except:
        car_model = ''
    result.append(car_model)

    try:
        # Аукцион.
        auction = title.a.text
    except:
        auction = ''
    result.append(auction)

    try:
        # VIN.
        car_vin = title.find('span', class_='vin-drop').text
    except:
        try:
            car_vin = car_json['vehicleIdentificationNumber']
        except:
            car_vin = ''
    result.append(car_vin)

    try:
        # Номер лота.
        lot_number = title.find('span', class_='lot-drop').text
    except:
        lot_number = ''
    result.append(lot_number)

    try:
        # Дата аукциона.
        purchace = car_json['purchaseDate']
    except:
        purchace = ''
    result.append(purchace)

    try:
        detitles = ['Убыток', 'Первичное повреждение', 'Вторичное повреждение', 'Одометр', 'Начальный код', 'Ключ']
        details = soup.find('div', {'id': 'condition-details'}).find_all('div', class_='option')
        details.pop()
        res_details = []
        for index in range(len(details)):
            try:
                spec_value = ' '.join(details[index].text.replace(detitles[index], '').split())
            except:
                spec_value = ""
            res_details.append(spec_value)
        res_details.insert(4, '')
        if 'unknown' in res_details[3]:
            res_details[3] = res_details[4] = ''
        else:
            lengths = res_details[3].split('(')
            # Мили, километры.
            res_details[3] = int(''.join(filter(str.isdigit, lengths[0])))
            res_details[4] = int(''.join(filter(str.isdigit, lengths[1])))

        result.extend(res_details)
    except:
        result.extend(['']*7)

    try:
        # Двигатель.
        motor = car_json['vehicleEngine']['name']
    except:
        motor = ''
    result.append(motor)

    try:
        # Последняя ставка.
        car_bid = int(''.join(filter(str.isdigit, soup.find('div', class_='price-archived-item').text)))
    except:
        car_bid = ''
    result.append(car_bid)
    return result
