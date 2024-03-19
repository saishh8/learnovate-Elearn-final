
from django.shortcuts import get_object_or_404, render
from django.contrib import messages
from courses.models import Course
from .models import LearnerCourses


# Create your views here.


def courses(request):

    Courses = Course.objects.all()
    return render(request, 'courses.html', {'Courses': Courses})


def desc(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    has_purchased = LearnerCourses.objects.filter(courses=course, learner=request.user).exists()
    if has_purchased:
        # messages.error(request, 'Passwords do not match.')
        messages.warning(request, 'You have already purchased this course')
    
    context = {
        'course': course,
        'has_purchased': has_purchased
    }
    # context = {'course': course}
    return render(request, 'desc.html', context)


 

# @login_required
# def course_detail(request, course_id):
#     course = Course.objects.get(id=course_id)
#     user = request.user
    

   

#     return render(request, 'course_detail.html', context)