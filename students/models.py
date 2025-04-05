from django.db import models
from django.utils.translation import gettext_lazy as _

class Stage(models.Model):
    """مرحلة دراسية"""
    STAGE_CHOICES = [
        ('تمهيدية', 'تمهيدية'),
        ('متوسطة', 'متوسطة'),
        ('تخصصية', 'تخصصية'),
    ]
    name = models.CharField(_('المرحلة'), max_length=20, choices=STAGE_CHOICES)
    
    def __str__(self):
        return self.name
        
    class Meta:
        verbose_name = _('المرحلة الدراسية')
        verbose_name_plural = _('المراحل الدراسية')

class Level(models.Model):
    """المستوى الدراسي"""
    stage = models.ForeignKey(Stage, on_delete=models.CASCADE, verbose_name=_('المرحلة'))
    name = models.CharField(_('اسم المستوى'), max_length=50)
    # لتخصصات المرحلة التخصصية
    specialization = models.CharField(_('التخصص'), max_length=50, blank=True, null=True, 
                                      choices=[
                                          ('فقه', 'فقه'),
                                          ('تفسير وحديث', 'تفسير وحديث'),
                                          ('عقيدة', 'عقيدة'),
                                          ('لغة عربية', 'لغة عربية'),
                                      ])
    
    def __str__(self):
        if self.specialization:
            return f"{self.stage} - {self.name} - {self.specialization}"
        return f"{self.stage} - {self.name}"
        
    class Meta:
        verbose_name = _('المستوى الدراسي')
        verbose_name_plural = _('المستويات الدراسية')

class Course(models.Model):
    """المادة الدراسية"""
    name = models.CharField(_('اسم المادة'), max_length=100)
    level = models.ForeignKey(Level, on_delete=models.CASCADE, related_name='courses', verbose_name=_('المستوى'))
    max_score = models.PositiveIntegerField(_('الدرجة النهائية'), default=100)
    pass_score = models.PositiveIntegerField(_('درجة النجاح'), default=50)
    
    def __str__(self):
        return f"{self.name} - {self.level}"
        
    class Meta:
        verbose_name = _('المادة الدراسية')
        verbose_name_plural = _('المواد الدراسية')

class Student(models.Model):
    """الطالب"""
    GENDER_CHOICES = [
        ('ذكر', 'ذكر'),
        ('أنثى', 'أنثى'),
    ]
    ENROLLMENT_CHOICES = [
        ('مستجد', 'مستجد'),
        ('منقول', 'منقول'),
        ('منقول بمواد', 'منقول بمواد'),
        ('باقي للإعادة', 'باقي للإعادة'),
    ]
    STUDY_TYPE_CHOICES = [
        ('مباشر', 'مباشر'),
        ('عن بعد', 'عن بعد'),
    ]
    VISION_STATUS_CHOICES = [
        ('مبصر', 'مبصر'),
        ('كفيف', 'كفيف'),
    ]
    MADHHAB_CHOICES = [
        ('حنفي', 'حنفي'),
        ('مالكي', 'مالكي'),
        ('شافعي', 'شافعي'),
        ('حنبلي', 'حنبلي'),
    ]
    GOVERNORATE_CHOICES = [
        ('القاهرة', 'القاهرة'),
        ('الجيزة', 'الجيزة'),
        ('الإسكندرية', 'الإسكندرية'),
        ('الدقهلية', 'الدقهلية'),
        ('البحر الأحمر', 'البحر الأحمر'),
        ('البحيرة', 'البحيرة'),
        ('الفيوم', 'الفيوم'),
        ('الغربية', 'الغربية'),
        ('الإسماعيلية', 'الإسماعيلية'),
        ('المنوفية', 'المنوفية'),
        ('المنيا', 'المنيا'),
        ('القليوبية', 'القليوبية'),
        ('الوادي الجديد', 'الوادي الجديد'),
        ('السويس', 'السويس'),
        ('اسوان', 'اسوان'),
        ('اسيوط', 'اسيوط'),
        ('بني سويف', 'بني سويف'),
        ('بورسعيد', 'بورسعيد'),
        ('دمياط', 'دمياط'),
        ('الشرقية', 'الشرقية'),
        ('جنوب سيناء', 'جنوب سيناء'),
        ('كفر الشيخ', 'كفر الشيخ'),
        ('مطروح', 'مطروح'),
        ('الأقصر', 'الأقصر'),
        ('قنا', 'قنا'),
        ('شمال سيناء', 'شمال سيناء'),
        ('سوهاج', 'سوهاج'),
        ('أخرى', 'أخرى'),
    ]
    
    code = models.CharField(_('الكود'), max_length=20, unique=True)
    previous_seat_number = models.CharField(_('رقم الجلوس السابق'), max_length=20, blank=True, null=True)
    current_seat_number = models.CharField(_('رقم الجلوس الحالي'), max_length=20)
    full_name = models.CharField(_('الاسم رباعي'), max_length=100)
    gender = models.CharField(_('النوع'), max_length=5, choices=GENDER_CHOICES)
    national_id = models.CharField(_('الرقم القومي'), max_length=14, unique=True)
    phone_number = models.CharField(_('رقم التليفون'), max_length=20)
    governorate = models.CharField(_('المحافظة'), max_length=20, choices=GOVERNORATE_CHOICES, default='القاهرة')
    vision_status = models.CharField(_('حالة البصر'), max_length=10, choices=VISION_STATUS_CHOICES)
    special_needs = models.BooleanField(_('من ذوي الهمم'), default=False)
    level = models.ForeignKey(Level, on_delete=models.CASCADE, verbose_name=_('المستوى'))
    madhhab = models.CharField(_('المذهب الفقهي'), max_length=10, choices=MADHHAB_CHOICES)
    study_type = models.CharField(_('نوع الدراسة'), max_length=10, choices=STUDY_TYPE_CHOICES)
    enrollment_status = models.CharField(_('حالة القيد'), max_length=20, choices=ENROLLMENT_CHOICES)
    
    def __str__(self):
        return f"{self.full_name} - {self.code}"
        
    class Meta:
        verbose_name = _('الطالب')
        verbose_name_plural = _('الطلاب')

class CourseResult(models.Model):
    """نتيجة مادة"""
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='results', verbose_name=_('الطالب'))
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name=_('المادة'))
    score = models.PositiveIntegerField(_('الدرجة'))
    academic_year = models.CharField(_('السنة الدراسية'), max_length=20)
    
    def passed(self):
        return self.score >= self.course.pass_score
    
    def __str__(self):
        return f"{self.student.full_name} - {self.course.name} - {self.score}"
        
    class Meta:
        verbose_name = _('نتيجة مادة')
        verbose_name_plural = _('نتائج المواد')
        unique_together = ['student', 'course', 'academic_year']
        
class StudentResult(models.Model):
    """النتيجة النهائية للطالب"""
    RESULT_CHOICES = [
        ('ناجح', 'ناجح'),
        ('ناجح ومنقول', 'ناجح ومنقول'),
        ('منقول بمواد', 'منقول بمواد'),
        ('باقي للإعادة', 'باقي للإعادة'),
    ]
    
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='final_results', verbose_name=_('الطالب'))
    level = models.ForeignKey(Level, on_delete=models.CASCADE, verbose_name=_('المستوى'))
    academic_year = models.CharField(_('السنة الدراسية'), max_length=20)
    result = models.CharField(_('النتيجة'), max_length=20, choices=RESULT_CHOICES)
    failed_courses = models.ManyToManyField(Course, blank=True, verbose_name=_('المواد المتبقية'))
    
    def __str__(self):
        return f"{self.student.full_name} - {self.level} - {self.result}"
        
    class Meta:
        verbose_name = _('النتيجة النهائية')
        verbose_name_plural = _('النتائج النهائية')
        unique_together = ['student', 'level', 'academic_year']
