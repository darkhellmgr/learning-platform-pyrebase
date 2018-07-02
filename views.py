from django.http import HttpResponse
from django.shortcuts import render, redirect
import pyrebase
from django.contrib import auth
from django import forms
from django.utils.safestring import mark_safe

from mainapp.models import School, Room, Building, Topic, Course, Program, CourseSchedule, Quiz

# Create your views here.
from mainapp.forms import StaffForm, StudentForm, ParentForm, MyStyleForm


def getnameidlist(which, suitablename):
    try:
        mydata = db.child(which).get().val()

        idslist = list(mydata.keys())
        print(idslist)
        nameslist = []
        for i in idslist:
            nameslist.append(mydata[i][suitablename])
        print(nameslist)
        return zip(idslist, nameslist)
    except:
        pass


def getform(formtype):
    if formtype == 'Schools':
        modelform = School
        comb_list = []
    elif formtype == 'Rooms':
        modelform = Room
        comb_list = getnameidlist("Buildings", "name_or_number")
    elif formtype == 'Buildings':
        modelform = Building
        comb_list = getnameidlist("Schools", "name")
    elif formtype == 'Topics':
        modelform = Topic
        comb_list = getnameidlist("Courses", "title")
    elif formtype == 'Courses':
        modelform = Course
        comb_list = getnameidlist("Programs", "title")
    elif formtype == 'Programs':
        modelform = Program
        comb_list = getnameidlist("Schools", "name")
    elif formtype == 'CourseSchedules':
        modelform = CourseSchedule
        comb_list = getnameidlist("Courses", "title")
    elif formtype == 'Quiz':
        modelform = Quiz
        comb_list = getnameidlist("Questions", "question")
    return (modelform, comb_list)


config = {
    'apiKey': "AIzaSyBTCNgjJpStBaazWCTkn9WmOzRD1jHkTEY",
    'authDomain': "learning-management-7b9f2.firebaseapp.com",
    'databaseURL': "https://learning-management-7b9f2.firebaseio.com",
    'projectId': "learning-management-7b9f2",
    'storageBucket': "learning-management-7b9f2.appspot.com",
    'messagingSenderId': "482234388569"
}
firebase = pyrebase.initialize_app(config)

authe = firebase.auth()
db = firebase.database()
storage = firebase.storage()

# to show items in admin panel
items = ['Schools', 'Rooms', 'Buildings', 'Topics', 'Courses', 'Programs', 'CourseSchedules', 'Quiz', 'Questions']


# for getting list of ids of database
# def getidslist(which):
#     return (list(db.child(which).shallow().get().val()))
# for getting list of names relating to id in that database

# Schoolids=getidslist('Schools')
# Schoolnames=getnamelist('Schools',Schoolids)
# print(Schoolids)
# print(Schoolnames)


# For User authentication
def sign(request):
    return render(request, "source/login.html")


def getusernamelist(which):
    data = db.child("Users").get().val()
    idlist = list(data[which].keys())
    student_namelist = []
    for i in idlist:
        student_namelist.append(data[which][i]['details']['name'])
    return zip(idlist, student_namelist)


def postsign(request):
    email = request.POST.get("email")
    passw = request.POST.get("pass")

    try:
        user = authe.sign_in_with_email_and_password(email, passw)
        userid = user['localId']
        print(user['idToken'])
        adminid_list = (list(db.child('Users').child('admin').shallow().get().val()))
        if userid in adminid_list:
            session_id = user['idToken']  # making session for user
            request.session['uid'] = str(session_id)
            return render(request, "source/admin.html", {"items": items})
        else:
            message = "You are not authoriized"
            return render(request, "source/login.html", {"messg": message})
    except RuntimeError:
        pass
        # message = "Invalid Credentials"
        # print(message)
        # return render(request, "source/login.html", {"messg": message})




def logout(request):
    auth.logout(request)
    return sign(request)


def allform(request, formtype, id=None):
    class AllForm(MyStyleForm):
        class Meta:
            model = getform(formtype)[0]
            fields = '__all__'

    # for editing forms
    if id:
        try:
            forminstance = db.child(formtype).child(id).get().val()
            form = AllForm(forminstance)

        except:
            isupdate = 0
            return HttpResponse("id not valid")  # for adding new data into forms
    else:
        form = AllForm()

    if request.method == 'POST':
        form = AllForm(request.POST)
        print(request.POST)
        request.POST._mutable = True
        r = request.POST
        if form.is_valid:
            schoolid = r['csrfmiddlewaretoken']
            del r['csrfmiddlewaretoken']
            print(r)
            # update if request.post has id
            if id:
                db.child(formtype).child(id).update(r)
            else:
                # insert if request.post doesnt have id
                db.child(formtype).push(r)
            return redirect('/mainapp/home/')
    comb_list = getform(formtype)[1]
    print(comb_list)
    args = {'form': form, 'items': items, 'comb_list': comb_list}

    return render(request, 'allforms.html', args)


def home(request):
    mydata = db.child("Schools").get().val()
    idslist = list(mydata.keys())
    nameslist = []
    for i in idslist:
        nameslist.append(mydata[i]['name'])
    print(nameslist)
    return render(request, 'home.html')


def userform(request, formtype):
    if formtype == 'staff':
        form = StaffForm()
        category = "Staff"


    elif formtype == 'student':
        form = StudentForm()
        category = "Student"
    elif formtype == 'parent':
        form = ParentForm()
        category = "Parent"
        return render(request, 'source/relationform.html',
                      {"form": form, 'comb_list': getusernamelist("Student")})

    if request.method == 'POST':
        print(request.POST)
        request.POST._mutable = True
        email = request.POST.get("email")
        passw = request.POST.get("password")
        r = request.POST
        print(r)

        try:
            if form.is_valid:
                del r['csrfmiddlewaretoken']
                print(r)
                user = authe.create_user_with_email_and_password(email, passw)
                uid = user['localId']
                print(uid)
                db.child("Users").child(category).child(uid).child('details').set(r)
                return redirect('source/admin.html')

        except:
            message = "Unable to create account. Please try again"
            return render(request, "accounts/admin.html", {"messg": message})

    args = {'form': form, 'items': items}

    return render(request, "source/form.html", args)


def details(request):
    allvalues = db.child('Questions').get().val()
    import json
    jsonobj = mark_safe(json.dumps(allvalues))
    return render(request, 'details.html', {'jsonobj': jsonobj})
