from datetime import date,datetime
from django.http import Http404, HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from courses.forms import UploadForm
from courses.forms import CourseEditForm

from courses.forms import CourseCreateForm
from .models import Course,Category, Slider, UploadModel
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required,user_passes_test



#forms
#GET => url = querystring
#POST 

 

def index(request):
    kurslar = Course.objects.filter(isActive=1 , isHome=1)
    kategoriler = Category.objects.all()
    slider = Slider.objects.filter(isActive=True)

    return render(request,'courses/index.html' , {
        'categories' : kategoriler,
        'courses' : kurslar,
        "sliders" : slider,
    })


def isAdmin(user):
    return user.is_superuser

@user_passes_test(isAdmin)
def create_course(request):
       
        if request.method == 'POST':
             form = CourseCreateForm(request.POST,request.FILES)

             if form.is_valid():
                  form.save()
                  return redirect('/kurslar')
    
        else:
            form = CourseCreateForm()
       
        return render(request,'courses/create-course.html',{'form':form})


@login_required()
def course_list(request):
    kurslar = Course.objects.all()
    return render(request,'courses/course-list.html' , {
        'courses' : kurslar,
    })

def course_edit(request,id):
    course = get_object_or_404(Course,pk=id)


    if request.method == 'POST':
         form = CourseEditForm(request.POST,request.FILES,instance=course,)
         form.save()
         return redirect('course_list')
    else:
        form = CourseEditForm(instance=course)
         

    return render(request,'courses/edit-course.html',{'form': form})


def course_delete(request,id):
    course = get_object_or_404(Course,pk=id)

    if request.method == 'POST':
        course.delete()
        return redirect('course_list')

    return render(request,'courses/course-delete.html',{'course':course})


def upload(request):
    if request.method == 'POST':
        form = UploadForm(request.POST,request.FILES)

        if form.is_valid():
            model = UploadModel(image=request.FILES.get('image'))
            model.save()
            return render(request,'courses/success.html')
    else:
        form = UploadForm()
    return render(request,'courses/upload.html',{'form':form})






    


def search(request):
    if 'q' in request.GET and request.GET['q'] != '':
        q = request.GET['q']
        kurslar=Course.objects.filter(isActive=1,title__contains=q).order_by('date')
        kategoriler=Category.objects.all()
    else:
        return redirect('/kurslar')


    return render(request,'courses/search.html',{
        'categories' : kategoriler,
        'courses' : kurslar,
    })


def details(request,slug):
    

    course = get_object_or_404(Course, slug=slug)
    
    context={
        'course':course
    }
    return render(request,'courses/details.html',context)

def getCoursesByCategory(request,slug):
    kurslar=Course.objects.filter(categories__slug=slug,isActive=1).order_by('date')
    kategoriler=Category.objects.all()

    paginator = Paginator(kurslar, 2)
    page = request.GET.get('page',1)
    page_obj = paginator.page(page)

    return render(request,'courses/list.html',{
        'categories' : kategoriler,
        'page_obj' : page_obj,
        'seciliKategori' : slug
    })
   



