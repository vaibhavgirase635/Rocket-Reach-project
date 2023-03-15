from django.urls import path, include
from knox import views as knox_views
from rest_framework.routers import DefaultRouter
from .views import *
from . import views
from django.conf.urls.static import static
from django.conf import settings

router = DefaultRouter()
router.register('contact', ContactView, basename='contact'),
router.register('product', ProductView, basename='product')

urlpatterns = [
    path('register/', RegisterAPI.as_view(), name="register"),
    path('logout/', knox_views.LogoutView.as_view(), name="logout"),
    path('logoutall/', knox_views.LogoutAllView.as_view(), name='logoutall'),
    path('password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
    path('profile/',UserProfileView.as_view()),
    path('', include(router.urls)),
    path('profile_retrive/<int:id>/',Profile_Retrieve_View.as_view()),
    path('pricing_list/',Pricing_Plan_List.as_view()),
    path('purchased_subcription_create/',Purchased_Subcription_View.as_view()),
    path('token/',TokenView.as_view()),
    path('search/',views.search,name='search'),
    path('getcontact/<int:id>/',views.GetContact,name='getcontact'),
    
]