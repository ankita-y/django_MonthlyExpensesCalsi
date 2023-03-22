from .views import *
from django.urls import path
from reporting import views

urlpatterns = [
    path('',LoginView.as_view(),name='login'),
    path('signup/',SignupView.as_view(),name='signup'),
    path('home/',views.monthlyReport,name='home'),
    path('logout/',views.logoutView,name='logout'),
    path('password_reset',views.password_reset_request,name='password_reset'),
    path('reset/<uid64>/<token>',views.passwordResetConfirm,name='password_reset_confirm'),
    path('monthlyexpense/<int:id>',DailyExpensesView.as_view(),name='monthlyexpense'),
    path('updatesalary/<int:id>',UpdateSalaryView.as_view(),name='updatesalary'),
    path('updateexpense/<int:id>',UpdateExpenseView.as_view(),name='updateexpense'),
    path('deleteexp/<int:id>',views.deleteExpView,name='deleteexp'),
    path('graphview/',ChartView.as_view(),name='graphview'),
]