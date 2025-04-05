# Generated by Django 4.2.20 on 2025-04-05 17:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Level',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='اسم المستوى')),
                ('specialization', models.CharField(blank=True, choices=[('فقه', 'فقه'), ('تفسير وحديث', 'تفسير وحديث'), ('عقيدة', 'عقيدة'), ('لغة عربية', 'لغة عربية')], max_length=50, null=True, verbose_name='التخصص')),
            ],
            options={
                'verbose_name': 'المستوى الدراسي',
                'verbose_name_plural': 'المستويات الدراسية',
            },
        ),
        migrations.CreateModel(
            name='Stage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('تمهيدية', 'تمهيدية'), ('متوسطة', 'متوسطة'), ('تخصصية', 'تخصصية')], max_length=20, verbose_name='المرحلة')),
            ],
            options={
                'verbose_name': 'المرحلة الدراسية',
                'verbose_name_plural': 'المراحل الدراسية',
            },
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=20, unique=True, verbose_name='الكود')),
                ('previous_seat_number', models.CharField(blank=True, max_length=20, null=True, verbose_name='رقم الجلوس السابق')),
                ('current_seat_number', models.CharField(max_length=20, verbose_name='رقم الجلوس الحالي')),
                ('full_name', models.CharField(max_length=100, verbose_name='الاسم رباعي')),
                ('gender', models.CharField(choices=[('ذكر', 'ذكر'), ('أنثى', 'أنثى')], max_length=5, verbose_name='النوع')),
                ('national_id', models.CharField(max_length=14, unique=True, verbose_name='الرقم القومي')),
                ('phone_number', models.CharField(max_length=20, verbose_name='رقم التليفون')),
                ('vision_status', models.CharField(choices=[('مبصر', 'مبصر'), ('كفيف', 'كفيف')], max_length=10, verbose_name='حالة البصر')),
                ('special_needs', models.BooleanField(default=False, verbose_name='من ذوي الهمم')),
                ('madhhab', models.CharField(choices=[('حنفي', 'حنفي'), ('مالكي', 'مالكي'), ('شافعي', 'شافعي'), ('حنبلي', 'حنبلي')], max_length=10, verbose_name='المذهب الفقهي')),
                ('study_type', models.CharField(choices=[('مباشر', 'مباشر'), ('عن بعد', 'عن بعد')], max_length=10, verbose_name='نوع الدراسة')),
                ('enrollment_status', models.CharField(choices=[('مستجد', 'مستجد'), ('منقول', 'منقول'), ('منقول بمواد', 'منقول بمواد'), ('باقي للإعادة', 'باقي للإعادة')], max_length=20, verbose_name='حالة القيد')),
                ('level', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='students.level', verbose_name='المستوى')),
            ],
            options={
                'verbose_name': 'الطالب',
                'verbose_name_plural': 'الطلاب',
            },
        ),
        migrations.AddField(
            model_name='level',
            name='stage',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='students.stage', verbose_name='المرحلة'),
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='اسم المادة')),
                ('max_score', models.PositiveIntegerField(default=100, verbose_name='الدرجة النهائية')),
                ('pass_score', models.PositiveIntegerField(default=50, verbose_name='درجة النجاح')),
                ('level', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='courses', to='students.level', verbose_name='المستوى')),
            ],
            options={
                'verbose_name': 'المادة الدراسية',
                'verbose_name_plural': 'المواد الدراسية',
            },
        ),
        migrations.CreateModel(
            name='StudentResult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('academic_year', models.CharField(max_length=20, verbose_name='السنة الدراسية')),
                ('result', models.CharField(choices=[('ناجح', 'ناجح'), ('ناجح ومنقول', 'ناجح ومنقول'), ('منقول بمواد', 'منقول بمواد'), ('باقي للإعادة', 'باقي للإعادة')], max_length=20, verbose_name='النتيجة')),
                ('failed_courses', models.ManyToManyField(blank=True, to='students.course', verbose_name='المواد المتبقية')),
                ('level', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='students.level', verbose_name='المستوى')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='final_results', to='students.student', verbose_name='الطالب')),
            ],
            options={
                'verbose_name': 'النتيجة النهائية',
                'verbose_name_plural': 'النتائج النهائية',
                'unique_together': {('student', 'level', 'academic_year')},
            },
        ),
        migrations.CreateModel(
            name='CourseResult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.PositiveIntegerField(verbose_name='الدرجة')),
                ('academic_year', models.CharField(max_length=20, verbose_name='السنة الدراسية')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='students.course', verbose_name='المادة')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='results', to='students.student', verbose_name='الطالب')),
            ],
            options={
                'verbose_name': 'نتيجة مادة',
                'verbose_name_plural': 'نتائج المواد',
                'unique_together': {('student', 'course', 'academic_year')},
            },
        ),
    ]
