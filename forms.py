from django import forms

from mainapp.models import (
User, 
School,
Room,
Building,
Topic,
Course,
Program, 
CourseSchedule,
Quiz,
StudentQuizQuestionAttempt )
 


class StaffForm(forms.ModelForm):
    class Meta:
        model = User
        exclude = ('dob', 'special_care_needed', 'subject_of_interest', 'children_name',)


class StudentForm(forms.ModelForm):
    class Meta:
        model = User
        exclude = ('designation', 'children_name',)


class ParentForm(forms.ModelForm):
    class Meta:
        model = User
        exclude = ('designation', 'subject_of_interest', 'special_care_needed','dob',)


class MyStyleForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(MyStyleForm, self).__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


