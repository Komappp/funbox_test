import time

import redis
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from backend.settings import REDIS_HOST, REDIS_PORT

redis_instance = redis.StrictRedis(
        host=REDIS_HOST,
        port=REDIS_PORT, db='test'
    )


class ApiTests(APITestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.url_set = reverse('set_domains')
        cls.url_get = reverse('get_domains')
        cls.data = {
            "links": [
                "https://ya.ru",
                "vk.com",
                "https://pornhub.com/dfdfdf"
            ]
        }

    def test_post_201(self):
        """При пост запросе возвращается код 201"""
        url_set = ApiTests.url_set
        data = ApiTests.data
        response = self.client.post(url_set, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_data_save_to_redis(self):
        """Данные в редис сохраняются корректно"""
        url_set = ApiTests.url_set
        data = ApiTests.data
        since = int(time.time())
        self.client.post(url_set, data, format='json')
        to = int(time.time())
        url_get = ApiTests.url_get + f'?from={since}&to={to}'
        data = self.client.get(url_get).data['domains']
        self.assertTrue('ya.ru' in data)
        self.assertTrue('vk.com' in data)
        self.assertTrue('pornhub.com' in data)

    def test_no_data(self):
        """Если в диапазоне нет данных возвращается код 400"""
        since = 1
        to = 2
        url_get = ApiTests.url_get + f'?from={since}&to={to}'
        response = self.client.get(url_get)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_bad_data(self):
        """Если переданы не валидные данные код 400"""
        url_set = ApiTests.url_set
        data = ''
        response = self.client.post(url_set, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
