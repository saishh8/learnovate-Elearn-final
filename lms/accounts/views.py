from random import shuffle
from django.http import HttpResponse, HttpResponseNotAllowed
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login , logout
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.contrib.auth.hashers import make_password
from .models import User, Instructor
from courses.models import Course, Course_Videos, Quiz, QuizQuestion, QuizResultModel
from learner.models import LearnerCourses, LearnerVideo
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
# Create your views here.
# def SetSession(request):
#     request.session['name']='Saish'
#     return render(request,'setSession.html')

# def GetSession(request):
#     name=request.session.get('name',default='Guest')
#     return render(request,'getSession.html',{'name':name})

# def DelSession(request):
#     if 'name' in request.session:
#         del request.session['name']

#     return render(request,'delSession.html')

@csrf_exempt
def RegisterInstructor(request):
    
    if request.method == "POST":
        
        first_name = request.POST.get('fname')
        last_name = request.POST.get('lname')
        email = request.POST.get('email')
        password = request.POST.get('passwd')
        cpassword = request.POST.get('confirmPasswd')
        resume= request.FILES['file']
        linkedin_url = request.POST.get('linkedin')
        try:
            validate_email(email)
        except ValidationError:
            messages.error(request, 'Invalid email address.')
            return redirect('iregister')
        if password != cpassword:
            messages.error(request, 'Passwords do not match.')
            return redirect('iregister')
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email address is already taken.')
            return redirect('iregister')
        
        user = User.objects.create_instructor(email=email, password=password, first_name=first_name, last_name = last_name)
        
        instructor = Instructor.objects.create(email=user, linked_in_url=linkedin_url, resume=resume)
        instructor.save()
        login(request, user)
        return redirect("dashins") #redirect to instructor dashboard
    else:

        

        return render(request,'instructor_register.html')

@csrf_exempt
def Login(request):

    
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('passwd')

       
        # Authenticate the user
        user = authenticate(request, username=email, password=password)
        print(user)
        
        

        # If user is authenticated, log them in and redirect to home page
        if user is not None:
            login(request, user)
            print("<red>Authenticated User ID:</red>", user.id)  # Print authenticated user ID



            
            user_id = request.session.get('_auth_user_id')
            if user_id:
                user = User.objects.get(pk=user_id)
                print("Authenticated User ID:", user_id)
            else:
                print("User is not authenticated")




            return redirect("dashins" if user.is_instructor else "/")  # Redirect based on user type
        else:
            print("<red>User is not authenticated</red>")  # Print user authentication status
            return redirect("/")  # Redirect to home page if authentication fails
             
    else:
        return render(request, 'login.html')

def Home(request):
    
    latest_courses = Course.objects.all().order_by('-upload_date')[:3]
    context = {'latest_courses': latest_courses}
    return render(request, 'index.html', context)


# def UserAcc(request):

#      return render(request,'usercc.html')

# def LearnerAcc(request):

#      return render(request,'user.html')


def RegisterLearner(request):
    
    if request.method == "POST":
        
        first_name = request.POST.get('fname')
        last_name = request.POST.get('lname')
        email = request.POST.get('email')
        password = request.POST.get('passwd')
        cpassword = request.POST.get('confirmPasswd')
       
        try:
            validate_email(email)
        except ValidationError:
            messages.error(request, 'Invalid email address.')
            return redirect('lregister')
        if password != cpassword:
            messages.error(request, 'Passwords do not match.')
            return redirect('lregister')
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email address is already taken.')
            return redirect('lregister')
        
        user = User.objects.create_learner(email=email, password=password, first_name=first_name, last_name = last_name)
        
        login(request, user)
        return redirect("/")
    else:

        

        return render(request,'learner_register.html')
    



def LogoutView(request):
    logout(request)
    return redirect('/')


def InstructorDash(request):

    courseCount= Course.objects.filter(instructor=request.user)
    count =  courseCount.count()
    return render(request,'instructor_dash.html',{'count':count})



def LearnerProfile(request):
     courseCount= LearnerCourses.objects.filter(learner=request.user)
     count =  courseCount.count()
     return render(request,'learner_profile.html',{'count':count})


def MyCourse(request):
   
    learner_courses = LearnerCourses.objects.filter(learner = request.user).select_related('courses')
    # Courses = Course.objects.filter(id = learner_courses.id)
    return render(request, 'learner_courses.html', {'learner_courses': learner_courses}) 


def CourseVideo(request,course_id):

    course = get_object_or_404(Course, id=course_id)
    videos = Course_Videos.objects.filter(course=course)
    quiz_completed = QuizResultModel.objects.filter(user=request.user, course=course, is_completed=True).exists()
    context = {'video': videos,'course':course, 'quiz_completed': quiz_completed}
    return render(request, 'video_panel.html', context)

def update_videos(request):
    if request.method == 'POST':
        video_ids = request.POST.getlist('video_ids')
        for video_id in video_ids:
            video = Course_Videos.objects.get(id=video_id)
            learner_video, created = LearnerVideo.objects.get_or_create(
                learner=request.user,
                video=video,
            )
            if created:
                learner_video.is_completed = True
                learner_video.save()
        return redirect(request.META.get('HTTP_REFERER'))
    
    else:
        return render(request,"video_panel.html")
    
 
#quiz
def ho(request):
    context={'courses':Course.objects.all()}
    if request.GET.get('course'):
        return redirect(f"/quiz/?course={request.GET.get('course')}")
    return render(request,'quizHome.html',context)

def quiz(request,course_id):
    #context = {'course':request.GET.get('course')}
    course = get_object_or_404(Course, id=course_id)
    context={'course':course}
    return render(request,'quiz.html',context)


def get_quiz(request):
    try:
        question_objs = QuizQuestion.objects.all()
        if request.GET.get('course'):
            question_objs=question_objs.filter(quiz__course__title__exact=request.GET.get('course'))

        question_objs=list(question_objs)
        print(question_objs)
        shuffle(question_objs)

        data=[]
        for question_obj in question_objs:
            data.append({
                'id':question_obj.id,
                'quiz' : question_obj.quiz.title,
                'question' : question_obj.question,
                'marks' : question_obj.marks,
                'answers':question_obj.get_answers()
            })
        
        payload={'status' : True, 'data' : data}

        return JsonResponse(payload)
    

        
    except Exception as e:
        print(e)
    return HttpResponse("something went wrong")


@csrf_exempt
@login_required
def submit_quiz(request):
    if request.method == 'POST':
        score = request.POST.get('score')
        course = request.POST.get('course')
        #quizobj = Quiz.objects.get(course__title=course)
        #quizobj.is_completed = True
        is_completed=True
        quiz_result = QuizResultModel(user=request.user, course=course, score=score,is_completed=is_completed)
        quiz_result.save()        
        #quizobj.save()
        

        response = {'status': 'success', 'message': 'Quiz result submitted successfully.'}
        return JsonResponse(response)
        #return render(request,'index.html')

    else:
        response = {'status': 'error', 'message': 'Invalid request method.'}
        return JsonResponse(response)

    
def inscourses(request):
    # Retrieve the courses created by the current user (assuming they're an instructor)
    courses = Course.objects.filter(instructor=request.user)

    # Calculate enrollment and revenue for each course
    for course in courses:
        enrollment = LearnerCourses.objects.filter(courses=course).count()
        revenue = enrollment * course.price
        course.total_enrollment = enrollment
        course.total_revenue = revenue

    # Render the template with the courses
    return render(request, 'inscourses.html', {'courses': courses})
