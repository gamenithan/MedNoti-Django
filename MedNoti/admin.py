from django.contrib import admin
from django.apps import apps
from MedNoti.models import Profile, Medicine, Neighbor, Calendar, Schedule
from django.contrib.auth.models import Permission, User

# Register your models here.
# Register your models here.
class Profileadmin(admin.ModelAdmin):
    list_display = ['id']
    list_per_page = 15
#   list_display = ['id', 'question', 'text', 'value']
#     list_per_page = 15
class Medicineadmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    list_per_page = 15 

    # fieldsets = [
    #     (None, {'fields': ['name', 'rating']}),
    #     ("Active Duration", {'fields': ['release_date'], 'classes': ['collapse']})
    # ]


class Neighboradmin(admin.ModelAdmin):
    list_display = ['id', 'user_id_id', 'first_name']
    list_per_page = 15

#   list_display = ['id', 'question', 'text', 'value']
#     list_per_page = 15

try:
    admin.site.register(Permission)
    admin.site.register(Profile, Profileadmin)
    admin.site.register(Medicine,Medicineadmin)
    admin.site.register(Neighbor,Neighboradmin)
    admin.site.register(Calendar)
    admin.site.register(Schedule)
except Exception:
    pass
