from django.contrib import admin

# Register your models here.
from deposit.models import *
admin.site.register(Deposit)
admin.site.register(Mydepositlist)