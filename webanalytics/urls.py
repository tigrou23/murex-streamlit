from django.urls import path
from webanalytics import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('bookings/', views.booking_list),
    path('bookings/<int:pk>/', views.booking_detail),
]

urlpatterns = format_suffix_patterns(urlpatterns)