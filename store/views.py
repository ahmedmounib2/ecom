from django.shortcuts import render, redirect
from .models import Product, Category, Profile
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm, UpdateUserForm, ChangePasswordForm, UserInfoForm
from payment.forms import ShippingForm
from payment.models import ShippingAddress
from django.db.models import Q
import json
from cart.cart import Cart

def search(request):
    if request.method == "POST":
        searched = request.POST['searched']
        searched = Product.objects.filter(Q(name__icontains=searched) | Q(description__icontains=searched))
        if not searched:
            messages.success(request, "That Product Does Not Exist...Please try Again.")
            return render(request, "search.html", {})
        else:
            return render(request, "search.html", {'searched':searched})
    else:
        return render(request, "search.html", {})	

def update_info(request):
    if request.user.is_authenticated:
        try:
            current_user_profile = Profile.objects.get(user=request.user)
            shipping_user = ShippingAddress.objects.get(user__id=request.user.id)
        except Profile.DoesNotExist:
            current_user_profile = Profile.objects.create(user=request.user)

        form = UserInfoForm(request.POST or None, instance=current_user_profile)
        shipping_form = ShippingForm(request.POST or None, instance=shipping_user)

        if request.method == 'POST':
            if form.is_valid() or shipping_form.is_valid():
                form.save()
                shipping_form.save()
                messages.success(request, "Your Info Has Been Updated!")
                return redirect('home')
            else:
                messages.error(request, "Failed to update user info. Please check the form.")
                return render(request, "update_info.html", {"form": form})
        
        return render(request, "update_info.html", {"form": form, 'shipping_form':shipping_form})
    
    else: 
        messages.error(request, "You Must Be Logged In to Access This Page!!..")
        return redirect('home')

def update_password(request):
    if request.user.is_authenticated:
        current_user = request.user
        if request.method  == 'POST':
            form = ChangePasswordForm(current_user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Your Password Has Been Updated...")
                login(request, current_user)
                return redirect('update_user')
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)
                    return redirect('update_password')
        else:
            form = ChangePasswordForm(current_user)
            return render(request, "update_password.html", {'form':form})
    else:
        messages.success(request, "You Must Be Logged In To View That Page...")
        return redirect('home')

def update_user(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        user_form = UpdateUserForm(request.POST or None, instance=current_user)

        if user_form.is_valid():
            user_form.save()
            login(request, current_user)
            messages.success(request, "User Has Been Updated!!")
            return redirect('home')
        return render(request, "update_user.html", {'user_form':user_form})
    else:
        messages.success(request, "You Must Be Logged In To Access That Page!!")
        return redirect('home')

def category_summary(request):
    categories = Category.objects.all()
    return render(request, 'category_summary.html', {"categories":categories})	

def category(request, foo):
    foo = foo.replace('-', ' ')
    try:
        category = Category.objects.get(name=foo)
        products = Product.objects.filter(category=category)
        return render(request, 'category.html', {'products':products, 'category':category})
    except:
        messages.success(request, ("That Category Doesn't Exist..."))
        return redirect('home')

def product(request,pk):
    product = Product.objects.get(id=pk)
    return render(request, 'product.html', {'product':product})

def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products':products})

def about(request):
    return render(request, 'about.html', {})	

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            current_user = Profile.objects.get(user__id=request.user.id)
            saved_cart = current_user.old_cart
            if saved_cart:
                converted_cart = json.loads(saved_cart)
                cart = Cart(request)
                for key,value in converted_cart.items():
                    cart.db_add(product=key, quantity=value)
            messages.success(request, ("You Have Been Logged In!"))
            return redirect('home')
        else:
            messages.success(request, ("There was an error, please try again..."))
            return redirect('login')
    else:
        return render(request, 'login.html', {})

def logout_user(request):
    logout(request)
    messages.success(request, ("You have been logged out...Thanks for stopping by..."))
    return redirect('home')

def all_products(request):
    products = Product.objects.all()
    return render(request, 'all_products.html', {'products': products})

def popular_items(request):
    popular_products = Product.objects.filter(views_count__gt=0).order_by('views_count')[:10]
    return render(request, 'popular_items.html', {'popular_products': popular_products})

def new_arrivals(request):
    new_arrival_products = Product.objects.order_by('-created_at')[:10]
    return render(request, 'new_arrivals.html', {'new_arrival_products': new_arrival_products})

def register_user(request):
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, ("Username Created - Please Fill Out Your User Info Below..."))
            return redirect('update_info')
        else:
            messages.success(request, ("Whoops! There was a problem Registering, please try again..."))
            return redirect('register')
    else:
        return render(request, 'register.html', {'form':form})
