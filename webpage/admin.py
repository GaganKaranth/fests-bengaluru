from django.contrib import admin
from .models import College, Event, Fest, Organizer, Participated

admin.site.register(College)
admin.site.register(Organizer)
admin.site.register(Fest)
admin.site.register(Event)
admin.site.register(Participated)
