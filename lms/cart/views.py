import datetime
from http import client
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from learner.models import LearnerCourses
from courses.models import Course
from .models import Cart,Order
import razorpay
import hmac
import hashlib

from django.views.decorators.csrf import csrf_exempt


@login_required
def add_to_cart(request, course_id):
    course = Course.objects.get(id=course_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart.courses.add(course)
    return redirect('cart')


@login_required
def remove_from_cart(request, course_id):
    course = Course.objects.get(id=course_id)
    cart = Cart.objects.get(user=request.user)
    cart.courses.remove(course)
    return redirect('cart')


@login_required
def cart(request):
    cart = Cart.objects.filter(user=request.user).first()
    if cart:
        courses = cart.courses.all()
        total_price = cart.total_price()
    else:
        courses = None
        total_price = 0
    return render(request, 'cart.html', {'courses': courses, 'total_price': total_price})


razorpay_client = razorpay.Client(
    auth=("rzp_test_02ojyOxXeuKp1x", "h4WTKVgkRT74P1f0fc9JL7Ox"))


def checkout(request):
    cart = Cart.objects.get(user=request.user)
    total_price = cart.total_price()
    order_amount = int(total_price * 100)
    order_currency = 'INR'
    order_receipt = 'order_receipt_' + str(cart.id)

    response = razorpay_client.order.create(
        dict(amount=order_amount, currency=order_currency, receipt=order_receipt))

    order_id = response['id']

    return render(request, 'checkout.html', {'order_id': order_id, 'order_amount': order_amount, 'order_currency': order_currency})

from learner.models import LearnerCourses

from .models import Cart


@csrf_exempt
def payment_confirmation(request):

    print(request.user.id)

    # Inspect session data to verify user authentication
    if request.user.is_authenticated:
        user = request.user
        print("Authenticated User ID:", user.id)
    else:
        print("User is not authenticated")

    
    user_id = request.session.get('_auth_user_id')
    if user_id:
        user = User.objects.get(pk=user_id)
        print("Authenticated User ID:", user_id)
    else:
        print("User is not authenticated")


    cart = get_object_or_404(Cart, user=request.user.id) #issue
    
    if request.method == 'POST':
        razorpay_payment_id = request.POST.get('razorpay_payment_id')
        razorpay_order_id = request.POST.get('razorpay_order_id')
        razorpay_signature = request.POST.get('razorpay_signature')

        expected_signature = hmac.new("h4WTKVgkRT74P1f0fc9JL7Ox".encode(
        ), f'{razorpay_order_id}|{razorpay_payment_id}'.encode(), digestmod=hashlib.sha256).hexdigest()

        if expected_signature == razorpay_signature:
            # Payment is successful
            # Update the cart and order status here

            # Add the courses to the learner's account
            for course in cart.courses.all():
                LearnerCourses.objects.get_or_create(courses=course, learner=request.user)

            # Remove the courses from the cart
            cart.courses.clear()

            # Save the cart object to update it in the database
            cart.save()

            return render(request, 'payment_success.html')
        else:
            # Payment failed
            return render(request, 'payment_failure.html')
    else:
        return redirect('cart')

    #cart = Cart.objects.get(user=request.user)
    # cart = get_object_or_404(Cart, user=request.user)
    # if request.method == 'POST':
    #     razorpay_payment_id = request.POST.get('razorpay_payment_id')
    #     razorpay_order_id = request.POST.get('razorpay_order_id')
    #     razorpay_signature = request.POST.get('razorpay_signature')

    #     expected_signature = hmac.new("BjXf30hxxojxeWJwqTEow7XO".encode(
    #     ), f'{razorpay_order_id}|{razorpay_payment_id}'.encode(), digestmod=hashlib.sha256).hexdigest()

    #     if expected_signature == razorpay_signature:
    #         # Payment is successful
    #         # Update the cart and order status here

    #         # add the courses to the learner's account
    #         learner_id = request.user.id
    #         for course in cart.courses.all():
    #             LearnerCourses.objects.create(courses=course, learner_id=learner_id)

    #         # delete the courses from the cart
    #         cart.courses.clear()

    #         # save the cart object to update it in the database
    #         cart.save()

    #         return render(request, 'payment_success.html')
    #     else:
    #         # Payment failed
    #         return render(request, 'payment_failure.html')
    # else:
    #     return redirect('cart')


'''
def add_course_to_learner(learner_id, course_id):
    # Get the learner object
    learner = get_object_or_404(Learner, id=learner_id)
    
    # Get the course object
    course = get_object_or_404(Course, id=course_id)
    
    # Create a new LearnerCourses object
    LearnerCourses.objects.create(learner=learner, course=course)

@csrf_exempt
def payment_confirmation(request):
    #cart = Cart.objects.get(user=request.user)
    cart = get_object_or_404(Cart, user=request.user)
    if request.method == 'POST':
        razorpay_payment_id = request.POST.get('razorpay_payment_id')
        razorpay_order_id = request.POST.get('razorpay_order_id')
        razorpay_signature = request.POST.get('razorpay_signature')

        expected_signature = hmac.new("BjXf30hxxojxeWJwqTEow7XO".encode(
        ), f'{razorpay_order_id}|{razorpay_payment_id}'.encode(), digestmod=hashlib.sha256).hexdigest()

        if expected_signature == razorpay_signature:
            # Payment is successful
            # Update the cart and order status here

            # delete the courses from the cart
            cart.courses.clear()

    # save the cart object to update it in the database
            cart.save()

            return render(request, 'payment_success.html')
        else:
            # Payment failed
            return render(request, 'payment_failure.html')
    else:
        return redirect('cart')


def add_course_to_learner(request, course_id):
    # get the learner from the request
    learner = request.user.learner
    # create a new LearnerCourses object and save it
    learner_course = LearnerCourses(learner=learner, course_id=course_id)
    learner_course.save()
    # redirect to the learner dashboard
    return redirect('learner_dashboard')


@csrf_exempt
def payment_confirmation(request):
    if request.method == "POST":
        order_id = request.POST['razorpay_order_id']
        payment_id = request.POST['razorpay_payment_id']
        signature = request.POST['razorpay_signature']
        order = Order.objects.get(id = id)
        params_dict = {
            'razorpay_order_id': order_id,
            'razorpay_payment_id': payment_id,
            'razorpay_signature': signature
        }
        # verify the payment signature
        try:
            status = client.utility.verify_payment_signature(params_dict)
            if status == None:
                # update the order status to successful
                order.status = 'successful'
                order.save()
                # add the course to the learner account
                cart = Cart.objects.get(id=request.session['cart_id'])
                for item in cart.cartitem_set.all():
                    add_course_to_learner(request, item.course.id)
                # delete the cart
                cart.delete()
                return render(request, 'payment_success.html')
        except:
            return render(request, 'payment_failure.html')
    

'''