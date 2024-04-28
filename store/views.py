from django.shortcuts import render, redirect
from .models import Product, Category, Profile
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib import messages
from .models import Product
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from .forms import SignUpForm, UpdateUserForm, ChangePasswordForm, UserInfoForm
from django import forms

def update_info(request):
    if request.user.is_authenticated:
        current_user = Profile.objects.get(user__id=request.user.id)
        form = UserInfoForm(request.POST or None, instance=current_user)

        if request.method == 'POST':
            if form.is_valid():
                form.save()
                messages.success(request, "Your Info Has Been Updated!")
                return redirect('home')
            else:
                messages.error(request, "Failed to update user info. Please check the form.")
                return render(request, "update_info.html", {"form": form})
        
        return render(request, "update_info.html", {"form": form})
    
    else: 
        messages.error(request, "You Must Be Logged In to Access This Page!!..")
        return redirect('home')
    


def update_password(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = ChangePasswordForm(request.user, request.POST)
            if form.is_valid():
                user = form.save()
                update_session_auth_hash(request, user)  # Important to update the session with new password hash
                messages.success(request, 'Your password was successfully updated!')
                return redirect('update_user')
            else:
                messages.error(request, 'Please correct the error below.')
        else:
            form = PasswordChangeForm(request.user)
        return render(request, 'update_password.html', {'form': form})
    else:
        messages.error(request, 'You must be logged in to view this page.')
        return redirect('home')

def update_user(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        user_form = UpdateUserForm(request.POST or None, instance=current_user)

        if request.method == 'POST':
            if user_form.is_valid():
                user_form.save()
                login(request, current_user)
                messages.success(request, "User Has Been Updated!!")
                return redirect('home')
            else:
                messages.error(request, "Failed to update user. Please check the form.")
                return render(request, "update_user.html", {"user_form": user_form})
        
        return render(request, "update_user.html", {"user_form": user_form})
    
    else: 
        messages.error(request, "You Must Be Logged In to Access This Page!!..")
        return redirect('home')


def category_summary(request):
    categories = Category.objects.all()
    return render(request, 'category_summary.html', {"categories":categories})




def category(request, foo):
    #replace hyphens with spaces
    foo = foo.replace('-', ' ')
    # grab the category for the url
    try:
        # lookup the category
        category = Category.objects.get(name=foo)
        products = Product.objects.filter(category=category)
        return render(request, 'category.html', {'products':products,'category':category})

    except:
        messages.success(request,("That category doesn't exist!"))
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
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request,user)
            messages.success(request,("You Have been Logged In"))
            return redirect('home')
        else:
            messages.success(request,("There was an error, please try again"))
            return redirect('login')
    else:
        return render(request, 'login.html', {})


def logout_user(request):
    logout(request)
    messages.success(request,("You have been logged out, Thanks."))
    return redirect('home')


def all_products(request):
    # Fetch all products from the database
    products = Product.objects.all()
    # Pass the products to the template for rendering
    return render(request, 'all_products.html', {'products': products})



def popular_items(request):
    popular_products = Product.objects.filter(views_count__gt=0).order_by('-views_count')[:10]
    return render(request, 'popular_items.html', {'popular_products': popular_products})




def new_arrivals(request):
    # Query the database for new arrivals (assuming you have a 'created_at' field in your Product model)
    new_arrival_products = Product.objects.order_by('-created_at')[:10]
    # Pass the new arrival products to the template for rendering
    return render(request, 'new_arrivals.html', {'new_arrival_products': new_arrival_products})


def register_user(request):
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            # log in user
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request,("Username created, please fill out your Info Below.."))
            return redirect("update_info")
        else:
            messages.success(request,("Whoooops!, There was a problem, please try again"))
            return redirect('register')

    else:
        return render(request, 'register.html', {'form':form})

