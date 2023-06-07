from django.contrib import admin
from .models import AgentClass, AgentInstance, Tag, AgentRatings

# Register your models here.
admin.site.register((AgentClass, AgentInstance, Tag, AgentRatings,))