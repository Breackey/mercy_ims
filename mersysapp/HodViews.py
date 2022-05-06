from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
import json

from .models import CustomUser, Staffs, County, Sub_County, Ward, Village


def admin_home(request):
	return render(request, "hod_template/home_content.html")


def add_staff(request):
	return render(request, "hod_template/add_staff_template.html")


def add_staff_save(request):
	if request.method != "POST":
		messages.error(request, "Invalid Method ")
		return redirect('add_staff')
	else:
		first_name = request.POST.get('first_name')
		last_name = request.POST.get('last_name')
		username = request.POST.get('username')
		email = request.POST.get('email')
		password = request.POST.get('password')
		address = request.POST.get('address')

		try:
			user = CustomUser.objects.create_user(username=username,
												password=password,
												email=email,
												first_name=first_name,
												last_name=last_name,
												user_type=2)
			user.staffs.address = address
			user.save()
			messages.success(request, "Staff Added Successfully!")
			return redirect('add_staff')
		except:
			messages.error(request, "Failed to Add Staff!")
			return redirect('add_staff')



def manage_staff(request):
	staffs = Staffs.objects.all()
	context = {
		"staffs": staffs
	}
	return render(request, "hod_template/manage_staff_template.html", context)


def edit_staff(request, staff_id):
	staff = Staffs.objects.get(admin=staff_id)

	context = {
		"staff": staff,
		"id": staff_id
	}
	return render(request, "hod_template/edit_staff_template.html", context)


def edit_staff_save(request):
	if request.method != "POST":
		return HttpResponse("<h2>Method Not Allowed</h2>")
	else:
		staff_id = request.POST.get('staff_id')
		username = request.POST.get('username')
		email = request.POST.get('email')
		first_name = request.POST.get('first_name')
		last_name = request.POST.get('last_name')
		address = request.POST.get('address')

		try:
			# INSERTING into Customuser Model
			user = CustomUser.objects.get(id=staff_id)
			user.first_name = first_name
			user.last_name = last_name
			user.email = email
			user.username = username
			user.save()
			
			# INSERTING into Staff Model
			staff_model = Staffs.objects.get(admin=staff_id)
			staff_model.address = address
			staff_model.save()

			messages.success(request, "Staff Updated Successfully.")
			return redirect('/edit_staff/'+staff_id)

		except:
			messages.error(request, "Failed to Update Staff.")
			return redirect('/edit_staff/'+staff_id)


def delete_staff(request, staff_id):
	staff = Staffs.objects.get(admin=staff_id)
	try:
		staff.delete()
		messages.success(request, "Staff Deleted Successfully.")
		return redirect('manage_staff')
	except:
		messages.error(request, "Failed to Delete Staff.")
		return redirect('manage_staff')

@csrf_exempt
def check_email_exist(request):
	email = request.POST.get("email")
	user_obj = CustomUser.objects.filter(email=email).exists()
	if user_obj:
		return HttpResponse(True)
	else:
		return HttpResponse(False)


@csrf_exempt
def check_username_exist(request):
	username = request.POST.get("username")
	user_obj = CustomUser.objects.filter(username=username).exists()
	if user_obj:
		return HttpResponse(True)
	else:
		return HttpResponse(False)


def admin_profile(request):
	user = CustomUser.objects.get(id=request.user.id)

	context={
		"user": user
	}
	return render(request, 'hod_template/admin_profile.html', context)


def admin_profile_update(request):
	if request.method != "POST":
		messages.error(request, "Invalid Method!")
		return redirect('admin_profile')
	else:
		first_name = request.POST.get('first_name')
		last_name = request.POST.get('last_name')
		password = request.POST.get('password')

		try:
			customuser = CustomUser.objects.get(id=request.user.id)
			customuser.first_name = first_name
			customuser.last_name = last_name
			if password != None and password != "":
				customuser.set_password(password)
			customuser.save()
			messages.success(request, "Profile Updated Successfully")
			return redirect('admin_profile')
		except:
			messages.error(request, "Failed to Update Profile")
			return redirect('admin_profile')
	

def staff_profile(request):
	pass


def add_county(request):
	return render(request, "hod_template/add_county_template.html")

def add_county_save(request):
	return render(request, "hod_template/add_county_template.html")

def manage_county(request):
	return render(request, "hod_template/manage_county_template.html")

def edit_county(request):
	return render(request, "hod_template/edit_county_template.html")

def edit_county_save(request):
	return render(request, "hod_template/edit_county_template.html")

def delete_county(request):
	return render(request, "hod_template/delete_county_template.html")



def add_subcounty(request):
	return render(request, "hod_template/add_subcounty_template.html")

def add_subcounty_save(request):
	return render(request, "hod_template/add_subcounty_template.html")

def manage_subcounty(request):
	return render(request, "hod_template/manage_subcounty_template.html")

def edit_subcounty(request):
	return render(request, "hod_template/edit_subcounty_template.html")

def edit_subcounty_save(request):
	return render(request, "hod_template/edit_subcounty_template.html")

def delete_subcounty(request):
	return render(request, "hod_template/delete_subcounty_template.html")




def add_ward(request):
	return render(request, "hod_template/add_ward_template.html")

def add_ward_save(request):
	return render(request, "hod_template/add_ward_template.html")

def manage_ward(request):
	return render(request, "hod_template/manage_ward_template.html")

def edit_ward(request):
	return render(request, "hod_template/edit_ward_template.html")

def edit_ward_save(request):
	return render(request, "hod_template/edit_ward_template.html")

def delete_ward(request):
	return render(request, "hod_template/delete_ward_template.html")



def add_village(request):
	return render(request, "hod_template/add_village_template.html")

def add_village_save(request):
	return render(request, "hod_template/add_village_template.html")

def manage_village(request):
	return render(request, "hod_template/manage_village_template.html")

def edit_village(request):
	return render(request, "hod_template/edit_village_template.html")

def edit_village_save(request):
	return render(request, "hod_template/edit_village_template.html")

def delete_village(request):
	return render(request, "hod_template/delete_village_template.html")




def add_household(request):
	return render(request, "hod_template/add_household_template.html")

def add_household_save(request):
	return render(request, "hod_template/add_household_template.html")

def manage_household(request):
	return render(request, "hod_template/manage_household_template.html")

def edit_household(request):
	return render(request, "hod_template/edit_household_template.html")

def edit_household_save(request):
	return render(request, "hod_template/edit_household_template.html")

def delete_household(request):
	return render(request, "hod_template/delete_household_template.html")




def add_participant(request):
	return render(request, "hod_template/add_participant_template.html")

def add_participant_save(request):
	return render(request, "hod_template/add_participant_template.html")

def manage_participant(request):
	return render(request, "hod_template/manage_participant_template.html")

def edit_participant(request):
	return render(request, "hod_template/edit_participant_template.html")

def edit_participant_save(request):
	return render(request, "hod_template/edit_participant_template.html")

def delete_participant(request):
	return render(request, "hod_template/delete_participant_template.html")




def add_groups(request):
	return render(request, "hod_template/add_groups_template.html")

def add_groups_save(request):
	return render(request, "hod_template/add_groups_template.html")

def manage_groups(request):
	return render(request, "hod_template/manage_groups_template.html")

def edit_groups(request):
	return render(request, "hod_template/edit_groups_template.html")

def edit_groups_save(request):
	return render(request, "hod_template/edit_groups_template.html")

def delete_groups(request):
	return render(request, "hod_template/delete_groups_template.html")


