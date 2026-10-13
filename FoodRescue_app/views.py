from django.shortcuts import render,redirect
from .models import Register,Food, Order
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test

from django.contrib.auth.decorators import login_required

# Create your views here.
from django.http import HttpResponse

def home(request):
    return render(request, 'FoodRescue_app/home.html')

def login(request):
    return render(request,'FoodRescue_app/login.html')

def register(request):
    return render(request, 'FoodRescue_app/register.html')

from django.shortcuts import render, redirect
from .models import Register

def register(request):

    if request.method == 'POST':
        role = request.POST['role']

        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        username = request.POST['username']
        password = request.POST['password']

        Register.objects.create(
            name=name,
            email=email,
            phone=phone,
            username=username,
            password=password,
            role=role

        )

        return redirect('login')

    return render(request, 'FoodRescue_app/register.html')

from django.shortcuts import render, redirect
from .models import Register


def login(request):
    if request.method == 'POST':

        username = request.POST['username']
        password = request.POST['password']

        user = Register.objects.filter(
            username=username,
            password=password
        ).first()

        if user:

            # Save username in session
            request.session['username'] = user.username

            if user.role == 'hotel':
                return redirect('hotel_dashboard')

            elif user.role == 'customer':
                return redirect('customer_dashboard')
            elif user.role == 'delivery':
                return redirect('delivery_dashboard')

        else:
            return render(
                request,
                'FoodRescue_app/login.html',
                {'msg': 'Invalid Username or Password'}
            )

    return render(
        request,
        'FoodRescue_app/login.html'
    )



def userhome(request):
    return render(
        request,
        'FoodRescue_app/userhome.html'
    )

def hotel_dashboard(request):
    return render(
        request,
        'FoodRescue_app/hotel_dashboard.html'
    )

def hotel_orders(request):
    orders = Order.objects.all()

    return render(
        request,
        'FoodRescue_app/hotel_orders.html',
        {'orders': orders}
    )

def customer_dashboard(request):
    return render(
        request,
        'FoodRescue_app/customer_dashboard.html'
    )

def add_food(request):

    if request.method == 'POST':

        username = request.session.get('username')

        hotel = Register.objects.filter(
            username=username,
            role='hotel'
        ).first()

        if not hotel:
            return redirect('login')

        name = request.POST['name']
        category = request.POST['category']
        quantity = request.POST['quantity']
        price = request.POST['price']
        available_time = request.POST['available_time']
        description = request.POST['description']
        image = request.FILES.get('image')

        Food.objects.create(
            hotel=hotel,
            name=name,
            category=category,
            quantity=quantity,
            price=price,
            available_time=available_time,
            description=description,
            image=image
        )

        return redirect('hotel_food')

    return render(
        request,
        'FoodRescue_app/add_food.html'
    )

def edit_food(request, food_id):
    food = Food.objects.get(id=food_id)

    if request.method == 'POST':
        food.name = request.POST['name']
        food.category = request.POST['category']
        food.quantity = request.POST['quantity']
        food.price = request.POST['price']
        food.available_time = request.POST['available_time']
        food.description = request.POST['description']

        if request.FILES.get('image'):
            food.image = request.FILES.get('image')

        food.save()

        return redirect('hotel_food')

    return render(
        request,
        'FoodRescue_app/edit_food.html',
        {'food': food}
    )


def delete_food(request, food_id):
    food = Food.objects.get(id=food_id)
    food.delete()

    return redirect('hotel_food')



def my_orders(request):
    if 'username' not in request.session:
        return redirect('login')

    username = request.session['username']

    orders = Order.objects.filter(
        customer_name=username
    ).order_by('-order_date')

    return render(request, 'FoodRescue_app/my_orders.html', {
        'orders': orders
    })


from django.shortcuts import render, redirect, get_object_or_404
from .models import Food, Order

def place_order(request, food_id):

    username = request.session.get('username')

    if not username:
        return redirect('login')

    food = Food.objects.get(id=food_id)

    if request.method == 'POST':

        customer_name = request.POST['customer_name']
        quantity = int(request.POST['quantity'])
        

        if quantity <= 0:
            return render(
                request,
                'FoodRescue_app/place_order.html',
                {
                    'food': food,
                    'msg': 'Please enter a quantity greater than zero.'      
                }
            )

        total_price = food.price * quantity

        Order.objects.create(
            food=food,
            customer_name=customer_name,
            quantity=quantity,
            total_price=total_price
        )

        food.quantity -= quantity
        food.save()

        return redirect('my_orders')

    return render(
        request,
        'FoodRescue_app/place_order.html',
        {'food': food}
    )


def logout(request):
    request.session.flush()
    return redirect('login')

def available_food(request):
    foods = Food.objects.all()

    return render(
        request,
        'FoodRescue_app/available_food.html',
        {'foods': foods}
    )
def hotel_food(request):
    username = request.session.get('username')

    if not username:
        return redirect('login')

    hotel = Register.objects.filter(
        username=username,
        role='hotel'
    ).first()

    if not hotel:
        return redirect('login')

    foods = Food.objects.filter(hotel=hotel)

    return render(
        request,
        'FoodRescue_app/hotel_food.html',
        {'foods': foods}
    )

def update_order_status(request, order_id):

    order = Order.objects.get(id=order_id)

    if request.method == 'POST':

        status = request.POST['status']

        order.status = status
        order.save()

    return redirect('hotel_orders')

def admin_only(user):
    return user.is_authenticated and user.is_superuser



def delivery_dashboard(request):

    username = request.session.get('username')

    if not username:
        return redirect('login')

    delivery_partner = Register.objects.filter(
        username=username,
        role='delivery'
    ).first()

    if not delivery_partner:
        return redirect('login')

    # New confirmed orders that nobody has accepted
    new_orders = Order.objects.filter(
        status='Confirmed',
        delivery_partner__isnull=True
    ).order_by('-order_date')

    # Orders already accepted by this delivery partner
    my_orders = Order.objects.filter(
        delivery_partner=delivery_partner
    ).order_by('-order_date')

    return render(
        request,
        'FoodRescue_app/delivery_dashboard.html',
        {
            'new_orders': new_orders,
            'my_orders': my_orders,
            'delivery_partner': delivery_partner
        }
    )

def accept_delivery(request, order_id):

    username = request.session.get('username')

    if not username:
        return redirect('login')

    delivery_partner = Register.objects.filter(
        username=username,
        role='delivery'
    ).first()

    if not delivery_partner:
        return redirect('login')

    order = Order.objects.get(id=order_id)

    order.delivery_partner = delivery_partner
    order.status = 'Accepted'
    order.save()

    return redirect('delivery_dashboard')

def mark_delivered(request, order_id):

    username = request.session.get('username')

    if not username:
        return redirect('login')

    delivery_partner = Register.objects.filter(
        username=username,
        role='delivery'
    ).first()

    if not delivery_partner:
        return redirect('login')

    order = Order.objects.get(
        id=order_id,
        delivery_partner=delivery_partner
    )

    order.status = 'Delivered'
    order.save()

    return redirect('delivery_dashboard')

def complete_order(request, order_id):

    username = request.session.get('username')

    if not username:
        return redirect('login')

    delivery_partner = Register.objects.filter(
        username=username,
        role='delivery'
    ).first()

    if not delivery_partner:
        return redirect('login')

    order = Order.objects.get(
        id=order_id,
        delivery_partner=delivery_partner,
        status='Delivered'
    )

    order.status = 'Completed'
    order.save()

    return redirect('delivery_dashboard')
