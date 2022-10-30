import time
import urllib

import redis
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from backend.settings import REDIS_HOST, REDIS_PORT

redis_instance = redis.StrictRedis(
        host=REDIS_HOST,
        port=REDIS_PORT, db=0
    )


def get_bad_request(message):
    return Response({"status": message},
                    status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def set_domains(request):
    """Cохраняет в Redis пару (key, value):
        key - текущее время в Unix
        value - строка с уникальными URL"""
    key = int(time.time())

    try:
        urls_list = request.data['links']
    except KeyError:
        return get_bad_request('В запросе отсутствует ключ links')
    except TypeError:
        return get_bad_request('Передайте данные в JSON формате')

    for i, url in enumerate(urls_list):
        if url.startswith('http'):
            urls_list[i] = urllib.parse.urlsplit(url).netloc
            continue
        urls_list[i] = urllib.parse.urlsplit(url).path

    value = ', '.join(set(urls_list))
    redis_instance.set(key, value)
    response = {
        "status": 'ок'
    }
    return Response(response, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def get_domains(request):
    """При GET запросе проходит циклом по всем возможным ключам за
    заданный промежуток времени, если такие ключи есть - извлекает значение"""
    items = []

    try:
        since = int(request.query_params.get('from'))
        to = int(request.query_params.get('to'))
    except TypeError:
        return get_bad_request('Неверные параметры запроса')
    project_birthday = 1667163944  # время создания проекта
    if since < project_birthday:
        return get_bad_request('Точка from раньше чем 31.10.22')
    for key in range(since, to + 1):
        if redis_instance.get(key):
            items += (str(redis_instance.get(key), 'UTF-8').split(', '))
            continue

    items = list(set(items))
    if items:
        response = {
            'domains': items,
            'status': 'ок'
        }
        return Response(response, status=status.HTTP_200_OK)
    return get_bad_request('Данные отсутствуют, измените диапазон')
