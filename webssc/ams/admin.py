from django.contrib import admin
from ams.models import Phone, Engineer, Publisher, State, Step, Event

class EngineerAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email')
    search_fields = ('first_name', 'last_name')
    filter_horizontal = ('phone',)

class PublisherAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email')
    filter_horizontal = ('phone',)

class StepAdmin(admin.ModelAdmin):
    list_display = ('title', 'state', 'publisher', 'publication_datetime')
    list_filter = ('publication_datetime',)
    ordering = ('-publication_datetime',)
    filter_horizontal = ('engineer',)

class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'state', 'publisher', 'publication_datetime')
    list_filter = ('publication_datetime',)
    ordering = ('-publication_datetime',)
    filter_horizontal = ('engineer', 'step',)

admin.site.register(Phone)
admin.site.register(Engineer, EngineerAdmin)
admin.site.register(Publisher, PublisherAdmin)
admin.site.register(State)
admin.site.register(Step, StepAdmin)
admin.site.register(Event, EventAdmin)
