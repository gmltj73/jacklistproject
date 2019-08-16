from django.shortcuts import render, redirect
from .models import *
from .forms import *
from django.http import HttpResponse
from django.forms import modelformset_factory
from django.db import transaction, IntegrityError
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.contrib.auth import logout
from django.contrib import messages


'''
#샵샵
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
'''



'''
#첫번째 페이지_초기
def ProjectCreate(request):
    if request.method=='POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            obj = Project(name=form.data['name'],summary=form.data['summary'],description=form.data['description'],
                          update_time=form.data['update_time'],reg_date=form.data['reg_date'])
            obj.save()
            return HttpResponse('success')
        return HttpResponse('fail')
    elif request.method=='GET':
        form = ProjectForm()
        return render(request, 'polls/form.html', {'form': form})
    else:
        pass
'''



#첫번째페이지_완성
def ProjectCreate(request):
    if request.method=='POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            Project(name=form.data['name'], summary=form.data['summary'],
                    description=form.data['description'], update_time=form.data['update_time'], reg_date=form.data['reg_date']).save()
            project_idx = Project.objects.latest("field_idx")
            value_set = request.POST.getlist('member_idx')
            for value in value_set:
                member_idx = AuthUser.objects.get(id=value)
                ProjectMember(project_idx=project_idx, member_idx=member_idx).save()
                messages.info(request, 'saved successfully!')
            return redirect('polls:main')
        return HttpResponse('fail')
    elif request.method=='GET':
        form = ProjectForm()
        return render(request, 'polls/form.html', {'form': form})
    else:
        pass



'''
#두번째 페이지_초기
def ReportDailyCreate(request):
    if request.method == 'POST':
        form = ReportDailyForm(request.POST)
        if form.is_valid():

            project = Project.objects.get(field_idx=form.data['project_idx'])
            ReportDaily(daily_date=form.data['daily_date'], comment=form.data['comment'], love=form.data['love']).save()
            daily_report = ReportDaily.objects.latest("field_idx")
            ReportDailyProject(report_daily_idx=daily_report, project_idx=project, contents=form.data['contents'],
                               remarks=form.data['remarks']).save()
            return HttpResponse('success')
        return HttpResponse('fail')
    #GET
    else:
        form = ReportDailyForm()how to import modelformset_factory
    return render(request, 'polls/formsecond.html', {'form': form})
'''



#두번째 페이지_완성
def ReportDailyCreate(request):
    context = {}
    ReportDailyProjectFormset = modelformset_factory(ReportDailyProject, form=ReportDailyProjectForm)
    form = ReportDailyForm(request.POST or None)
    formset = ReportDailyProjectFormset(request.POST or None, queryset= ReportDailyProject.objects.none(), prefix='report_daily_project')
    if request.method == "POST":
        if form.is_valid() and formset.is_valid():
            try:
                with transaction.atomic():
                    reportdaily = form.save(commit=False)
                    #member 추가
                    user = AuthUser.objects.get(username = request.user.get_username())
                    reportdaily.member_idx = user

                    reportdaily.save()
                    report_daily_idx = ReportDaily.objects.latest("field_idx")


                    for reportdailyproject in formset:
                        data = reportdailyproject.save(commit=False)
                        data.report_daily_idx = report_daily_idx
                        data.reportdailyproject = reportdailyproject
                        data.save()
                        # cd = reportdailyproject.cleaned_data
                        # project_idx = cd.get('project_idx')
                        # contents = cd.get('contents')
                        # remarks = cd.get('remarks')
                        # rdp_save = ReportDailyProject(report_daily_idx = report_idx, project_idx = project_idx, contents = contents, remarks = remarks)
                        # rdp_save.save()

            except IntegrityError:
                print("Error Encountered")

            return redirect('polls:list')


    context['formset'] = formset
    context['form'] = form
    return render(request, 'polls/for_form.html', context)

def list(request):
    datas = ReportDaily.objects.all()
    return render(request, 'polls/list.html', {'datas':datas})



#회원가입
def signup(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            # division = AuthUserDivision.objects.get(field_idx=form.data['division'])
            new_user = User.objects.create_user(**form.cleaned_data)
            # new_user.division = division
            login(request, new_user)
            #return HttpResponse('가입 성공.')
            return redirect('polls:join')
        else:
            return HttpResponse('가입 실패. 다시 시도 해보세요.')
    else:
        form = UserForm()
        return render(request, 'polls/adduser.html', {'form': form})





#로그인
def signin(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('polls:main')
        else:
            return HttpResponse('로그인 실패. 다시 시도 해보세요.')
    else:
        form = LoginForm()
        return render(request, 'polls/login.html', {'form': form})




#로그아웃
def logout(request):
    logout(request)
    return redirect('polls:main')





#메인페이지
def main(request):
    project = Project.objects.order_by('-field_idx')[:5]
    daily = ReportDaily.objects.order_by('-field_idx')[:5]
    project_member = ProjectMember.objects.all()
    context = {
        'project': project,
        'daily': daily,
        'project_member': project_member,
    }
    return render(request, 'polls/main.html', context=context)
