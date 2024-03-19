"""authverify URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.Home,name='home'),
    path('home', views.Home),
    path('iregister', views.RegisterInstructor, name='iregister'),
    path('lregister', views.RegisterLearner, name='lregister'),
    path('login', views.Login, name='login'),
    # path('login/', auth_views.LoginView.as_view(), name='login'), #sus
    path('logout', views.LogoutView, name='logout'),
    path('learnerprofile',views.LearnerProfile, name="lprofile"),
    # path('learner',views.LearnerAcc),

    path('instructordash', views.InstructorDash, name='dashins'),
    path('createcourse', include('courses.urls')),
    path('inscourses', views.inscourses, name='inscourses'),

    path('courses', include('learner.urls')),
    path('mycourses',views.MyCourse,name = "mycourse"),
    path('mycourses/<int:course_id>/', views.CourseVideo, name='vid'),
    path('update_videos/', views.update_videos, name='update_videos'),

    path('cart', include('cart.urls')),

    path('api/get-quiz/',views.get_quiz, name='get_quiz'),
    path('quiz/<int:course_id>/',views.quiz, name ='quiz'),
    path('quizhome/',views.ho, name ='quizHome'),
    #path('api/quiz-result/', views.quiz_result, name='quiz-result'),
    path('submit-quiz/', views.submit_quiz, name='submit-quiz'),


     

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
