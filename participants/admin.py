from django.contrib import admin

from .models import Participant, ValuedItems, Bidding, ResultAuction

# Register your models here.

admin.site.register(Participant)
admin.site.register(ValuedItems)
admin.site.register(Bidding)
admin.site.register(ResultAuction)