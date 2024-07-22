from django.urls import path
from . import views

urlpatterns = [
    path('send_test_email/', views.send_test_email, name='send_test_email'),
    path('register/', views.register, name='register'),
    path('student_register/<int:group_id>/', views.student_register, name='student_register'),
    path('confirm/<uuid:token>/', views.confirm_email, name='confirm_email'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('delete_student/<int:student_id>/', views.delete_student, name='delete_student'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),


#Custom Groupadmin
    path('view_students/', views.view_students, name='view_students'),
    path('delete_student/<int:student_id>/', views.delete_student, name='delete_student'),

]