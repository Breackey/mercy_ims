from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
import json


from .models import CustomUser, Staffs

def staff_profile(request):
	user = CustomUser.objects.get(id=request.user.id)
	staff = Staffs.objects.get(admin=user)

	context={
		"user": user,
		"staff": staff
	}
	return render(request, 'staff_template/staff_profile.html', context)


def staff_profile_update(request):
	if request.method != "POST":
		messages.error(request, "Invalid Method!")
		return redirect('staff_profile')
	else:
		first_name = request.POST.get('first_name')
		last_name = request.POST.get('last_name')
		password = request.POST.get('password')
		address = request.POST.get('address')

		try:
			customuser = CustomUser.objects.get(id=request.user.id)
			customuser.first_name = first_name
			customuser.last_name = last_name
			if password != None and password != "":
				customuser.set_password(password)
			customuser.save()

			staff = Staffs.objects.get(admin=customuser.id)
			staff.address = address
			staff.save()

			messages.success(request, "Profile Updated Successfully")
			return redirect('staff_profile')
		except:
			messages.error(request, "Failed to Update Profile")
			return redirect('staff_profile')
