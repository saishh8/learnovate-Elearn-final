from django.shortcuts import get_object_or_404, render, redirect
from django.utils.datastructures import MultiValueDictKeyError
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.contrib.auth.hashers import make_password
from .models import Course, Course_Videos, Quiz, QuizMCQOption, QuizQuestion, User, Instructor
# from accounts.context_processors import instructor_validation.is_instructor

# Create your views here.


from .models import *
# Create your views here.


def CreateCourse(request):

    if request.method == 'POST':
        title = request.POST.get('title')
        cat = request.POST.get('category')
        desc = request.POST.get('desc')
        wtl = request.POST.get('whattolearn')
        price = int(request.POST.get('price'))
        thumbnail = request.FILES['thumbnail']
        v1 = request.FILES['v1']
        v2 = request.FILES['v2']
        v3 = request.FILES['v3']
        v4 = request.FILES['v4']
        v5 = request.FILES['v5']

        

        # category = Category(category_name= cat)
        # category.save()

        if request.user.instructor.is_validated:

            try:

                course = Course(title=title, description=desc, what_to_learn=wtl,
                                thumbnail=thumbnail, price=price, category=cat, instructor=request.user)
                course.full_clean()
                course.save()

                video1 = Course_Videos(title=v1.name, video=v1, course=course)
                video1.full_clean()
                video1.save()
                video2 = Course_Videos(title=v2.name, video=v2, course=course)
                video2.full_clean()
                video2.save()
                video3 = Course_Videos(title=v3.name, video=v3, course=course)
                video3.full_clean()
                video3.save()
                video4 = Course_Videos(title=v4.name, video=v4, course=course)
                video4.full_clean()
                video4.save()
                video5 = Course_Videos(title=v5.name, video=v5, course=course)
                video5.full_clean()
                video5.save()

# create quiz
                quizTitle=request.POST.get('quizTitle')
                #points=request.POST.get('points')
                quiz = Quiz.objects.create(title=quizTitle, course=course)

                for i in range(1,6):
                    questionText=request.POST.get(f'question_{i}')
                    marks=request.POST.get(f'marks_{i}')
                    questionobj = QuizQuestion.objects.create(quiz=quiz, question=questionText, marks=marks)

                    is_correct=True
                    answerText=request.POST.get(f'question_{i}_correct')
                    if answerText:
                        answer = QuizMCQOption.objects.create(question=questionobj, option=answerText, is_correct=is_correct)
                    
                    for j in range(1,4):
                        is_correct=False
                        #ques=f'question_{i}'
                        answerText=request.POST.get(f'question_{i}_incorrect_{j}')
                        if answerText:
                            answer = QuizMCQOption.objects.create(question=questionobj, option=answerText, is_correct=is_correct)
                        else:
                            print("something")



                messages.error(request, 'Course Created Successfully')

            except MultiValueDictKeyError:
                messages.error(request, 'Add all videos.')
                return redirect('/')

        else:
            messages.error(request, 'Your account is not validated')
            return redirect('/')

    return render(request, 'create_course.html')
