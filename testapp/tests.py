from rest_framework.test import APITestCase
from rest_framework import status
from .models import Topic, Subscribe


class TestURLs(APITestCase):

    def test_create_topic(self):
        url = '/create/topic/'
        data = {
            'topic': 'topic'
        }
        response = self.client.post(path=url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def create_topic(self):
        self.topic = Topic.objects.create(name='Topic')
        return self.topic

    def test_subscription(self):
        self.create_topic()
        url = f'/subscribe/topic/'
        data = {
            'url': 'http://localhost:8000/event'
        }
        response = self.client.post(path=url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_publish_event(self):
        topic = self.create_topic()
        subscriber = Subscribe.objects.create(topic=topic, listener='http://localhost:8000/event')
        subscriber.save()
        url = f'/publish/Topic/'
        data = {
            'message': 'hello world'
        }
        response = self.client.post(path=url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_listener(self):
        url = '/event/'
        response = self.client.post(path=url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
