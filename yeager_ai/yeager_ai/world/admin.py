from django.contrib import admin
from .models import WorldClass, Memory, WorldInstance, Event, ObjectClass, ObjectInstance, WorldRatings

# Registered Models
admin.site.register((WorldClass, Memory, WorldInstance,
                    ObjectClass, ObjectInstance, Event, WorldRatings,))
