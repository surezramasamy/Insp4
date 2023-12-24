from django.db import models
from django.contrib.auth.models import User



class Part_group(models.Model):
    Part_group=models.CharField(max_length=256,blank=True,null=True)    
    
    def __str__(self):
        return str(self.Part_group)  


class Part(models.Model):
    part_group=models.ForeignKey(Part_group, on_delete=models.SET_NULL, null=True, blank=True) 
    part=models.CharField(max_length=256,blank=True,null=True) 
        
    def __str__(self):
        return str(self.part)   
    
class Part_detail(models.Model):
    part_no=models.CharField(max_length=256,blank=True,null=True) 
    part_name=models.CharField(max_length=256,blank=True,null=True)  
    def get_upload_path(instance, filename):
        return 'drawings/{0}/{1}'.format(instance.part_name, filename)
    
    Drawing=models.FileField(max_length=256,blank=True,null=True,upload_to=get_upload_path) 
 
   


class Check(models.Model):     
    part = models.ForeignKey(Part, on_delete=models.SET_NULL, null=True, blank=True)     
    checkpoint=models.CharField(max_length=256,blank=True,null=True)
    uom = models.CharField(max_length=256,blank=True,null=True)
    checking_method=models.CharField(max_length=150,blank=True,null=True)
    spec_min=models.FloatField(null=True, blank=True)
    spec_max=models.FloatField(null=True, blank=True)
    Requirement=models.CharField(max_length=256,null=True, blank=True)
  

    def __str__(self):
        return str(self.part.part+self.checkpoint)
    
class Project_code(models.Model):
    project_code=models.CharField(max_length=256,blank=True,null=True)
    part_no=models.CharField(max_length=256,blank=True,null=True)
    Work_order_No= models.IntegerField(blank=True,null=True) 
    Qty=models.IntegerField(blank=True,null=True)
    Operator=models.CharField(max_length=256,blank=True,null=True)
    Machine=models.CharField(max_length=256,blank=True,null=True)
    RM_Coil_No = models.CharField(max_length=256,blank=True,null=True)

      
    
    def __str__(self):
        return str(self.project_code)      

    
class Inspection(models.Model):     
    date=models.DateTimeField(auto_now=True,editable=False,null=True, blank=True) 
    project = models.ForeignKey(Project_code,on_delete=models.SET_NULL,blank=True,null=True)         
    check_point = models.ForeignKey(Check,on_delete=models.SET_NULL,blank=True,null=True) 
    Var_spec_min=models.FloatField(null=True, blank=True)
    Var_spec_max=models.FloatField(null=True, blank=True)     
    Actual=models.FloatField()   
    result_choices=(("Ok","Ok"),("Not_ok","Not_ok"))
    Observation =models.CharField(choices=result_choices,blank=True,null=True,max_length=50)
    Photo=models.FileField(upload_to='Photos',blank=True,null=True)
    Reported_by = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True,related_name="reporter")
    Approved_by=models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True,related_name="approver")
    Remarks =models.CharField(max_length=256,blank=True,null=True)

    def Result(self):
     actual_values = [
        self.Actual,
        
    ]
     valid_actual_values = [value for value in actual_values if value is not None]
     if self.check_point:
        if self.check_point.spec_max is not None and self.check_point.spec_min is not None:
            if valid_actual_values and all(
                self.check_point.spec_min <= value <= self.check_point.spec_max for value in valid_actual_values
            ):
                return "Ok"

        # If spec_max is None, check Var_Spec_Max and Var_Spec_Min
        elif self.Var_spec_max is not None and self.Var_spec_min is not None:
            if valid_actual_values and all(
                self.Var_spec_min <= value <= self.Var_spec_max for value in valid_actual_values
            ):
                return "Ok"
     

     return "Not_Ok"
        
            
    
    def __str__(self):
        return str(self.check_point)
