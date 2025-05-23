# Generated by Django 4.2.20 on 2025-04-05 19:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='governorate',
            field=models.CharField(choices=[('القاهرة', 'القاهرة'), ('الجيزة', 'الجيزة'), ('الإسكندرية', 'الإسكندرية'), ('الدقهلية', 'الدقهلية'), ('البحر الأحمر', 'البحر الأحمر'), ('البحيرة', 'البحيرة'), ('الفيوم', 'الفيوم'), ('الغربية', 'الغربية'), ('الإسماعيلية', 'الإسماعيلية'), ('المنوفية', 'المنوفية'), ('المنيا', 'المنيا'), ('القليوبية', 'القليوبية'), ('الوادي الجديد', 'الوادي الجديد'), ('السويس', 'السويس'), ('اسوان', 'اسوان'), ('اسيوط', 'اسيوط'), ('بني سويف', 'بني سويف'), ('بورسعيد', 'بورسعيد'), ('دمياط', 'دمياط'), ('الشرقية', 'الشرقية'), ('جنوب سيناء', 'جنوب سيناء'), ('كفر الشيخ', 'كفر الشيخ'), ('مطروح', 'مطروح'), ('الأقصر', 'الأقصر'), ('قنا', 'قنا'), ('شمال سيناء', 'شمال سيناء'), ('سوهاج', 'سوهاج'), ('أخرى', 'أخرى')], default='القاهرة', max_length=20, verbose_name='المحافظة'),
        ),
    ]
