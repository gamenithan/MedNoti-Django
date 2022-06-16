from builtins import object
from datetime import datetime
from itertools import count

from dateutil.parser import parse
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import (login_required,
                                            permission_required,
                                            user_passes_test)
from django.contrib.auth.models import Group, User
from django.contrib.auth.signals import user_logged_in
from django.core.files.storage import FileSystemStorage
from django.core.mail import send_mail
from django.forms import formset_factory
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import get_list_or_404, redirect, render
from django.template.context_processors import request
from pkg_resources import require

from MedNoti.models import Calendar, Medicine, Neighbor, Profile, Schedule

from .forms import ContactForm


def email(request):
    subject = 'testSendEmail'
    message = ' it  means a world to us '
    email_from = settings.EMAIL_HOST_USER
    recipient_list = ['game-pp@hotmail.com']
    send_mail( subject, message, email_from, recipient_list )
    return redirect('login')

def my_login(request):
    logout(request)
    context = {}
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            next_url = request.POST.get('next_url')
            if next_url:
                return redirect(next_url)
            else:
                meds = Medicine.objects.filter(user_id_id=user.id)
                for med in meds:
                    if med.freq1 == "เช้า":
                        if datetime.now() > datetime(datetime.now().year, datetime.now().month, datetime.now().day, 6, 00) and datetime.now() < datetime(datetime.now().year, datetime.now().month, datetime.now().day, 10, 00):
                            subject = 'คุณ'+med.who+'อย่าลืมกินยา'+med.name+'ตอนเช้านะจ๊ะ'
                            message = med.when
                            email_from = settings.EMAIL_HOST_USER
                            recipient_list = [user.email]
                            send_mail( subject, message, email_from, recipient_list )
                    if med.freq2 == "กลางวัน":
                        if datetime.now() > datetime(datetime.now().year, datetime.now().month, datetime.now().day, 12, 00) and datetime.now() < datetime(datetime.now().year, datetime.now().month, datetime.now().day, 14, 00):
                            subject = 'คุณ'+med.who+'อย่าลืมกินยา'+med.name+'ตอนกลางนะจ๊ะ'
                            message = med.when
                            email_from = settings.EMAIL_HOST_USER
                            recipient_list = [user.email]
                            send_mail( subject, message, email_from, recipient_list )
                    if med.freq3 == "เย็น":
                        if datetime.now() > datetime(datetime.now().year, datetime.now().month, datetime.now().day, 16, 00) and datetime.now() < datetime(datetime.now().year, datetime.now().month, datetime.now().day, 18, 00):
                            subject = 'คุณ'+med.who+'อย่าลืมกินยา'+med.name+'ตอนเย็นนะจ๊ะ'
                            message = med.when
                            email_from = settings.EMAIL_HOST_USER
                            recipient_list = [user.email]
                            send_mail( subject, message, email_from, recipient_list )
                    if med.freq4 == "ก่อนนอน":
                        if datetime.now() > datetime(datetime.now().year, datetime.now().month, datetime.now().day, 20, 00) and datetime.now() < datetime(datetime.now().year, datetime.now().month, datetime.now().day, 22, 00):
                            subject = 'คุณ'+med.who+'ก่อนอนอย่าลืมกินยา'+med.name+'นะจ๊ะ'
                            message = med.when
                            email_from = settings.EMAIL_HOST_USER
                            recipient_list = [user.email]
                            send_mail( subject, message, email_from, recipient_list )
                return redirect('createprofile')
        else:   
            context['username'] = username
            context['password'] = password
            context['error'] = "Wrong username or password!"
    next_url = request.GET.get('next')
    if next_url:
        context['next_url'] = next_url
    return render(request, template_name='login.html', context=context)

@login_required
def my_logout(request):
    logout(request)
    return redirect('login')

def my_regis(request):
    logout(request)
    context = {}
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        password2 = request.POST['password2']
        email = request.POST['email']       
        user_all = User.objects.all()
        check = 0
        if username != '' and password != '':
            for i in user_all:
                if i.username == username:
                    check = 1
                elif password2 != password:
                    check = 2
                elif i.email == email:
                    check = 3
                elif len(password) < 8:
                    check = 4
            if check == 0:
                user = User.objects.create_user(username=username, password=password, email=email)
                user.set_password(password)
                group = Group.objects.get(name='user')
                user.groups.add(group)
                user.save()
                return redirect('createprofile')
            elif check == 1:
                context['error'] = "already have this userename!"
                return render(request, 'MedNoti/sign-up.html', context=context)
            elif check == 3:
                context['error'] = "already have this Email!"
                return render(request, 'MedNoti/sign-up.html', context=context)
            elif check == 4:
                context['error'] = "รหัสผ่านต้องมีอย่างน้อย8ตัว"
                return render(request, 'MedNoti/sign-up.html', context=context)
            else:
                context['error'] = "รหัสไม่ตรงกัน"
                return render(request, 'MedNoti/sign-up.html', context=context)
        else:
            context['error'] = "กรุณากรอกข้อมูล"
            return render(request, 'MedNoti/sign-up.html', context=context)

    else:
        return render(request, 'MedNoti/profile.html')

def regis(request):
    logout(request)
    return render(request, 'MedNoti/sign-up.html')

@login_required
def my_profile(request):
    user = request.user
    profile = Profile.objects.get(user_id=user.id)
    return render(request, 'MedNoti/profile.html', context={
        'user': user,
        'profile': profile
    })

@login_required
def change_password(request):
    context = {}
    if request.method == 'POST':
        user = request.user
        # user1 = User()
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if password1 == password2:
            user.set_password(password1)
            user.save()
            # user = authenticate(request, username=user1.username, password=password1)
            # login(request, user)
            return redirect('profile')
        else:
            context['password1'] = password1
            context['password2'] = password2
            context['error'] = "password does't match!"

        # check that the passwords match

        # reset password 

    return render(request, template_name='MedNoti/changepassword.html', context=context)

@login_required
def create_profile(request):
    user = request.user
    # profile = request.objects.profile
    # form = ContactForm(instance=user)
    if user.first_name == '':

        if request.method == 'POST':
            firstname = request.POST['first_name']
            lastname = request.POST['last_name']
            age = request.POST['age']
            sex = request.POST['sex']
            date_of_birth = request.POST['date_of_birth']
            disease = request.POST['disease']
            allergy = request.POST['allergy']
            # image_url = request.FILE['image_url']
            # form = ContactForm(request.FILES, instance=user)
            # if form.is_valid():
            #     form.save()
            temp = User.objects.filter(id=user.id).update(first_name=firstname, last_name=lastname)
            post = Profile(
                    age=age,
                    sex=sex,
                    date_of_birth=date_of_birth,
                    disease=disease,
                    allergy=allergy,
                    user_id=user.id,
                    image_url=request.FILES['image_url']
                )
            # img = Image(
            #     image_url=image_url,
            #     user_id_id=user.id)
            # img.save()
            post.save()
            return redirect('home')
        else:
            form = ContactForm()
            return render(request, template_name='MedNoti/createprofile.html', context={'form': form})
        

        return render(request, template_name='MedNoti/createprofile.html', context={'form': form})
    else:
        return redirect('home')

@login_required
def my_home(request):
    user = request.user
    
    meds = Medicine.objects.filter(user_id_id=user.id)
    count = meds.count()
    return render(request, 'MedNoti/home.html', context={
        'user': user,
        'meds': meds,
        'c': count
    })
   
def add_drug(request):
    user = request.user
    neighbor = ''
    try:
        neighbor = Neighbor.objects.filter(user_id=user.id)
        print("have")
    except Exception:
        pass
    # if Neighbor.objects.get(user_id=user.id):
    #     neighbor = Neighbor.objects.get(user_id=user.id)
    #     print("have")
    # else:
    #     print("dont have")
    if request.method == 'POST':
        name = request.POST['name']
        med_type = request.POST['med_type']
        cate = request.POST['cate']
        take_start = request.POST['take_start']
        unit_eat = request.POST['unit_eat']
        if 'freq1' in request.POST:
            freq1 = request.POST['freq1']
        else:
            freq1 = ''
        if 'freq2' in request.POST:
            freq2 = request.POST['freq2']
        else:
            freq2 = ''
        if 'freq3' in request.POST:
            freq3 = request.POST['freq3']
        else:
            freq3 = ''
        if 'freq4' in request.POST:
            freq4 = request.POST['freq4']
        else:
            freq4 = ''
        when = request.POST['when']
        hmt = request.POST['hmt']
        who = request.POST['who']
        post = Medicine(
                name=name,
                med_type=med_type,
                cate=cate,
                take_start=take_start,
                unit_eat=int(unit_eat),
                freq1=freq1,
                freq2=freq2,
                freq3=freq3,
                freq4=freq4,
                when=when,
                hmt=int(hmt),
                who=who,
                user_id_id=user.id
            )
        post.save()
        return redirect('home')
    else:
        return render(request, template_name='MedNoti/adddrug.html', context={
            'user': user,
            'neighbor': neighbor
        })
    return render(request, template_name='MedNoti/adddrug.html')

 
def my_menu(request):
    user = request.user
    return render(request, template_name='MedNoti/account.html', context={
        'user': user,
        })

@login_required
def edit_profile(request):
    user = request.user
    profile = Profile.objects.get(user_id=user.id)
    if request.method == 'POST':
        temp = User.objects.filter(id=user.id).update(first_name=request.POST['first_name'], last_name=request.POST['last_name'])
        post = Profile.objects.filter(user_id=user.id).update(
                age=request.POST['age'],
                sex=request.POST['sex'],
                date_of_birth=request.POST['date_of_birth'],
                disease=request.POST['disease'],
                allergy=request.POST['allergy'],
                # image_url=request.FILES['image_url']
            )
        m = Profile.objects.get(pk=profile.id)
        m.image_url = request.FILES['image_url']
        m.save()
        return redirect('home')
    else:
        return render(request, template_name='MedNoti/editprofile.html', context={
            'user':user,
            'profile': profile
        })
    return render(request, template_name='MedNoti/editprofile.html', context={
        'user':user,
        'profile': profile
    })

def edit_drug(request, num):
    user = request.user
    med = Medicine.objects.get(pk=num)
    neighbor = ''
    try:
        neighbor = Neighbor.objects.filter(user_id=user.id)
        print("have")
    except Exception:
        pass
    if request.method == 'POST':
        name = request.POST['name']
        med_type = request.POST['med_type']
        cate = request.POST['cate']
        take_start = request.POST['take_start']
        unit_eat = request.POST['unit_eat']
        if 'freq1' in request.POST:
            freq1 = request.POST['freq1']
        else:
            freq1 = ''
        if 'freq2' in request.POST:
            freq2 = request.POST['freq2']
        else:
            freq2 = ''
        if 'freq3' in request.POST:
            freq3 = request.POST['freq3']
        else:
            freq3 = ''
        if 'freq4' in request.POST:
            freq4 = request.POST['freq4']
        else:
            freq4 = ''
        when = request.POST['when']
        hmt = request.POST['hmt']
        who = request.POST['who']
        post = Medicine.objects.filter(pk=num).update(
                name=name,
                med_type=med_type,
                cate=cate,
                take_start=take_start,
                unit_eat=int(unit_eat),
                freq1=freq1,
                freq2=freq2,
                freq3=freq3,
                freq4=freq4,
                when=when,
                hmt=int(hmt),
                who=who
            )
        return redirect('home')
    else:
        return render(request, template_name='MedNoti/editDrug.html', context={
            'user':user,
            'med': med,
            'neighbor': neighbor
        })
    return render(request, template_name='MedNoti/editDrug.html', context={
        'user':user,
        'med': med,
        'neighbor': neighbor
    })
@login_required
def addOther(request):
    user = request.user
    # profile = request.objects.profile
    # form = ContactForm(instance=user)
    if request.method == 'POST':
        post = Neighbor(
                first_name=request.POST['first_name'],
                last_name=request.POST['last_name'],
                age=request.POST['age'],
                sex=request.POST['sex'],
                disease=request.POST['disease'],
                allergy=request.POST['allergy'],
                user_id_id=user.id,
                image_url=request.FILES['image_url']
            )
            # img = Image(
            #     image_url=image_url,
            #     user_id_id=user.id)
            # img.save()
        post.save()
        return redirect('home')
    else:
        return render(request, template_name='MedNoti/addOther.html')


def delete_med(request, num):
    Medicine.objects.filter(id=num).delete()
    return redirect('home')

def my_calendar(request):
    return render(request, template_name='MedNoti/calendar.html')

@login_required
def my_home2(request, num):
    med = Medicine.objects.get(pk=num)
    user = request.user
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            schedule = Schedule(
                check1=form.cleaned_data['check1'],
                check2=form.cleaned_data['check2'],
                check3=form.cleaned_data['check3'],
                check4=form.cleaned_data['check4'],
                medicine_id_id=num,
                date=datetime.now(),
                count=med.unit_eat,
                user_id_id=user.id
            )
            schedule.save()
            return redirect('minus-med', schedule.id)
        else:
            return redirect('home2', num)
    else:
        ContactFormSet = formset_factory(ContactForm, extra=1)
        form = ContactForm()
    return render(request, template_name='MedNoti/home2.html', context={
        'user': user,
        'med': med,
        'form': form,

    })

@login_required
def minus_med(request, num):
    schedule = Schedule.objects.get(pk=num)
    med = Medicine.objects.get(pk=schedule.medicine_id_id)
    temp = 0
    print(num)
    if schedule.check1:
        temp += 1
    if schedule.check2:
        temp += 1
    if schedule.check3:
        temp += 1
    if schedule.check4:
        temp += 1
    if temp == 0:
        pass
    else:
        var = med.unit_eat - (med.hmt*temp)
        post = Medicine.objects.filter(pk=med.id).update(
            unit_eat=var
        )
        post2 = Schedule.objects.filter(pk=num).update(
            count=var
        )
        if var <= 0:
            Medicine.objects.filter(id=med.id).delete()
    return redirect('home')
@login_required
def my_event(request):
    user = request.user
    calendar = ''
    try:
        events = Calendar.objects.filter(user_id=user.id)
        print("have")
    except Exception:
        pass
    if request.method == 'POST':
        post = Calendar(
                date=request.POST['date'],
                activity=request.POST['activity'],
                user_id_id=user.id
            )
            # img = Image(
            #     image_url=image_url,
            #     user_id_id=user.id)
            # img.save()
        post.save()
        return redirect('event')
    return render(request, template_name='MedNoti/event.html', context={
        'events': events
    })
@login_required
def delete_event(request, num):
    Calendar.objects.filter(id=num).delete()
    return redirect('event')
@login_required
def my_history(request):
    user = request.user
    schs = ''
    if request.method == 'POST':
        schs = Schedule.objects.filter(date=request.POST['date'])
    else:
        try:
            schs = Schedule.objects.filter(user_id_id=user.id)
        except Exception:
            pass
    return render(request, template_name='MedNoti/history.html', context={
        'schs': schs
    })
@login_required
def other_page(request):
    user = request.user
    neis = Neighbor.objects.filter(user_id_id=user.id)
    return render(request, template_name='MedNoti/other.html', context={
        'neis': neis
    })

@login_required
def my_other(request, num):
    nei = Neighbor.objects.get(pk=num)
    return render(request, 'MedNoti/profileOther.html', context={
        'nei': nei,
    })

@login_required
def edit_other(request, num):
    nei = Neighbor.objects.get(pk=num)
    if request.method == 'POST':
        post = Neighbor.objects.filter(pk=num).update(
                first_name=request.POST['first_name'],
                last_name=request.POST['last_name'],
                age=request.POST['age'],
                sex=request.POST['sex'],
                disease=request.POST['disease'],
                allergy=request.POST['allergy'],
                # image_url=request.FILES['image_url']
            )
        m = Neighbor.objects.get(pk=num)
        m.image_url = request.FILES['image_url']
        m.save()
        return redirect('myother', num)
    else:
        return render(request, template_name='MedNoti/editProfile2.html', context={
            'nei': nei
        })

def my_report(request):
    user = request.user
    schs = Schedule.objects.filter(user_id_id=user.id)
    week = 0
    week1 = 0
    week2 = 0
    week3 = 0
    week4 = 0
    temp = 0
    count1 = count2 = count3 = count4 = 0
    
    if request.method == 'POST':
        month = int(request.POST['month'])
        if month == 4 or month == 6 or month == 9 or month == 11:
            temp = 30
        elif month == 1 or month == 3 or month == 4 or month == 7 or month == 8 or month == 10 or month == 12:
            temp = 31
        else:
            temp = 28
        for sch in schs:
            for _ in range(temp):
                week += 1
                if week <= 7:
                    if week == sch.date.day and sch.date.year == int(request.POST['year']):
                        if sch.check1 == True and sch.medicine_id.freq1 != '':
                            week1 += 1
                            count1 += 1
                        elif sch.check1 == False and sch.medicine_id.freq1 != '':
                            count1 += 1
                        if sch.check2 == True and sch.medicine_id.freq2 != '':
                            week1 += 1
                            count1 += 1
                        elif sch.check2 == False and sch.medicine_id.freq2 != '':
                            count1 += 1
                        if sch.check3 == True and sch.medicine_id.freq3 != '':
                            week1 += 1
                            count1 += 1
                        elif sch.check3 == False and sch.medicine_id.freq3 != '':
                            count1 += 1
                        if sch.check4 == True and sch.medicine_id.freq4 != '':
                            week1 += 1
                            count1 += 1
                        elif sch.check4 == False and sch.medicine_id.freq4 != '':
                            count1 += 1
                elif week2 > 7 and week2 <= 14:
                    if week == sch.date.day and sch.date.year == int(request.POST['year']):
                        if sch.check1 == True and sch.medicine_id.freq1 != '':
                            week2 += 1
                            count2 += 1
                        elif sch.check1 == False and sch.medicine_id.freq1 != '':
                            count2 += 1
                        if sch.check2 == True and sch.medicine_id.freq2 != '':
                            week2 += 1
                            count2 += 1
                        elif sch.check2 == False and sch.medicine_id.freq2 != '':
                            count2 += 1
                        if sch.check3 == True and sch.medicine_id.freq3 != '':
                            week2 += 1
                            count2 += 1
                        elif sch.check3 == False and sch.medicine_id.freq3 != '':
                            count2 += 1
                        if sch.check4 == True and sch.medicine_id.freq4 != '':
                            week2 += 1
                            count2 += 1
                        elif sch.check4 == False and sch.medicine_id.freq4 != '':
                            count2 += 1
                elif week2 > 14 and week2 <= 21:
                    if week == sch.date.day and sch.date.year == int(request.POST['year']):
                        if sch.check1 == True and sch.medicine_id.freq1 != '':
                            week3 += 1
                            count3 += 1
                        elif sch.check1 == False and sch.medicine_id.freq1 != '':
                            count3 += 1
                        if sch.check2 == True and sch.medicine_id.freq2 != '':
                            week3 += 1
                            count3 += 1
                        elif sch.check2 == False and sch.medicine_id.freq2 != '':
                            count3 += 1
                        if sch.check3 == True and sch.medicine_id.freq3 != '':
                            week3 += 1
                            count3 += 1
                        elif sch.check3 == False and sch.medicine_id.freq3 != '':
                            count3 += 1
                        if sch.check4 == True and sch.medicine_id.freq4 != '':
                            week3 += 1
                            count3 += 1
                        elif sch.check4 == False and sch.medicine_id.freq4 != '':
                            count3 += 1
                else:
                    if week == sch.date.day and sch.date.year == int(request.POST['year']):
                        if sch.check1 == True and sch.medicine_id.freq1 != '':
                            week4 += 1
                            count4 += 1
                        elif sch.check1 == False and sch.medicine_id.freq1 != '':
                            count4 += 1
                        if sch.check2 == True and sch.medicine_id.freq2 != '':
                            week4 += 1
                            count4 += 1
                        elif sch.check2 == False and sch.medicine_id.freq2 != '':
                            count4 += 1
                        if sch.check3 == True and sch.medicine_id.freq3 != '':
                            week4 += 1
                            count4 += 1
                        elif sch.check3 == False and sch.medicine_id.freq3 != '':
                            count4 += 1
                        if sch.check4 == True and sch.medicine_id.freq4 != '':
                            week4 += 1
                            count4 += 1
                        elif sch.check4 == False and sch.medicine_id.freq4 != '':
                            count4 += 1
            week = 0
            result = week1 + week2 + week3 + week4
            count = count1 + count2 + count3 + count4
            print(week4)
            print(count4)
        if count1 == 0:
            week1 = 0
        else:
            week1 = (week1 * 100) / count1
        if count2 == 0:
            week2 = 0
        else:
            week2 = (week2 * 100) / count2
        if count3 == 0:
            week3 = 0
        else:
            week3 = (week3 * 100) / count3
        if count4 == 0:
            week4 = 0
        else:
            week4 = (week4 * 100) / count4
            week = 0

        # for sch in schs:
        #     if sch.date.year == int(request.POST['year']) and sch.date.month == int(request.POST['month']):
        #         if 
        #         perf = Performance(
        #             date=sch.date,
        #             user_id_id=user.id
        #         )
        #         perf.save()
        #     else:
        #         print('bruh')
        return render(request, template_name='MedNoti/report.html', context={
            'week1': week1,
            'week2': week2,
            'week3': week3,
            'week4': week4
        })
    return render(request, template_name='MedNoti/report.html', context={
            'num': 20
        })
def my_setting(request):
    return render(request, template_name='MedNoti/setting.html')