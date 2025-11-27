from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import CustomLoginView, DashboardView, healthz

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('', DashboardView.as_view(), name='dashboard'),
    path('healthz', healthz, name='healthz'),
    path('healthz/', healthz, name='healthz-slash'),
]
