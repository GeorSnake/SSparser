


from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from selenium import webdriver
from fake_useragent import UserAgent
from .models import Listing
import re
from django.db import connection
from time import sleep

# Удаляем все существующие записи из модели Listing
Listing.objects.all().delete()
with connection.cursor() as cursor:
    # Сбрасываем последовательность id для модели Listing
    cursor.execute("SELECT setval('parserss_listing_id_seq', 1, false)")

def parse_kartochka_data(kartochka, driver):
    # Создаем объект UserAgent для генерации случайных User-Agent
    useragent = UserAgent()
    options = webdriver.ChromeOptions()
    # Добавляем случайный User-Agent в опции веб-драйвера
    options.add_argument(f"user-agent={useragent.random}")
    driver = webdriver.Chrome(options=options)

    # Находим элемент с заголовком и извлекаем текст
    title = kartochka.find('h2')
    title_text = title.get_text().strip() if title else None

    # Находим элемент с ценой и извлекаем текст
    price_elem = kartochka.find('span', {'class': 'sc-6e54cb25-2 cikpcz listing-detailed-item-price'})
    price = price_elem.get_text().strip() if price_elem else None

    # Находим элемент с адресом и извлекаем текст
    address_elem = kartochka.find('h5', class_='sc-6b97eccb-12 fVwWfz listing-detailed-item-address')
    address = address_elem.get_text().strip() if address_elem else None

    # Находим элемент с полным заголовком и извлекаем текст
    full_title_elem = kartochka.find('p', class_="sc-6e54cb25-16 ijRIAC listing-detailed-item-desc")
    full_title = full_title_elem.get_text().strip() if full_title_elem else None

    # Инициализируем переменные для размера, количества спален и этажа
    size = None
    bedrooms = None
    floor = None

    # Итерируемся по элементам с информацией о квартире
    for y in kartochka.find_all('div', class_="sc-6b97eccb-14 PGhKc"):
        # Ищем элемент с информацией о размере и извлекаем значение
        size_elem = y.find('span', class_="icon-crop_free")
        if size_elem:
            size_text = y.get_text('div').strip()
            size = re.sub(r'[^\d.,]', '', size_text)

        # Ищем элемент с информацией о количестве спален и извлекаем значение
        bedrooms_elem = y.find('span', class_="icon-bed")
        if bedrooms_elem:
            bedrooms_text = y.get_text('div').strip()
            bedrooms = int(bedrooms_text.split()[0])

        # Ищем элемент с информацией об этаже и извлекаем значение
        floor_elem = y.find('span', class_="icon-stairs")
        if floor_elem:
            floor_text = y.get_text('div').strip()
            if ',' in floor_text:
                floor = floor_text.split(',')[0]
            elif '/' in floor_text:
                floor = floor_text.split('/')[0]
            elif '-' in floor_text:
                floor = floor_text
            else:
                floor = floor_text

    # Получаем URL карточки объявления
    kartochka_url = kartochka.get('href')
    full_url = "https://home.ss.ge" + kartochka_url

    # Переходим на страницу объявления
    driver.get(full_url)

    # Инициализируем список для хранения URL изображений
    image_urls = []

    try:
        # Ожидаем появления элемента с классом "lg-react-element"
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "lg-react-element")))
        cards_info = driver.find_element(By.CLASS_NAME, "lg-react-element")
        if cards_info:
            # Находим все элементы с URL изображений
            image_elems = cards_info.find_elements(By.CSS_SELECTOR, 'a[href*=static]')
            for image_elem in image_elems:
                # Получаем URL изображения и добавляем в список
                image_url = image_elem.get_attribute('href')
                image_urls.append(image_url)
    except Exception as e:
        print(f"Ошибка при извлечении ссылок на изображения: {e}")
        print("Попытаемся найти ссылки на изображения еще раз...")
        try:
            # Повторная попытка поиска элементов с URL изображений
            WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "lg-react-element")))
            cards_info = driver.find_element(By.CLASS_NAME, "lg-react-element")
            if cards_info:
                image_elems = cards_info.find_elements(By.CSS_SELECTOR, 'a[href*=static]')
                for image_elem in image_elems:
                    image_url = image_elem.get_attribute('href')
                    image_urls.append(image_url)
        except Exception as e:
            print(f"Не удалось найти ссылки на изображения: {e}")

    # Создаем или обновляем запись в модели Listing
    listing, created = Listing.objects.update_or_create(
        url=full_url,
        defaults={
            'title': title_text,
            'price': price,
            'address': address,
            'full_title': full_title,
            'size': size,
            'bedrooms': bedrooms,
            'floor': floor,
            'image_urls': '\n'.join(image_urls)
        }
    )

    print(f"Ссылки на изображения: {image_urls}")

    # Закрываем веб-драйвер
    driver.quit()

def get_source_html(url, max_retries=3, retry_delay=5):
    # Удаляем все существующие записи из модели Listing
    Listing.objects.all().delete()
    with connection.cursor() as cursor:
        # Сбрасываем последовательность id для модели Listing
        cursor.execute("SELECT setval('parserss_listing_id_seq', 1, false)")

    retry_count = 0
    while retry_count < max_retries:
        try:
            useragent = UserAgent()
            options = webdriver.ChromeOptions()
            options.add_argument(f"user-agent={useragent.random}")
            driver = webdriver.Chrome(options=options)

            # Переходим на указанный URL
            driver.get(url=url)
            wait = WebDriverWait(driver, 10)
            try:
                # Ожидаем появления элемента с классом "sc-20a31af8-3 KgsUg top-grid-lard"
                wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.sc-20a31af8-3.KgsUg.top-grid-lard')))
                break
            except:
                print("Не удалось найти элемент списка после ожидания. Страница может быть недоступна или структура страницы изменилась.")
                raise
        except Exception as _ex:
            print(f"Ошибка при загрузке страницы: {_ex}")
            retry_count += 1
            print(f"Повторная попытка #{retry_count} через {retry_delay} секунд...")
            sleep(retry_delay)
    else:
        print(f"Не удалось загрузить страницу после {max_retries} попыток. Пропускаем эту страницу.")
        driver.quit()
        return

    try:
        # Находим элемент с общим количеством страниц
        total_pages_element = driver.find_element(By.CSS_SELECTOR, '.sc-20a31af8-9.hPbyoG')
        total_pages = int(total_pages_element.text.split('\n')[-1])
        current_page = 1

        while current_page <= total_pages:
            print(f"Текущая страница: {current_page}/{total_pages}")
            # Получаем HTML-код текущей страницы
            soup = BeautifulSoup(driver.page_source, 'lxml')
            # Находим блок с карточками объявлений
            block = soup.find('div', class_="sc-20a31af8-3 KgsUg top-grid-lard")
            if block:
                # Находим все ссылки на объявления
                all_kartochki = block.find_all('a', href=lambda href: href and '/ru/%' in href)

                # Итерируемся по каждой карточке объявления
                for kartochka in all_kartochki:
                    # Парсим данные карточки объявления
                    parse_kartochka_data(kartochka, driver)
            else:
                print(f"Элемент div с классом 'sc-20a31af8-3 KgsUg top-grid-lard' не найден на странице {current_page}. Пропускаем эту страницу.")

            # Переходим на следующую страницу, если текущая не последняя
            if current_page < total_pages:
                next_page_url = url.replace("page=1", f"page={current_page+1}")

                useragent = UserAgent()
                options = webdriver.ChromeOptions()
                options.add_argument(f"user-agent={useragent.random}")
                driver = webdriver.Chrome(options=options)

                # Переходим на следующую страницу
                driver.get(next_page_url)
                # Ожидаем появления элемента с классом "sc-20a31af8-3 KgsUg top-grid-lard"
                wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.sc-20a31af8-3.KgsUg.top-grid-lard')))

            current_page += 1

    except Exception as _ex:
        print(_ex)
    finally:
        # Закрываем веб-драйвер
        driver.quit()