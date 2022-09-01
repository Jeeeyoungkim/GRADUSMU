from django.shortcuts import render, redirect
from .models import subjects, BalancedCulture
from accounts.models import User
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse
import datetime

#들은 과목 
def signed_search_subject(request):
    request = json.loads(request.body)
    
    user = User.objects.get(id = request['user_id'])
    signed = list(user.sign_up.values_list('id',flat=True))
    if request['dept_type'] == "전심":
        dept_type = "1전심"
    elif request['dept_type'] == "전선":
        dept_type = "1전선"
    elif request['dept_type'] == "교선":
        dept_type = "교선"
    elif request['dept_type'] == "교필":
        dept_type = "교필"
    elif request['dept_type'] == "균교":
        dept_type = "균교"
    year = "20"+request['year'][:2]
    semester = request['year'][5]
    if dept_type == "균교":
        print(dept_type)
        datas = BalancedCulture.getBal()
        context = {}
        i=0
        for key in list(datas.keys()):
            for data in datas[key].filter(id__in = signed):
                context[i] = {
                    "id" : data.id,
                    "name" : data.name,
                    "serial_num" : data.serialNumber+"-"+str(data.distribution),
                    "prof" : data.prof,
                    "point" : data.point,
                    "sort" : key
                }
                i+=1

    else:
        datas = subjects.objects.filter(type = dept_type,year = year, semester = int(semester)).filter(id__in = signed)
        context={}
        for i in range(len(datas)):
            context[i] = {
                "id" : datas[i].id,
                "name" : datas[i].name,
                "serial_num" : datas[i].serialNumber+"-"+str(datas[i].distribution),
                "prof" : datas[i].prof,
                "point" : datas[i].point,
            }
        
    return JsonResponse(context)

#안들은 과목 
def unsigned_search_subject(request):
    request = json.loads(request.body)
    
    user = User.objects.get(id = request['user_id'])
    signed = list(user.sign_up.values_list('id',flat=True))
    if request['dept_type'] == "전심":
        dept_type = "1전심"
    elif request['dept_type'] == "전선":
        dept_type = "1전선"
    elif request['dept_type'] == "교선":
        dept_type = "교선"
    elif request['dept_type'] == "교필":
        dept_type = "교필"
    elif request['dept_type'] == "균교":
        dept_type = "균교"
    year = "20"+request['year'][:2]
    semester = request['year'][5]
    if dept_type == "균교":
        datas = BalancedCulture.getBal()
        context = {}
        i=0
        for key in list(datas.keys()):
            for data in datas[key].exclude(id__in = signed):
                context[i] = {
                    "id" : data.id,
                    "name" : data.name,
                    "serial_num" : data.serialNumber+"-"+str(data.distribution),
                    "prof" : data.prof,
                    "point" : data.point,
                    "sort" : key
                }
                i+=1

    else:
        datas = subjects.objects.filter(type = dept_type,year = year, semester = int(semester)).exclude(id__in = signed)
        context={}
        for i in range(len(datas)):
            context[i] = {
                "id" : datas[i].id,
                "name" : datas[i].name,
                "serial_num" : datas[i].serialNumber+"-"+str(datas[i].distribution),
                "prof" : datas[i].prof,
                "point" : datas[i].point,
            }
        
    return JsonResponse(context)

#과목 상세
def subject_detail(request):
    request = json.loads(request.body)
    user = User.objects.get(id = request['user_id'])
    signed = list(user.sign_up.values_list('id',flat=True))

    subject = subjects.objects.get(id = request['subject_id'])
    
    context = {
            "id" : subject.id,
            "name" : subject.name,
            "yaer" : subject.year + "년" + str(subject.semester) + "학기",
            "type" : subject.type,
            "serial_num" : subject.serialNumber+"-"+str(subject.distribution),
            "prof" : subject.prof,
            "point" : str(subject.point) + "학점",
            "room" : subject.room,
            "time" : subject.time,
            "dept" : subject.dept,
            "signed" : True if subject.id in signed else False,
        }
    return JsonResponse(context)

#학점 상세 페이지
def score_detail(request):
    return render(request,"scoreDetail.html")

#학점 상세 페이지
def score_graph_detail(request):
    return render(request,"scoreGraphDetail.html")

#과목 추가
@csrf_exempt
def add_subject(request):
    
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            
            user = User.objects.get(id = data['user_id'])
            user.sign_up.add(subjects.objects.get(id = data["subject_id"]))
            is_added = True
        except:
            is_added = False
        context = {
            "is_added" : is_added,
        }
        return JsonResponse(context)
    else:
        
        return render(request, "addSubject.html")

@csrf_exempt
def delete_subject(request):
    if request.method == "DELETE":
        try:
            data = json.loads(request.body)
            
            user = User.objects.get(id = data['user_id'])
            user.sign_up.remove(subjects.objects.get(id = data["subject_id"]))
            is_deleted = True
        except:
            is_deleted = False
        context = {
            "is_deleted" : is_deleted,
        }
        return JsonResponse(context)
    else:
        
        return render(request, "addSubject.html")
# 균교 영역별 
def balanced_search_subject(request):
    request = json.loads(request.body)
    
    user = User.objects.get(id = request['user_id'])
    signed = list(user.sign_up.values_list('id',flat=True))
    currentDateTime = datetime.datetime.now()
    date = currentDateTime.date()
    year = date.strftime("%Y")
    datas = BalancedCulture.getBal()
    context = {}
    i=0
    for data in datas[request['dept_type']].filter(id__in = signed):
        context[i] = {
            "id" : data.id,
            "name" : data.name,
            "serial_num" : data.serialNumber+"-"+str(data.distribution),
            "prof" : data.prof,
            "point" : data.point,
            "signed" : True
        }
        i+=1
    for data in datas[request['dept_type']].filter(year = year).exclude(id__in = signed):
        context[i] = {
            "id" : data.id,
            "name" : data.name,
            "serial_num" : data.serialNumber+"-"+str(data.distribution),
            "prof" : data.prof,
            "point" : data.point,
            "signed" : False
        }
        i+=1    
    return JsonResponse(context)
