from django.conf import settings
from django.shortcuts import get_object_or_404

from .models import Instructor


def instructor_validation(request):
    is_instructor = False
    is_validated = False

    if request.user.is_authenticated and request.user.is_instructor:
        is_instructor = True
        instructor = get_object_or_404(Instructor, email=request.user)
        is_validated = instructor.is_validated

    return {
        'is_instructor': is_instructor,
        'is_validated': is_validated,
    }