from django.forms import ModelForm
from  .models import Education,Profile



class EducationForm(ModelForm):
    class Meta:
    	model=Education
    	fields=['name','board_university','passing_year','percentage']

    