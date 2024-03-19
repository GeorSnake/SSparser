## Этот проект представляет собой парсер сайта SS.GE для извлечения данных о недвижимости. Он использует Selenium и BeautifulSoup для сбора информации о квартирах, включая заголовок, цену, адрес, описание, размер, количество спален, этаж и ссылки на изображения.

### Требования
- Python 3.x
- Django
- Selenium
- BeautifulSoup
- fake-useragent
- lxml

### Установка
1. Клонируйте репозиторий:

```git clone https://github.com/your-username/ssge-parser.git```

2. Перейдите в каталог проекта:

```cd ssge-parser```

3. Создайте и активируйте виртуальное окружение:

```python -m venv venv```
`source venv/bin/activate`  # для Unix/Linux

`venv\Scripts\activate`  # для Windows

4. Установите зависимости:

```pip install -r requirements.txt```

5. Настройте базу данных:

```python manage.py migrate```

### Использование

1. Запустите парсер:

```python manage.py runscript parser```

2. Парсер начнет сбор данных со страниц сайта SS.GE и сохранять их в базу данных Django.
3. После завершения работы парсера вы можете просмотреть собранные данные в административной панели Django или через API.

## Модель данных

Модель Listing представляет собой объект недвижимости со следующими полями:
- url (URLField): URL объявления
- title (CharField): Заголовок объявления
- price (CharField): Цена квартиры
- address (CharField): Адрес квартиры
- full_title (TextField): Полное описание квартиры
- size (CharField): Размер квартиры
- bedrooms (IntegerField): Количество спален
- floor (CharField): Этаж
- image_urls (TextField): Список URL изображений квартиры

## Веб-драйвер

Для работы парсера требуется веб-драйвер Selenium. По умолчанию используется ChromeDriver. Убедитесь, что у вас установлен Chrome, и путь к ChromeDriver доступен в переменной окружения PATH.

Если вы хотите использовать другой браузер, измените код в файле parser.py, чтобы использовать соответствующий веб-драйвер.
