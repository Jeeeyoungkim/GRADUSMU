import switch as switch
from django.db import models
import json


# J 이수학점 MODEL

class GraduationCiteria(models.Model):
    underGra = models.CharField(max_length=50)  #학부
    major = models.CharField(max_length=50)     #학과

    essentialLiberal = models.IntegerField(null=True)  #교필
    choiceLiberal = models.IntegerField(null=True)      #균교

    #심화전공
    deepMajor = models.IntegerField(null=True)          #전심
    deepChoiceMajor = models.IntegerField(null=True)    #전선

    #다전공
    manyMajor1 = models.IntegerField(null=True)         #다전공2    manyMajor2 = models.IntegerField(null=True)

    # 부전공
    essMajor = models.IntegerField(null=True)           #주전공
    subMajor = models.IntegerField(null=True)           #부전공
    # 총 이수
    total = models.IntegerField(null=False)


class subjects(models.Model):
    serialNumber = models.CharField(max_length=100,null=False) #학수번호
    semester = models.IntegerField() #학기
    distribution = models.IntegerField(null=False) # 분반
    name = models.CharField(max_length=100,null=False) # 과목이름
    grade = models.IntegerField(null=False) #학년
    prof = models.CharField(max_length=100,null=False) # 교수님
    dept = models.CharField(max_length=100,null=False) # 개설학과
    time = models.CharField(max_length=100,null=False) # 강의 시간
    room = models.CharField(max_length=100,null=False) # 강의실
    type = models.CharField(max_length=100,null=False) # 구분
    point = models.IntegerField(null=False) # 학점
    year = models.CharField(max_length=10,null=False) # 개설연도


class EssentialLiberalArts(models.Model):
    sort = models.CharField(max_length=50, null=True)
    name = models.CharField(max_length=50,null=True)
    year = models.IntegerField(max_length=50, null=True)

    def getEss(request):
        forCount = EssentialLiberalArts.object.all
        subject = subjects.object.all
        ess={}
        ess["사고와표현"] = []
        ess["EnglishFoundations"] = []
        ess["기초수학"] = []
        ess["컴퓨팅사고와데이터의이해"] = []
        ess["알고리즘과게임콘텐츠"]=[]

        for i in range(subject.count()):
            for j in range(forCount.count()):
                if subject[i].name == forCount[j].name:
                    ess[forCount[j].sort].append({
                        "core": forCount[j].sort,
                        "serialNumber": subject[i].serialNumber,
                        "semester": subject[i].semester,
                        "distribution": subject[i].distribution,
                        "name": subject[i].name,
                        "grade": subject[i].grade,
                        "prof": subject[i].prof,
                        "dept": subject[i].dept,
                        "time": subject[i].time,
                        "room": subject[i].room,
                        "type": subject[i].type,
                        "point": subject[i].point,
                        "year": subject[i].year,
                        "years": forCount[j].year
                    })
        context = {"ess": ess}
        return()

class CoreLiberalArtsSortation(models.Model):
    name = models.CharField(max_length=50, null=True)

class  CoreLiberalArts(models.Model):
    sort = models.CharField(max_length=50, null=True)
    name = models.CharField(max_length=50, null=True)
    year = models.IntegerField(max_length=50, null=True)

    def getCore(request):
        forCount = CoreLiberalArts.object.all
        subject = subjects.object.all
        core={}
        core["창의적문제해결역량"] = []
        core["융복합역량"] = []
        core["다양성존중역량"] = []
        core["윤리실천역량"] = []
        for i in range(subject.count()):
            for j in range(forCount.count()):
                if subject[i].name == forCount[j].name:
                    core[forCount[j].sort].append({
                        "core": forCount[j].sort,
                        "serialNumber": subject[i].serialNumber,
                        "semester": subject[i].semester,
                        "distribution": subject[i].distribution,
                        "name": subject[i].name,
                        "grade": subject[i].grade,
                        "prof": subject[i].prof,
                        "dept": subject[i].dept,
                        "time": subject[i].time,
                        "room": subject[i].room,
                        "type": subject[i].type,
                        "point": subject[i].point,
                        "year": subject[i].year,
                        "years": forCount[j].year
                    })
        context = {"core": core}
        return (request, context)




class BalancedCurtureNot(models.Model):
    major = models.CharField(max_length=50, null=True)
    field = models.CharField(max_length=50, null=True)

class BalancedCultureSortation(models.Model):
    name = models.CharField(max_length = 50, null=True)



class BalancedCulture(models.Model):
    sort = models.CharField(max_length = 50, null=True)
    name = models.CharField(max_length = 50, null=True)
    year = models.IntegerField(max_length=50, null=True)

    def getBal():
        forCount={}
        forCount['인문'] = BalancedCulture.objects.filter(name = "인문").values_list('sort',flat = True)
        forCount['사회'] = BalancedCulture.objects.filter(name = "사회").values_list('sort',flat = True)
        forCount['자연'] = BalancedCulture.objects.filter(name = "자연").values_list('sort',flat = True)
        forCount['공학'] = BalancedCulture.objects.filter(name = "공학").values_list('sort',flat = True)
        forCount['예술'] = BalancedCulture.objects.filter(name = "예술").values_list('sort',flat = True)

        bal={}
        bal["인문"] = subjects.objects.filter(name__in = forCount["인문"])
        bal["사회"] = subjects.objects.filter(name__in = forCount["사회"])
        bal["자연"] = subjects.objects.filter(name__in = forCount["자연"])
        bal["공학"] = subjects.objects.filter(name__in = forCount["공학"])
        bal["예술"] = subjects.objects.filter(name__in = forCount["예술"])

        return (bal)
#과목 모델





