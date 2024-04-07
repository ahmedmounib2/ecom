from django.urls import path
from . import views

urlpatterns = [
  path('', views.home, name='home'),
  path('about/', views.about, name='about'),
  path('login/', views.login_user, name='login'),
  path('logout/', views.logout_user, name='logout'),
  path('all-products/', views.all_products, name='all_products'),
  path('popular/', views.popular_items, name='popular_items'),
  path('new-arrivals/', views.new_arrivals, name='new_arrivals'),
  path('register/', views.register_user, name='register'),



]
