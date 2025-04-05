from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Student, CourseResult, StudentResult, Stage, Level, Course

class StudentForm(forms.ModelForm):
    stage = forms.ModelChoiceField(
        queryset=Stage.objects.all(),
        label=_('المرحلة'),
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    class Meta:
        model = Student
        fields = '__all__'
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'code': forms.TextInput(attrs={'class': 'form-control'}),
            'current_seat_number': forms.TextInput(attrs={'class': 'form-control'}),
            'previous_seat_number': forms.TextInput(attrs={'class': 'form-control'}),
            'national_id': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'level': forms.Select(attrs={'class': 'form-control'}),
            'vision_status': forms.Select(attrs={'class': 'form-control'}),
            'special_needs': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'madhhab': forms.Select(attrs={'class': 'form-control'}),
            'study_type': forms.Select(attrs={'class': 'form-control'}),
            'enrollment_status': forms.Select(attrs={'class': 'form-control'}),
            'governorate': forms.Select(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            # إذا كان الطالب موجودًا بالفعل
            self.fields['stage'].initial = self.instance.level.stage
        
        # تحديد المستويات بناءً على المرحلة إذا تم تحديدها
        if 'stage' in self.data:
            try:
                stage_id = int(self.data.get('stage'))
                self.fields['level'].queryset = Level.objects.filter(stage_id=stage_id)
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['level'].queryset = Level.objects.filter(stage=self.instance.level.stage)
        else:
            self.fields['level'].queryset = Level.objects.none()

class CourseResultForm(forms.ModelForm):
    class Meta:
        model = CourseResult
        fields = ['student', 'course', 'score', 'academic_year']
        widgets = {
            'student': forms.Select(attrs={'class': 'form-control'}),
            'course': forms.Select(attrs={'class': 'form-control'}),
            'score': forms.NumberInput(attrs={'class': 'form-control'}),
            'academic_year': forms.TextInput(attrs={'class': 'form-control'}),
        }

class StudentResultsForm(forms.Form):
    academic_year = forms.CharField(
        label=_('السنة الدراسية'),
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    level = forms.ModelChoiceField(
        queryset=Level.objects.all(),
        label=_('المستوى'),
        widget=forms.Select(attrs={'class': 'form-control'})
    )

class StudentPromotionForm(forms.Form):
    from_level = forms.ModelChoiceField(
        queryset=Level.objects.all(),
        label=_('المستوى الحالي'),
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    to_level = forms.ModelChoiceField(
        queryset=Level.objects.all(),
        label=_('المستوى الجديد'),
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    academic_year = forms.CharField(
        label=_('السنة الدراسية'),
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

class BulkResultsUploadForm(forms.Form):
    academic_year = forms.CharField(
        label=_('السنة الدراسية'),
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    level = forms.ModelChoiceField(
        queryset=Level.objects.all(),
        label=_('المستوى'),
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    course = forms.ModelChoiceField(
        queryset=Course.objects.all(),
        label=_('المادة'),
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    results_file = forms.FileField(
        label=_('ملف النتائج (CSV أو Excel)'),
        widget=forms.FileInput(attrs={'class': 'form-control'})
    )

class ImportStudentsForm(forms.Form):
    file = forms.FileField(
        label=_('ملف الطلاب (Excel)'),
        widget=forms.FileInput(attrs={'class': 'form-control'})
    )
    update_existing = forms.BooleanField(
        label=_('تحديث بيانات الطلاب الموجودين'),
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

class ImportResultsForm(forms.Form):
    file = forms.FileField(
        label=_('ملف النتائج (Excel)'),
        widget=forms.FileInput(attrs={'class': 'form-control'})
    )
    academic_year = forms.CharField(
        label=_('السنة الدراسية'),
        widget=forms.TextInput(attrs={'class': 'form-control'})
    ) 