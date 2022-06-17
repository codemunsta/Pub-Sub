import json
import requests
from .models import Topic, Message, Subscribe
from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework import status


@csrf_exempt
@api_view(['POST'])
def create_topic(request):

    if request.method == 'POST':
        data = request.data
        topic = Topic.objects.create(
            name=data['topic']
        )
        topic.save()
        return JsonResponse({'message': f'new topic {data["topic"]} created'}, status=status.HTTP_200_OK)
    else:
        return JsonResponse({'message': 'method not allowed'}, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(['POST'])
def subscription(request, topic):

    if request.method == 'POST':
        data = request.data
        url = data['url']
        try:
            Tp = Topic.objects.get(name=topic)
        except ObjectDoesNotExist:
            return JsonResponse({'message': 'no topic exist'})
        subscribe = Subscribe.objects.create(
            topic=Tp,
            listener=url
        )
        subscribe.save()
        return JsonResponse({'message': f'subscribed to {topic}'}, status=status.HTTP_200_OK)
    else:
        return JsonResponse({'message': 'method not allowed'}, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(['POST'])
def publish_event(request, params):

    if request.method == 'POST':
        data = request.data
        try:
            Tp = Topic.objects.get(name=params)
            message = Message.objects.create(
                topic=Tp,
                content=data['message']
            )
            message.save()
            subscribers = Subscribe.objects.filter(topic=Tp)
            for subscriber in subscribers:
                url = subscriber.listener
                data = {
                    'message': data['message']
                }
                headers = {
                    'Content-Type': 'application/json'
                }
                response = requests.post(url, headers=headers, data=json.dumps(data))
                return JsonResponse({'message': 'event published'}, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            try:
                subscriber = Subscribe.objects.get(id=int(params))
                Tp = get_object_or_404(Topic, name=subscriber.topic.name)
                message = Message.objects.create(
                    topic=Tp,
                    content=data['message']
                )
                message.save()
                url = subscriber.listener
                data = {
                    'message': data['message']
                }
                headers = {
                    'Content-Type': 'application/json'
                }
                response = requests.post(url, headers=headers, data=json.dumps(data))
                return JsonResponse({'message': 'event published'}, status=status.HTTP_200_OK)
            except ObjectDoesNotExist:
                return JsonResponse({'message': 'no topic or subscriber found'}, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(['POST'])
def listener(request):
    if request.method == 'POST':
        print(request.data)
        return JsonResponse({'message': 'okay'}, status=status.HTTP_200_OK)
