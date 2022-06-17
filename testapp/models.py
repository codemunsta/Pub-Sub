from django.db import models


class Topic(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.name}'


class Message(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    content = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.topic.name}'


class Subscribe(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    listener = models.URLField()
