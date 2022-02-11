import xlsxwriter, mimetypes
from datetime import date
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm
from .models import Fest,College,Event,Participated

def home(request):
    context={
        'fests':Fest.objects.all().filter(start_date__gte=date.today()).order_by('start_date')[:3]
    }
    return render(request,'webpage/home.html',context)

def admin_page(request):
    context={
        'fests':Fest.objects.all().filter(start_date__gte=date.today()).order_by('start_date')[:3]
        }
    cur=request.user
    if cur.id!=1:
        
        messages.warning(request,f'You are not authorized to access this page!')
        return redirect('http://localhost:8000/')
    return render(request,'webpage/admin-page.html',context)

@login_required
def college(request):
    context={
        'colleges':College.objects.all()
    }
    return render(request,'webpage/college.html',context)

@login_required
def fest(request,type):
    if type=='ALL':
        context={
            'fests':Fest.objects.all()
        }
        return render(request,'webpage/fest.html',context)
    elif type=='COL':
        context={
        'fests':Fest.objects.filter(fest_type='COL')
        }
        return render(request,'webpage/fest.html',context)
    elif type=='TEC':
        context={
        'fests':Fest.objects.filter(fest_type='TEC')
        }
        return render(request,'webpage/fest.html',context)
    elif type=='CUL':
        context={
        'fests':Fest.objects.filter(fest_type='CUL')
        }
        return render(request,'webpage/fest.html',context)
    else:
        context={
        'fests':Fest.objects.filter(fest_type='SPO')
        }
        return render(request,'webpage/fest.html',context) 

def fest_clg(request,value):
    context={
        'fests':Fest.objects.filter(clg_id=value)
    }
    return render(request,'webpage/fest.html',context)

@login_required
def event(request):
    cur=request.user
    context={
        'events':Event.objects.all(),
        'user': User.objects.get(id=cur.id)
    }
    return render(request,'webpage/event.html',context)

def event_fest(request,value):
    context={
        'events':Event.objects.filter(fest_id=value),
    }
    return render(request,'webpage/event.html',context)

def update_participation(request, user_id, event_id):
        event = Event.objects.get(id=event_id)
        data = Participated(user=user_id, event=event_id)
        ev_date=event.event_date
        if ev_date<date.today():
            cur=request.user
            context={
                    'events':Event.objects.all(),
                    'user': User.objects.get(id=cur.id)
                    }
            messages.warning(request,f'Registration closed for {event.name}, please try next time!')
            return render(request,'webpage/event.html',context)
        data.save()
        participated = Participated.objects.filter(user=user_id)
        history = []
        for partcipate in participated:
            name=Event.objects.get(id=partcipate.event)
            event_name=name.name

            fest=Fest.objects.get(id=name.fest_id.id)
            fest_name=fest.name

            clg=College.objects.get(id=fest.clg_id.id).name
            history.append({'event':event_name,'fest':fest_name,'college':clg})
        messages.success(request,f'You have registered for {event.name}')
        return render(request, 'webpage/my_events.html', context={'history': history})

@login_required
def my_events(request):
    cur=request.user
    participated = Participated.objects.filter(user=cur.id)
    history = []
    for partcipate in participated:
        name=Event.objects.get(id=partcipate.event)
        event_name=name.name

        fest=Fest.objects.get(id=name.fest_id.id)
        fest_name=fest.name

        clg=College.objects.get(id=fest.clg_id.id).name
        history.append({'event':event_name,'fest':fest_name,'college':clg})
    return render(request, 'webpage/my_events.html', context={'history': history})

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,f'Your account has been created! You are now able to login')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'webpage/register.html', {'form': form})

def download_file(request):
    report()
    # fill these variables with real values
    fl_path = 'media/Report.xlsx'
    filename = 'Report.xlsx'

    fl = open(fl_path, 'rb')
    mime_type, _ = mimetypes.guess_type(fl_path)
    response = HttpResponse(fl, content_type=mime_type)
    response['Content-Disposition'] = "attachment; filename=%s" % filename
    return response

def draw_frame_border(workbook, worksheet, first_row, first_col, rows_count, cols_count):

    # top left corner
    worksheet.conditional_format(first_row, first_col,
                                 first_row, first_col,
                                 {'type': 'formula', 'criteria': 'True',
                                  'format': workbook.add_format({'border':2})})
    # top right corner
    worksheet.conditional_format(first_row, first_col + cols_count - 1,
                                 first_row, first_col + cols_count - 1,
                                 {'type': 'formula', 'criteria': 'True',
                                  'format': workbook.add_format({'border':2})})
    # bottom left corner
    worksheet.conditional_format(first_row + rows_count - 1, first_col,
                                 first_row + rows_count - 1, first_col,
                                 {'type': 'formula', 'criteria': 'True',
                                  'format': workbook.add_format({'bottom': 2, 'left': 2})})
    # bottom right corner
    worksheet.conditional_format(first_row + rows_count - 1, first_col + cols_count - 1,
                                 first_row + rows_count - 1, first_col + cols_count - 1,
                                 {'type': 'formula', 'criteria': 'True',
                                  'format': workbook.add_format({'bottom': 2, 'right': 2})})

    # top
    worksheet.conditional_format(first_row, first_col + 1,
                                 first_row, first_col + cols_count - 2,
                                 {'type': 'formula', 'criteria': 'True', 'format': workbook.add_format({'border':2})})
    # left
    worksheet.conditional_format(first_row + 1,              first_col,
                                 first_row + rows_count - 2, first_col,
                                 {'type': 'formula', 'criteria': 'True', 'format': workbook.add_format({'left': 2})})
    # bottom
    worksheet.conditional_format(first_row + rows_count - 1, first_col + 1,
                                 first_row + rows_count - 1, first_col + cols_count - 2,
                                 {'type': 'formula', 'criteria': 'True', 'format': workbook.add_format({'bottom': 2})})
    # right
    worksheet.conditional_format(first_row + 1,              first_col + cols_count - 1,
                                 first_row + rows_count - 2, first_col + cols_count - 1,
                                 {'type': 'formula', 'criteria': 'True', 'format': workbook.add_format({'right': 2})})

def report():
    workbook=xlsxwriter.Workbook('C:/Users/Gagan Karanth/Desktop/dbms/media/Report.xlsx')
    worksheet=workbook.add_worksheet()
    cell_format=workbook.add_format()
    cell_format.set_bold()
    cell_format.set_font_size(14)
    date_format = workbook.add_format({'num_format':'yyyy-mm-dd'})
    time_format = workbook.add_format({'num_format':'hh:mm'})
    worksheet.write('B2','College',cell_format)
    worksheet.write('C2','Fests',cell_format)
    worksheet.write('D2','Start Date',cell_format)
    worksheet.write('E2','End Date',cell_format)
    worksheet.set_column('D:F', 14)
    worksheet.set_column('B:C', 22)
    k=3
    row=3
    for i in range(College.objects.all().count()):
        row=k
        col=College.objects.filter(id=i+1)
        worksheet.write('B'+str(row),col.first().name)
        fes=Fest.objects.filter(clg_id=col.first().id)
        for j in fes:
            worksheet.write('C'+str(k),j.name)
            worksheet.write('D'+str(k),j.start_date,date_format)
            worksheet.write('E'+str(k),j.end_date,date_format)
            k+=1 
    k1=k    
    draw_frame_border(workbook,worksheet,1,1,k-2,4)
    k+=2
    worksheet.write('B'+str(k),'Fest',cell_format)
    worksheet.write('C'+str(k),'Events',cell_format)
    worksheet.write('D'+str(k),'Date',cell_format)
    worksheet.write('E'+str(k),'Time',cell_format)
    worksheet.write('F'+str(k),'Entry Fee',cell_format)
    k+=1  
    for i in range(Fest.objects.all().count()):
        row=k
        fes=Fest.objects.filter(id=i+1)
        worksheet.write('B'+str(row),fes.first().name)
        ev=Event.objects.filter(fest_id=fes.first().id)
        for j in ev:
            worksheet.write('C'+str(k),j.name)
            worksheet.write('D'+str(k),j.event_date,date_format)
            worksheet.write('E'+str(k),j.event_time,time_format)
            worksheet.write('F'+str(k),j.entry_fee)
            k+=1
    draw_frame_border(workbook,worksheet,k1+1,1,k-k1-2,5)
    workbook.close()



