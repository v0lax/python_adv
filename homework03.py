from django.conf import settings
from django.core.cache import cache
from django.shortcuts import redirect, render
from django.urls import path

from django.core.validators import URLValidator
from django.core.exceptions import ValidationError


# Задание 3. URL shortener
#
# Реализуйте сервис для сокращения ссылок. Примеры таких сервисов:
# http://bit.ly, http://t.co, http://goo.gl
# Пример ссылки: http://bit.ly/1qJYR0y
#
# Вам понадобится шаблон с формой для отправки ссылки (файл index.html),
# и две функции, одна для обработки запросов GET и POST для сабмита URL
# и отображения результата, и вторая для редиректа с короткого URL на исходный.
# Для хранения соответствий наших коротких ключей и полных URL мы будем
# использовать кеш Django, django.core.cache
# Экземпляр cache уже импортирован, и используется следующим образом.
# Сохранить значение:
#
#  cache.add(key, value)
#
# Извлечь значение:
#
#  cache.get(key, default_value)
#
# Второй аргумент метода get - значение по умолчанию,
# если ключ не найден в кеше.
#
# Вы можете запустить сервер для разработки, и посмотреть
# ответы ваших функций в браузере:
#
# python homework03.py runserver


# Конфигурация, не нужно редактировать
if not settings.configured:
    settings.configure(
        DEBUG=True,
        ROOT_URLCONF=__name__,
        TEMPLATES=[{
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': ['']
        }]
    )


import random, string
def random_key():
    """
    Случайный короткий ключ, состоящий из цифр и букв.
    Минимальная длина ключа - 5 символов. Для генерации случайных
    последовательностей вы можете воспользоваться библиотекой random.
    """
    ln = 5
    chars = string.ascii_letters + string.digits
    rnd = random.SystemRandom()
    return ''.join(rnd.choice(chars) for i in range(ln))

def index(request):
    """
    При запросе методом GET, отдаем HTML страницу (шаблон index.html) с формой
    с одним полем url типа text (отредактируйте шаблон, дополните форму).

    При отправке формы методом POST извлекаем url из request.POST и
    делаем следующее:

    1. Проверяем URL. Допускаются следующие схемы: http, https, ftp

    Если URL не прошел проверку - отобразите на нашей странице с формой
    сообщение о том, какие схемы поддерживаются.

    Если URL прошел проверку:

    2. Создаем случайный короткий ключ, состоящий из цифр и букв
    (функция random_key).

    3. Сохраняем URL в кеш со сгенерированным ключом:

    cache.add(key, url)

    4. Отдаем ту же страницу с формой и дополнительно отображаем на ней
    кликабельную короткую ссылку (HTML тег 'a') вида
    http://localhost:8000/<key>
    """
    key, url = None, None
    cache.add(key, url)


    url = request.POST.get("url")
    err = 'Некорректный URL. Используйте http://, https://, ftp://'

    if url:
        try:
            validate = URLValidator(schemes=('http', 'https', 'ftp',))
            validate(url)

            if cache.get(url):
                key = cache.get(url)

            else:
                key = random_key()
                cache.add(key, url)

            return render(request, 'index.html', {'short_url': 'http://127.0.0.1:8000/' + key})

        
        except ValidationError:
            return render(request, 'index.html', {'msg': err})

    else:
        return render(request, 'index.html')


def redirect_view(request, key):
    """
    Функция обрабатывает сокращенный URL вида http://localhost:8000/<key>
    Ищем ключ в кеше (cache.get). Если ключ не найден,
    редиректим на главную страницу (/). Если найден,
    редиректим на полный URL, сохраненный под данным ключом.
    """

    link = cache.get(key)

    try:
        return redirect(link)
    except:
        return redirect(to='/')


def stats(request, key):
    """
    Статистика кликов на сокращенные ссылки.
    В теле ответа функция возращает количество
    переходов по данному коду.
    """
    pass


urlpatterns = [
    path('', index),
    path(r'stats/<key>', stats),
    path(r'<key>', redirect_view),
]


if __name__ == '__main__':
    import sys
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)
