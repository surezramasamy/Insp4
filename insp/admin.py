from django.contrib import admin
from import_export import fields, resources
from .models import Part,Check,Inspection,Part_group,Part_detail
from import_export.widgets import ForeignKeyWidget
from import_export.admin import ImportExportModelAdmin

class Resource_Insp(resources.ModelResource):
    part= fields.Field(column_name='part',attribute='part',widget=ForeignKeyWidget(Part, 'part'))
    
    class Meta:
        model = Check
    fields=('part','checkpoint','uom','checking_method','spec_min','spec_max','Requirement')
    export_order=('part','checkpoint','uom','checking_method','spec_min','spec_max','Requirement')


class Admin(ImportExportModelAdmin,admin.ModelAdmin):
    resource_class = Resource_Insp  
    
    list_display = ['part','checkpoint','uom','checking_method','spec_min','spec_max','Requirement']
    list_editable = ['checkpoint','uom','checking_method','spec_min','spec_max','Requirement']



class Admin1(admin.ModelAdmin):  
    def Part(self, obj):
        try:
            return obj.check_point.part.part
        except:
            return "-"          
    def Check(self, obj):
        try:
            return obj.check_point.checkpoint
        except:
            return "-"
    def UOM(self, obj):
        try:
            return obj.check_point.uom
        except:
            return"-"
    def Checking_Method(self, obj):
        try:
            return obj.check_point.checking_method
        except:
            return"-"
    def Spec_min(self, obj):
        try:
            return obj.check_point.spec_min
        except:
            return"-" 
    def Spec_max(self, obj):
        try:
            return obj.check_point.spec_max 
        except:
            return"-" 
    def Requirement(self, obj):
        try:
            return obj.check_point.Requirement 
        except:
            return"-"
    def Work_Order_No(self, obj):
        try:
            return obj.project.Work_order_No
        except:
            return"-"
    def Qty(self, obj):
        try:
            return obj.project.Qty
        except:
            return"-"
    def Machine(self, obj):
        try:
            return obj.project.Machine
        except:
            return"-"
    def Operator(self, obj):
        try:
            return obj.project.Operator
        except:
            return"-"
    def RM_Coil_No(self, obj):
        try:
            return obj.project.RM_Coil_No
        except:
            return"-"
    

    
    list_display = ['date','project','Work_Order_No','Qty','Machine',
                    'Operator','RM_Coil_No','Part','Check','UOM','Checking_Method',
                    'Spec_min','Spec_max','Var_spec_min','Var_spec_max','Actual',
                    'Result','Remarks','Requirement','Observation','Photo','Reported_by','Approved_by']
    

class Admin2(admin.ModelAdmin):   
    list_display = ['part','part_group']

class Admin3(admin.ModelAdmin):     
    list_display = ['part_no','part_name','Drawing']


admin.site.register(Part_group)
admin.site.register(Part,Admin2)
admin.site.register(Check,Admin)
admin.site.register(Inspection,Admin1)
admin.site.register(Part_detail,Admin3)
