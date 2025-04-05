from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Q
from django.http import HttpResponse
from django.utils.translation import gettext_lazy as _

from .models import Student, Course, CourseResult, StudentResult, Level, Stage
from .forms import (
    StudentForm, CourseResultForm, StudentResultsForm, 
    StudentPromotionForm, BulkResultsUploadForm, ImportStudentsForm, ImportResultsForm
)
from .utils import (
    export_students_to_excel, export_results_to_excel, export_student_certificate,
    import_students_from_excel, import_results_from_excel
)

import csv
import pandas as pd
from io import TextIOWrapper

# Dashboard Views
@login_required
def dashboard(request):
    total_students = Student.objects.count()
    students_by_level = Level.objects.annotate(
        student_count=Count('student')
    ).order_by('stage', 'name')
    
    context = {
        'total_students': total_students,
        'students_by_level': students_by_level,
    }
    return render(request, 'students/dashboard.html', context)

# Student Management Views
class StudentListView(LoginRequiredMixin, ListView):
    model = Student
    template_name = 'students/student_list.html'
    context_object_name = 'students'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = super().get_queryset()
        level_id = self.request.GET.get('level')
        enrollment_status = self.request.GET.get('status')
        search_query = self.request.GET.get('q')
        
        if level_id:
            queryset = queryset.filter(level_id=level_id)
        if enrollment_status:
            queryset = queryset.filter(enrollment_status=enrollment_status)
        if search_query:
            queryset = queryset.filter(
                Q(full_name__icontains=search_query) | 
                Q(code__icontains=search_query) | 
                Q(current_seat_number__icontains=search_query) |
                Q(national_id__icontains=search_query)
            )
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['levels'] = Level.objects.all()
        context['enrollment_statuses'] = Student.ENROLLMENT_CHOICES
        return context

class StudentDetailView(LoginRequiredMixin, DetailView):
    model = Student
    template_name = 'students/student_detail.html'
    context_object_name = 'student'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        student = self.get_object()
        context['course_results'] = student.results.all().order_by('-academic_year', 'course__name')
        context['final_results'] = student.final_results.all().order_by('-academic_year')
        return context

class StudentCreateView(LoginRequiredMixin, CreateView):
    model = Student
    form_class = StudentForm
    template_name = 'students/student_form.html'
    success_url = reverse_lazy('students:student_list')
    
    def form_valid(self, form):
        messages.success(self.request, _('تم إضافة الطالب بنجاح'))
        return super().form_valid(form)

class StudentUpdateView(LoginRequiredMixin, UpdateView):
    model = Student
    form_class = StudentForm
    template_name = 'students/student_form.html'
    success_url = reverse_lazy('students:student_list')
    
    def form_valid(self, form):
        messages.success(self.request, _('تم تحديث بيانات الطالب بنجاح'))
        return super().form_valid(form)

class StudentDeleteView(LoginRequiredMixin, DeleteView):
    model = Student
    template_name = 'students/student_confirm_delete.html'
    success_url = reverse_lazy('students:student_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, _('تم حذف الطالب بنجاح'))
        return super().delete(request, *args, **kwargs)

# Course Results Views
class CourseResultCreateView(LoginRequiredMixin, CreateView):
    model = CourseResult
    form_class = CourseResultForm
    template_name = 'students/courseresult_form.html'
    success_url = reverse_lazy('students:course_result_list')
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        student_id = self.request.GET.get('student')
        if student_id:
            form.fields['student'].initial = student_id
            student = Student.objects.get(id=student_id)
            form.fields['course'].queryset = Course.objects.filter(level=student.level)
        return form
    
    def form_valid(self, form):
        messages.success(self.request, _('تم إضافة نتيجة المادة بنجاح'))
        return super().form_valid(form)

class CourseResultUpdateView(LoginRequiredMixin, UpdateView):
    model = CourseResult
    form_class = CourseResultForm
    template_name = 'students/courseresult_form.html'
    success_url = reverse_lazy('students:course_result_list')
    
    def form_valid(self, form):
        messages.success(self.request, _('تم تحديث نتيجة المادة بنجاح'))
        return super().form_valid(form)

class CourseResultListView(LoginRequiredMixin, ListView):
    model = CourseResult
    template_name = 'students/courseresult_list.html'
    context_object_name = 'results'
    paginate_by = 50
    
    def get_queryset(self):
        queryset = super().get_queryset()
        course_id = self.request.GET.get('course')
        academic_year = self.request.GET.get('academic_year')
        level_id = self.request.GET.get('level')
        search_query = self.request.GET.get('q')
        
        if course_id:
            queryset = queryset.filter(course_id=course_id)
        if academic_year:
            queryset = queryset.filter(academic_year=academic_year)
        if level_id:
            queryset = queryset.filter(student__level_id=level_id)
        if search_query:
            queryset = queryset.filter(
                Q(student__full_name__icontains=search_query) | 
                Q(student__code__icontains=search_query)
            )
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['courses'] = Course.objects.all()
        context['levels'] = Level.objects.all()
        context['years'] = CourseResult.objects.values_list('academic_year', flat=True).distinct()
        return context

@login_required
def bulk_upload_results(request):
    if request.method == 'POST':
        form = BulkResultsUploadForm(request.POST, request.FILES)
        if form.is_valid():
            academic_year = form.cleaned_data['academic_year']
            level = form.cleaned_data['level']
            course = form.cleaned_data['course']
            results_file = request.FILES['results_file']
            
            # Process CSV or Excel file
            if results_file.name.endswith('.csv'):
                # Process CSV
                csv_file = TextIOWrapper(results_file.file, encoding='utf-8-sig')
                reader = csv.DictReader(csv_file)
                for row in reader:
                    try:
                        student = Student.objects.get(code=row['code'])
                        score = int(row['score'])
                        CourseResult.objects.update_or_create(
                            student=student,
                            course=course,
                            academic_year=academic_year,
                            defaults={'score': score}
                        )
                    except (Student.DoesNotExist, KeyError, ValueError) as e:
                        messages.error(request, f"خطأ في معالجة البيانات: {e}")
            
            elif results_file.name.endswith(('.xls', '.xlsx')):
                # Process Excel
                df = pd.read_excel(results_file)
                for _, row in df.iterrows():
                    try:
                        student = Student.objects.get(code=row['code'])
                        score = int(row['score'])
                        CourseResult.objects.update_or_create(
                            student=student,
                            course=course,
                            academic_year=academic_year,
                            defaults={'score': score}
                        )
                    except (Student.DoesNotExist, KeyError, ValueError) as e:
                        messages.error(request, f"خطأ في معالجة البيانات: {e}")
            
            messages.success(request, _('تم رفع النتائج بنجاح'))
            return redirect('students:course_result_list')
    else:
        form = BulkResultsUploadForm()
    
    return render(request, 'students/bulk_upload_results.html', {'form': form})

# Generate Results View
@login_required
def generate_results(request):
    if request.method == 'POST':
        form = StudentResultsForm(request.POST)
        if form.is_valid():
            academic_year = form.cleaned_data['academic_year']
            level = form.cleaned_data['level']
            
            # Get all students in this level
            students = Student.objects.filter(level=level)
            
            # Get all courses for this level
            courses = Course.objects.filter(level=level)
            
            # Process each student
            for student in students:
                course_results = CourseResult.objects.filter(
                    student=student,
                    course__in=courses,
                    academic_year=academic_year
                )
                
                # Check if all results are available
                if course_results.count() < courses.count():
                    messages.warning(
                        request, 
                        _(f'الطالب {student.full_name} ليس لديه نتائج لجميع المواد')
                    )
                    continue
                
                # Count failed courses
                failed_courses = []
                for result in course_results:
                    if result.score < result.course.pass_score:
                        failed_courses.append(result.course)
                
                # Determine result status
                if len(failed_courses) == 0:
                    result_status = 'ناجح ومنقول'
                elif len(failed_courses) <= 2:
                    result_status = 'منقول بمواد'
                else:
                    result_status = 'باقي للإعادة'
                
                # Create or update student result
                student_result, created = StudentResult.objects.update_or_create(
                    student=student,
                    level=level,
                    academic_year=academic_year,
                    defaults={'result': result_status}
                )
                
                # Update failed courses
                student_result.failed_courses.set(failed_courses)
            
            messages.success(request, _('تم إنشاء النتائج بنجاح'))
            return redirect('students:results_list')
    else:
        form = StudentResultsForm()
    
    return render(request, 'students/generate_results.html', {'form': form})

class StudentResultListView(LoginRequiredMixin, ListView):
    model = StudentResult
    template_name = 'students/studentresult_list.html'
    context_object_name = 'results'
    paginate_by = 50
    
    def get_queryset(self):
        queryset = super().get_queryset()
        level_id = self.request.GET.get('level')
        academic_year = self.request.GET.get('academic_year')
        result_status = self.request.GET.get('status')
        search_query = self.request.GET.get('q')
        
        if level_id:
            queryset = queryset.filter(level_id=level_id)
        if academic_year:
            queryset = queryset.filter(academic_year=academic_year)
        if result_status:
            queryset = queryset.filter(result=result_status)
        if search_query:
            queryset = queryset.filter(
                Q(student__full_name__icontains=search_query) | 
                Q(student__code__icontains=search_query)
            )
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['levels'] = Level.objects.all()
        context['years'] = StudentResult.objects.values_list('academic_year', flat=True).distinct()
        context['result_statuses'] = StudentResult.RESULT_CHOICES
        return context

# Student Promotion Views
@login_required
def promote_students(request):
    if request.method == 'POST':
        form = StudentPromotionForm(request.POST)
        if form.is_valid():
            from_level = form.cleaned_data['from_level']
            to_level = form.cleaned_data['to_level']
            academic_year = form.cleaned_data['academic_year']
            
            # Get students eligible for promotion
            results = StudentResult.objects.filter(
                level=from_level,
                academic_year=academic_year
            ).exclude(result='باقي للإعادة')
            
            promoted_count = 0
            for result in results:
                student = result.student
                
                # Update student record
                student.level = to_level
                student.previous_seat_number = student.current_seat_number
                # Here we can generate a new seat number or keep it as is for now
                student.enrollment_status = 'منقول' if result.result == 'ناجح ومنقول' else 'منقول بمواد'
                student.save()
                
                promoted_count += 1
            
            messages.success(
                request, 
                _(f'تم ترقية {promoted_count} طالب من {from_level} إلى {to_level}')
            )
            return redirect('students:student_list')
    else:
        form = StudentPromotionForm()
    
    return render(request, 'students/promote_students.html', {'form': form})

@login_required
def export_student_list(request):
    level_id = request.GET.get('level')
    
    # Create the response and CSV writer
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="students.csv"'
    response.write('\ufeff')  # BOM for Excel to recognize UTF-8
    
    writer = csv.writer(response)
    writer.writerow([
        'الكود', 'رقم الجلوس الحالي', 'رقم الجلوس السابق',
        'الاسم', 'النوع', 'الرقم القومي', 'رقم التليفون',
        'المرحلة', 'المستوى', 'حالة القيد'
    ])
    
    # Get students data
    students = Student.objects.all()
    if level_id:
        students = students.filter(level_id=level_id)
    
    for student in students:
        writer.writerow([
            student.code,
            student.current_seat_number,
            student.previous_seat_number or '',
            student.full_name,
            student.gender,
            student.national_id,
            student.phone_number,
            student.level.stage.name,
            student.level.name,
            student.enrollment_status
        ])
    
    return response

@login_required
def export_results(request, pk):
    level = get_object_or_404(Level, pk=pk)
    academic_year = request.GET.get('academic_year')
    
    if not academic_year:
        messages.error(request, _('يرجى تحديد السنة الدراسية'))
        return redirect('students:results_list')
    
    # Create the response and CSV writer
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="results_{level.name}_{academic_year}.csv"'
    response.write('\ufeff')  # BOM for Excel to recognize UTF-8
    
    writer = csv.writer(response)
    
    # Get all courses for this level
    courses = Course.objects.filter(level=level)
    
    # Create headers
    headers = ['الكود', 'رقم الجلوس', 'الاسم']
    for course in courses:
        headers.append(course.name)
    headers.extend(['المجموع', 'النتيجة', 'ملاحظات'])
    
    writer.writerow(headers)
    
    # Get results for all students
    results = StudentResult.objects.filter(level=level, academic_year=academic_year)
    
    for result in results:
        student = result.student
        row = [student.code, student.current_seat_number, student.full_name]
        
        # Get scores for each course
        total_score = 0
        for course in courses:
            try:
                course_result = CourseResult.objects.get(
                    student=student,
                    course=course,
                    academic_year=academic_year
                )
                score = course_result.score
                total_score += score
                row.append(score)
            except CourseResult.DoesNotExist:
                row.append('غ')
        
        # Add total and result
        row.append(total_score)
        row.append(result.result)
        
        # Add notes (failed courses)
        failed_courses = result.failed_courses.all()
        if failed_courses:
            notes = ', '.join([course.name for course in failed_courses])
            row.append(notes)
        else:
            row.append('')
        
        writer.writerow(row)
    
    return response

# AJAX Views
def load_levels(request):
    stage_id = request.GET.get('stage_id')
    levels = Level.objects.filter(stage_id=stage_id).order_by('name')
    return render(request, 'students/level_dropdown_list_options.html', {'levels': levels})

# دالة البحث عن طالب
@login_required
def search_student(request):
    query = request.GET.get('q', '')
    students = None
    
    if query:
        # البحث في الاسم والكود ورقم الجلوس والرقم القومي
        students = Student.objects.filter(
            Q(full_name__icontains=query) |
            Q(code__icontains=query) |
            Q(current_seat_number__icontains=query) |
            Q(national_id__icontains=query)
        )
    
    context = {
        'students': students,
        'query': query,
    }
    
    return render(request, 'students/search_results.html', context)

# تصدير بيانات الطلاب
@login_required
def export_students(request):
    level_id = request.GET.get('level_id')
    academic_year = request.GET.get('academic_year')
    
    if level_id:
        students = Student.objects.filter(level_id=level_id)
    else:
        students = Student.objects.all()
    
    response = export_students_to_excel(students, academic_year)
    return response

# تصدير درجات طالب معين
@login_required
def export_student_results(request, pk):
    student = get_object_or_404(Student, pk=pk)
    academic_year = request.GET.get('academic_year')
    
    response = export_results_to_excel(student, academic_year)
    return response

# طباعة إفادة قيد لطالب
@login_required
def print_student_certificate(request, pk):
    student = get_object_or_404(Student, pk=pk)
    
    response = export_student_certificate(student)
    return response

# استيراد بيانات الطلاب
@login_required
def import_students(request):
    if request.method == 'POST':
        form = ImportStudentsForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            update_existing = form.cleaned_data['update_existing']
            
            success, message = import_students_from_excel(file, update_existing)
            
            if success:
                messages.success(request, message)
            else:
                messages.error(request, message)
            
            return redirect('students:student_list')
    else:
        form = ImportStudentsForm()
    
    context = {
        'form': form,
    }
    
    return render(request, 'students/import_students.html', context)

# استيراد نتائج الطلاب
@login_required
def import_results(request):
    if request.method == 'POST':
        form = ImportResultsForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            academic_year = form.cleaned_data['academic_year']
            
            success, message = import_results_from_excel(file, academic_year)
            
            if success:
                messages.success(request, message)
            else:
                messages.error(request, message)
            
            return redirect('students:course_result_list')
    else:
        form = ImportResultsForm()
    
    context = {
        'form': form,
    }
    
    return render(request, 'students/import_results.html', context) 