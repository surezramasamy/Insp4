from django import forms
from .models import Project_code,Inspection,Part_detail

class LoginForm(forms.Form):
    username =forms.CharField(max_length=200)
    password =forms.CharField(max_length=200)

    def clean(self):
        data =self.cleaned_data
        username =data.get('username')
        password=data.get('password')

        return data

class Project_Form(forms.ModelForm):
    class Meta:    
        model = Project_code
        fields = ["project_code","Work_order_No","part_no","Qty","Operator","Machine","RM_Coil_No"]

class DateInput(forms.DateInput):
    input_type = 'date'

class Inspform(forms.Form):
    fromDate=forms.DateField(required=False,widget=DateInput)
    toDate=forms.DateField(required=False,widget=DateInput)


class PartDetailForm(forms.ModelForm):
    class Meta:
        model = Part_detail
        fields = ['part_no', 'part_name', 'Drawing']

class DrawingSearchForm(forms.Form):
    part_no = forms.CharField(label='Part Number', required=False)




