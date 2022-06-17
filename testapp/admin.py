from django.contrib import admin
from .models import Topic, Subscribe, Message


admin.site.register(Topic)
admin.site.register(Subscribe)
admin.site.register(Message)

# Register your models here.
