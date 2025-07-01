from django.contrib import admin
from .models import User, Task, Event, File, Poll, Choice, Vote


# Register your models here.
admin.site.register(User)
admin.site.register(Task)
admin.site.register(Event)
admin.site.register(File)
admin.site.register(Poll)
admin.site.register(Choice)
admin.site.register(Vote)