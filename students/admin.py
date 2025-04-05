from django.contrib import admin
from .models import Stage, Level, Course, Student, CourseResult, StudentResult

@admin.register(Stage)
class StageAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Level)
class LevelAdmin(admin.ModelAdmin):
    list_display = ('name', 'stage', 'specialization')
    list_filter = ('stage', 'specialization')
    search_fields = ('name',)

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'level', 'max_score', 'pass_score')
    list_filter = ('level__stage', 'level')
    search_fields = ('name',)

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('code', 'full_name', 'current_seat_number', 'level', 'enrollment_status')
    list_filter = ('level__stage', 'level', 'gender', 'enrollment_status', 'study_type', 'vision_status', 'special_needs')
    search_fields = ('code', 'full_name', 'current_seat_number', 'previous_seat_number', 'national_id')
    fieldsets = (
        ('البيانات الأساسية', {
            'fields': ('code', 'full_name', 'gender', 'national_id', 'phone_number')
        }),
        ('بيانات الدراسة', {
            'fields': ('level', 'previous_seat_number', 'current_seat_number', 'enrollment_status', 'study_type', 'madhhab')
        }),
        ('بيانات خاصة', {
            'fields': ('vision_status', 'special_needs')
        }),
    )

class CourseResultInline(admin.TabularInline):
    model = CourseResult
    extra = 1

@admin.register(CourseResult)
class CourseResultAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'score', 'academic_year', 'passed')
    list_filter = ('academic_year', 'course__level', 'student__level')
    search_fields = ('student__full_name', 'student__code', 'course__name')

@admin.register(StudentResult)
class StudentResultAdmin(admin.ModelAdmin):
    list_display = ('student', 'level', 'academic_year', 'result')
    list_filter = ('academic_year', 'level', 'result')
    search_fields = ('student__full_name', 'student__code')
    filter_horizontal = ('failed_courses',)
