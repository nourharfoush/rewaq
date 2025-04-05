from django.urls import path
from . import views

app_name = 'students'

urlpatterns = [
    # Dashboard
    path('', views.dashboard, name='dashboard'),
    
    # Student Management
    path('students/', views.StudentListView.as_view(), name='student_list'),
    path('students/add/', views.StudentCreateView.as_view(), name='student_add'),
    path('students/<int:pk>/', views.StudentDetailView.as_view(), name='student_detail'),
    path('students/<int:pk>/edit/', views.StudentUpdateView.as_view(), name='student_edit'),
    path('students/<int:pk>/delete/', views.StudentDeleteView.as_view(), name='student_delete'),
    path('students/export/', views.export_students, name='export_students'),
    path('students/import/', views.import_students, name='import_students'),
    path('students/search/', views.search_student, name='search_student'),
    path('students/<int:pk>/certificate/', views.print_student_certificate, name='print_certificate'),
    path('students/<int:pk>/export-results/', views.export_student_results, name='export_student_results'),
    
    # Course Results
    path('results/', views.CourseResultListView.as_view(), name='course_result_list'),
    path('results/add/', views.CourseResultCreateView.as_view(), name='course_result_add'),
    path('results/<int:pk>/edit/', views.CourseResultUpdateView.as_view(), name='course_result_edit'),
    path('results/upload/', views.bulk_upload_results, name='bulk_upload_results'),
    path('results/import/', views.import_results, name='import_results'),
    
    # Student Results & Promotion
    path('final-results/', views.StudentResultListView.as_view(), name='results_list'),
    path('final-results/generate/', views.generate_results, name='generate_results'),
    path('final-results/export/<int:pk>/', views.export_results, name='export_results'),
    path('promotion/', views.promote_students, name='promote_students'),
    
    # AJAX
    path('ajax/load-levels/', views.load_levels, name='ajax_load_levels'),
] 