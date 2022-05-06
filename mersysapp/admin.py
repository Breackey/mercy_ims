from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, AdminHOD, Staffs, County, Sub_County, Village, Ward, Participant, Groups, HouseHold 

# Register your models here.
class UserModel(UserAdmin):
	pass


admin.site.register(CustomUser, UserModel)

admin.site.register(AdminHOD)
admin.site.register(Staffs)
admin.site.register(County)
admin.site.register(Sub_County)
admin.site.register(Village)
admin.site.register(Ward)
admin.site.register(Participant)
admin.site.register(Groups)
admin.site.register(HouseHold)
