import sys
import time
import shutil
import logging
import random
import datetime
import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showwarning
from queue import Empty, Queue
from threading import Thread, Lock

import html_translator, writer
from driver_gen import get_chromedriver
from fake_generator import FakeGenerator;
from pages.login_page import LoginPage
from pages.search_page import SearchPage
from pages.item_page import ItemPage

LOGIN_PAGE = 'https://bid.cars/ru/login'
FAKE = FakeGenerator()

TITLES = ['Ссылка', 'Год авто', 'Линейка', 'Модель',
          'Аукцион', 'VIN', 'Номер лота', 'Дата покупки',
          'Убыток', 'Первичное повреждение', 'Вторичное повреждение',
          'Мили', 'Километраж', 'Начальный код', 'Ключ', 'Двигатель', 'Цена', 'IP']

def parse_search(link: str, down_limit: int, up_limit):
    links = Queue()
    cars = Queue()
    # Get links from search page.
    try:
        driver, _ = get_chromedriver(number=1, fake=FAKE)
        search = SearchPage(driver, link)
        text = search.search(up_limit)
        html_translator.get_car_links(text, links, down_limit)
    except Exception as e:
        logging.error('Возникла ошибка получения ссылок: %s', str(e))
    finally:
        driver.quit()
        shutil.rmtree('pluginfile1')

    logging.info("Обнаружено %i ссылок.", links.qsize())
    lock = Lock()
    # Process links by two threads.
    try:
        while not links.empty():
            first_thread = Thread(target=parse_links, args=(1, links, cars, lock, *FAKE.get_new_profile()))
            first_thread.start()
            logging.info('1 thread started')
            if links.qsize() >= 14: #14:
                second_thread = Thread(target=parse_links, args=(2, links, cars, lock, *FAKE.get_new_profile()))
                second_thread.start()
                logging.info('2 thread started')
                second_thread.join()
                logging.info('2 thread joined')     
            first_thread.join()
            logging.info('1 thread joined')
            # logging.info('Осталось %i ссылок', links.qsize())
    except Exception as e:
        logging.error('Возникла ошибка %s', str(e))
    finally:
        if cars.qsize() > 0:
            logging.info("Должно быть записано %i ссылок.", cars.qsize())
            add_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S').replace(':', '-')
            writer.write_to_xlsx(f'carpet{add_time.replace(" ", "-")}', TITLES, cars)
            


def parse_links(number: int, links: Queue, result: Queue, lock: Lock, login, password):
    lock.acquire()
    try:
        driver, ip = get_chromedriver(number=number, fake=FAKE)
    finally:
        lock.release()
    try:
        # Авторизация.
        logging.info('Thread %s with email=%s and password=%s created.', str(number), login, password)
        authorization = LoginPage(driver, LOGIN_PAGE)
        authorization.login(login, password)
        time.sleep(random.randrange(20, 40))
        if driver.current_url not in {'https://bid.cars/ru/user/increase-power', 'https://bid.cars/ru/'}:
            logging.error('У потока %s не произошёл редирект на главную страницу, закрытие...', str(number))
            return
        portion_size = random.randrange(25, 30)
        for _ in range(portion_size):
            try:
                new_link = links.get(timeout=3)
            except Empty:
                break
            try:
                car_page = ItemPage(driver, new_link)
                car_text = car_page.get_info()
                car = html_translator.get_car_info_new(car_text)
                car.insert(0, new_link)
                car.append(ip)
                result.put(car)
                links.task_done()
                logging.info('Thread with email=%s parsed: %s. Осталось %s ссылок.', login, str(car), str(links.qsize()))
            except Exception as e:
                logging.error('Error in parse_links process: %s', str(e))
                break
    finally:
        driver.quit()
        shutil.rmtree(f'pluginfile{number}')

if __name__ == "__main__":
    # Логгер.
    full = logging.getLogger()
    formatter = logging.Formatter("%(asctime)s;%(levelname)s;%(message)s")
    full.setLevel(logging.INFO)
    file_cache = logging.FileHandler('cache.log')
    file_cache.setFormatter(formatter)
    full.addHandler(file_cache)
    console_handler = logging.StreamHandler(sys.stdout)
    full.addHandler(console_handler)
    # Графическое окно программы.
    window = tk.Tk()
    window.title("CarParser v1.0")
    window.resizable(False, False)
    window.geometry('800x300')
    frame = tk.Frame(window, padx=10, pady=10)
    frame.pack(expand=True)
    
    link_label = tk.Label(frame, text="Ссылка: ")
    link_label.grid(row=3, column=1)
    link_input = tk.Entry(frame)
    link_input.grid(row=3, column=2, pady=5)
    combo = ttk.Combobox(frame, state="readonly", values=[x for x in range(1, 11)], width=3)
    combo.current(0)
    combo.grid(row=3, column=3, pady=1)
    combo2 = ttk.Combobox(frame, state="readonly", values=[x for x in range(1, 11)], width=3)
    combo2.current(0)
    combo2.grid(row=3, column=4, pady=1)

    def save_event():
        link = link_input.get()
        if link == '':
            showwarning(title="Предупреждение", message="Вставь ссылку!")
        elif int(combo.get()) > int(combo2.get()):
            showwarning(title="Предупреждение", message="Верхний лимит >= нижнему!")
        else:
            link_input.delete(0, tk.END)
            try:
                parse_search(link, int(combo.get())-1, int(combo2.get())-1)
            except Exception as e:
                logging.error('Handled error in form call: %s', str(e))
                showwarning(title='Ошибка!', message=str(e))

    cal_btn = tk.Button(frame, text='Скачать', command=save_event)
    cal_btn.grid(row=5, column=2)
    window.mainloop()
