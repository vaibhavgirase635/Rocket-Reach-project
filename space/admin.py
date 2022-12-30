from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(User_Profile)

admin.site.register(CustomUser)

admin.site.register(Tokens)

admin.site.register(Contacts)

admin.site.register(Pricing_Plan)

admin.site.register(Purchased_Subcription)