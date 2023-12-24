from django.shortcuts import render,redirect
from .models import Inspection,Part,Check,Inspection,Part_group,Part_detail
from django.forms import inlineformset_factory,modelformset_factory
from .forms import Project_Form,LoginForm,Inspform,PartDetailForm,DrawingSearchForm
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required,permission_required
from django.views.generic import ListView,DeleteView,UpdateView,CreateView
from django.contrib import messages
import datetime
from django.http import JsonResponse

def logout_view(request):
    logout(request)
    return redirect('/')

def login_view(request):
    error_message=None
    form=LoginForm()
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid:
            username =form.data.get("username")
            password=form.data.get("password")
            user = authenticate(username=username,password=password)
            if user is not None:
                login(request,user)
                if request.GET.get("next"):
                    return redirect(request.GET.get('next'))
                else:
                    return redirect ('/')
            else:
                error_message="Not Authorised to View/Update reports"
    return render(request,'login.html',{'form':form,'error_message':error_message})


def part_group(request):
    part_group=Part_group.objects.all()
    context={"part_group":part_group}
    return render(request,'partgrouplist.html',context)

def part_list(request,pk):
    parts = Part.objects.filter(part_group__id=pk)
    context={"parts":parts}
    return render(request,'partlist.html',context)


@login_required
@permission_required('Permission', raise_exception=True)
def part_detail(request, pk):
    part_ob = Part.objects.get(id=pk)
    checks = Check.objects.filter(part=part_ob)
    count = len(checks)
    drawing_search_form = DrawingSearchForm(request.GET)
    part_no_query = drawing_search_form['part_no'].value()
    if part_no_query:
        drawings = Part_detail.objects.filter(part_no=part_no_query)
    else:
        drawings = None
    
    formset=None
 

    form1 = Project_Form()
  
    InspFormSet = inlineformset_factory(Check, Inspection, extra=count, fields=('Var_spec_min', 'Var_spec_max', 'Actual', 'Remarks', 'Observation', 'Photo'), can_delete=False, labels='')

    if request.method == "POST":
        if 'drawing_search_submit' in request.POST:
            drawings = Part_detail.objects.filter(part_no__icontains=part_no_query)
            

        elif 'inspection_submit' in request.POST:
            # Handle inspection form submission
            formset = InspFormSet(request.POST, request.FILES, queryset=Inspection.objects.filter(check_point__part=part_ob))
            form1 = Project_Form(request.POST)

            if form1.is_valid() and formset.is_valid():
                form1 = form1.save()
                instances = formset.save(commit=False) 
            
                for instance, check in zip(instances, checks):
                    instance.check_point = check
                    instance.Reported_by = request.user
                    instance.project = form1
                    # Only use Var_spec_min and Var_spec_max if spec_min and spec_max are None
                    if check.spec_min is None and check.spec_max is None:
                        instance.Var_spec_min = check.Var_spec_min
                        instance.Var_spec_max = check.Var_spec_max                   
                    instance.save()
                       
                           

                return redirect("part_group")  # Redirect to the appropriate URL after form submission

    else:
        formset = InspFormSet(queryset=Inspection.objects.filter(check_point__part=part_ob))
    
    context = {'formset': formset, 'checks': checks, 'part': part_ob, 'form1': form1, 'drawing_search_form': drawing_search_form, 'drawings': drawings}
    return render(request, "partdetail.html", context)


@login_required
@permission_required('Permision', raise_exception=True)
def Insp_view(request):
    search_form1 = Inspform()  
    Insp_qs1 = None

    if request.method == 'POST':
        fromDate = request.POST.get('fromDate', None)
        toDate = request.POST.get('toDate', None)
        
        # Check if fromDate and toDate are not empty
        if fromDate and toDate:
            try:
                # Convert the date strings to datetime objects
                from_date = datetime.datetime.strptime(fromDate, '%Y-%m-%d')
                to_date = datetime.datetime.strptime(toDate, '%Y-%m-%d')
                
                # Filter the queryset based on the date range
                Insp_qs1 = Inspection.objects.filter(date__range=[from_date, to_date])
                approved_by_user = request.user
                Insp_qs1.update(Approved_by=approved_by_user)
            except ValueError:
                # Handle invalid date format
                # You might want to display an error message to the user
                pass
            
            

    context = {
        'search_form1': search_form1,
        'Insp_qs1': Insp_qs1,
    }
    return render(request, 'insp.html', context)







def input_num_extra_forms(request):
    if request.method == 'POST':
        num_extra_forms = int(request.POST.get('num_extra_forms', 1))
        return redirect('upload_drawings', num_extra_forms=num_extra_forms)
    else:
        return render(request, 'input_num_extra_forms.html')

def upload_drawings(request, num_extra_forms):
    PartDetailFormSet = modelformset_factory(Part_detail, form=PartDetailForm, extra=num_extra_forms)

    if request.method == 'POST':
        formset = PartDetailFormSet(request.POST, request.FILES, queryset=Part_detail.objects.none())

        if formset.is_valid():
            instances = formset.save(commit=False)

            for instance in instances:
                # Perform any additional processing before saving (if needed)
                instance.additional_integer = int(request.POST.get('additional_integer', 0))
                instance.save()

            return redirect("part_group") 
        else:
            errors = formset.errors
            return JsonResponse({'message': 'Formset is not valid', 'errors': errors}, status=400)

    else:
        formset = PartDetailFormSet(queryset=Part_detail.objects.none())
        return render(request, 'upload_drawings.html', {'formset': formset, 'num_extra_forms': num_extra_forms})

     

              

    



  