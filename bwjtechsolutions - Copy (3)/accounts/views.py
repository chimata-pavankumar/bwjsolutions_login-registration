from django.shortcuts import render, redirect
from django.contrib.auth.models import auth, User
from django.contrib import messages
import psycopg2
import json
from django.http import HttpResponse
from django.core.mail import send_mail
from django.conf import settings
import re
from accounts.forms import DocumentForm
from django.core.files.storage import FileSystemStorage
from accounts.models import users_table
# Create your views here.

AUDIO_FILE_TYPES = ['wav', 'mp3', 'ogg','png', 'jpg', 'jpeg']

def register(request):
    return render(request, 'register.html')

def login(request):
    return render(request,'login.html')

def login_(request):
    if request.is_ajax or request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        mydb = psycopg2.connect(
            host='localhost', user='postgres', password='pavanyadav123', database='bwjtech_account')
        mycursor = mydb.cursor()
        mysql = "select username from accounts_users_table where email like \'%s\'" % (email+'%')
        mycursor.execute(mysql)
        username = mycursor.fetchone()
        if username:
            a = [*username,password]
            user = auth.authenticate(username = a[0], password = a[1])
            if user is not None:
                auth.login(request, user)
                data = ['successfully logined']
                return HttpResponse(json.dumps(dnata))
            else:
                data = ['password incorrect']
                return HttpResponse(json.dumps(data))
        else:
            data = ['email not exists']
            return HttpResponse(json.dumps(data))
    else:
        return render(request, 'login.html')



def success(request):
    return render(request,'success.html')
    
def logout(request):
    auth.logout(request)
    return render('/')

def registration(request):
    if request.is_ajax() or request.method == 'POST':
        context = {}
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        DOB = request.POST.get('dob')
        tel = request.POST.get('tel')
        address = request.POST.get('address')
        gender = request.POST.get('gender')
        resume = request.FILES['resume']
        fs = FileSystemStorage()
        name = fs.save(resume.name, resume)
        context["url"] = fs.url(name)
        mydb = psycopg2.connect(host='localhost', user='postgres', password='pavanyadav123', database='bwjtech_account')
        mycursor = mydb.cursor()
        mysql = "select id from accounts_users_table where tel = %s" %(tel)
        mycursor.execute(mysql)
        m = mycursor.fetchone()
        if password1 == password2:
            if re.match(r'[a-z0-9]{6,}', password1):
                if User.objects.filter(email=email).exists():
                    data = ['email already exists']
                    return HttpResponse(json.dumps(data))
                elif User.objects.filter(username=username).exists():
                    data = ['username already exists']
                    return HttpResponse(json.dumps(data))
                elif m:
                    data = ['mobile number already exists']
                    return HttpResponse(json.dumps(data))
                else:
                    mysql = 'insert into accounts_users_table(username,first_name,last_name, "Resume", email,"DOB",password,gender,address,tel) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
                    data = (username, first_name, last_name,context["url"], email,
                        DOB, password1, gender, address, tel)
                    mycursor.execute(mysql, data)
                    mydb.commit()
                    send_mail(
                        'bwjtech solutions',
                        'you have successfully registered to bwjtech solutions',
                        'pavanch690@gmail.com',
                        [email],
                        fail_silently=False
                    )
                    user = User.objects.create_user(
                        username=username, first_name=first_name, last_name=last_name, email=email, password=password1)
                    user.save()
                    #data = ['account succesfully created']
                    return render(request,'login.html')
            else:
                data = ['password should contain alteast 1 characters in [a-z0-9]']
                return HttpResponse(json.dumps(data))
        else:
            data = ['confirm password does not match']   
            return HttpResponse(json.dumps(data))
    else:
        return redirect('/')
    
"""    
    
def registration(request):
    if request.is_ajax() or request.method == 'POST':
        context = {}
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        DOB = request.POST.get('dob')
        tel = request.POST.get('tel')
        address = request.POST.get('address')
        gender = request.POST.get('gender')
        resume = request.FILES['resume']
        fs = FileSystemStorage()
        name = fs.save(resume.name, resume)
        context["url"] = fs.url(name)
        mycursor = mydb.cursor()
        mydb = psycopg2.connect(host='localhost', user='postgres', password='pavanyadav123', database='bwjtech_account')
        mycursor = mydb.cursor()
        mysql = "select id from accounts_users_table where tel = %s" %(tel)
        mycursor.execute(mysql)
        m = mycursor.fetchone()
        if password1 == password2:
            if re.match(r'[a-z0-9]{6,}', password1):
                if User.objects.filter(email=email).exists():
                    data = ['email already exists']
                    return HttpResponse(json.dumps(data))
                elif User.objects.filter(username=username).exists():
                    data = ['username already exists']
                    return HttpResponse(json.dumps(data))
                elif m:
                    data = ['mobile number already exists']
                    return HttpResponse(json.dumps(data))
                else:
                    mysql = 'insert into accounts_users_table(username,first_name,last_name, "Resume, email,"DOB",password,gender,address,tel) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
                    data = (username, first_name, last_name,context["url"], email,
                        DOB, password1, gender, address, tel)
                    mycursor.execute(mysql, data)
                    mydb.commit()
                    send_mail(
                        'bwjtech solutions',
                        'you have successfully registered to bwjtech solutions',
                        'pavanch690@gmail.com',
                        [email],
                        fail_silently=False
                    )
                    user = User.objects.create_user(
                        username=username, first_name=first_name, last_name=last_name, email=email, password=password1)
                    user.save()
                    data = ['account succesfully created']
                    return HttpResponse(json.dumps(data))
            else:
                data = ['password should contain alteast 1 characters in [a-z0-9]']
                return HttpResponse(json.dumps(data))
        else:
            data = ['confirm password does not match']   
            return HttpResponse(json.dumps(data))
    else:
        return redirect('/')
"""    
"""   
        var token = '{{csrf_token}}';
            $.ajax({
                async: true,
                headers: {
                    "X-CSRFToken": token
                },
                type: 'POST',
                url: 'registration',
                dataType: 'json',
                data: {
                    'password1'  :  $('#password1').val(),
                    'password2'  :  $('#password2').val(),
                    'username'   :  $('#user').val(),
                    'first_name' :  $('#first').val(),
                    'last_name'  :  $('#last').val(),
                    'email'      :  $('#email').val(),
                    'gender'     :  $('input[type="radio"]').val(),
                    'dob'        :  $('#dob').val(),
                    'address'    :  $('#address').val(),
                    'resume'     :  $('#resume').val(),
                    'tel'        :  $('#tel').val()
                },
                success: function(data) {
                    if (data =='username already exists'){
                        $('#userdiv').text('username already exists');
                        $('#emaildiv').empty();
                        $('#teldiv').empty();
                        $('#passworddiv').empty();
                        $('#confirmdiv').empty();
                    }else if(data == 'email already exists'){
                        $('#emaildiv').text('email already exists');
                        $('#userdiv').empty();
                        $('#teldiv').empty();
                        $('#passworddiv').empty();
                        $('#confirmdiv').empty();
                    }else if(data == 'mobile number already exists'){
                        $('#teldiv').text('mobile number already exists');
                        $('#emaildiv').empty();
                        $('#userdiv').empty();
                        $('#passworddiv').empty();
                        $('#confirmdiv').empty();
                    }else if (data == 'password should contain alteast 1 characters in [a-z0-9]'){
                        $('#passworddiv').text('password should contain alteast 1 characters in [a-z0-9]');
                        $('#teldiv').empty();
                        $('#emaildiv').empty();
                        $('#userdiv').empty();
                        $('#confirmdiv').empty();
                    }else if(data == 'confirm password does not match'){
                        $('#confirmdiv').text('confirm password does not match');
                        $('#passworddiv').empty();
                        $('#teldiv').empty();
                        $('#emaildiv').empty();
                        $('#userdiv').empty();
                    }else{
                        $('.success').text(data);
                        $('.dialog').dialog("open");
                        $('#confirmdiv').empty();
                        $('#passworddiv').empty();
                        $('#teldiv').empty();
                        $('#emaildiv').empty();
                        $('#userdiv').empty();
                    }
                },
                error: function() {
                    console.log('error in sending');
                },
            });
        });
"""
