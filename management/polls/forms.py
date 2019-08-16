from django.forms import ModelForm
from .models import *
from django import forms
import datetime
from django.contrib.auth.models import User
from django.forms import DateTimeInput
'''
#샵샵
from django.forms.models import ModelMultipleChoiceField
'''





#첫번째페이지
# class DateInput(forms.DateInput):
#     input_type = 'date'

class UserModelMultipleChoiceField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        return obj.username

class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'summary', 'description', 'update_time', 'reg_date']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ProjectName'}),
            'summary': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Summary'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Description'}),
            'update_time': DateTimeInput(attrs={'class': 'form-control', 'type': 'date'}),
            'reg_date': DateTimeInput(attrs={'class': 'form-control', 'type': 'date'})
            #'update_time': DateInput(),
            #'reg_date': DateInput()
        }
    member_idx = UserModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple(), queryset=AuthUser.objects.exclude(username='admin'))





#두번째페이지용
class ReportDailyForm(forms.ModelForm):
    class Meta:
        model = ReportDaily
        fields = [
            'daily_date',
            'comment',
            'love',
        ]
        labels = {
            'daily_date': 'Daily date',
            'comment': 'Comment',
            'love': 'Love',
        }
        widgets = {
            'daily_date': DateTimeInput(attrs={'class': 'form-control', 'value': datetime.date.today}),
            'comment': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Comment'}),
            'love': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Love'}),
        }
    # daily_date = forms.DateField(initial=datetime.date.today)

#회원가입/두번째
class MyModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.name

#두번째-formset용
class ReportDailyProjectForm(forms.ModelForm):
    class Meta:
        model = ReportDailyProject
        fields = [
            'project_idx',
            'contents',
            'remarks',
        ]
        widgets = {
            'project_idx': forms.TextInput(attrs={'class': 'formset-field'}),
            'contents': forms.TextInput(attrs={'class': 'formset-field'}),
            'remarks': forms.TextInput(attrs={'class': 'formset-field'})
        }
    project_idx = MyModelChoiceField(queryset=Project.objects.all())





#회원가입
class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
            'password': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
            'email': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'E-mail'})
        }
    #미정
    def save(self, commit=True):
        division = self.cleaned_data.get('division', None)
        return super(UserForm, self).save(commit=commit)





#로그인
class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})
        }


