# نظام إدارة طلاب رواق العلوم الشرعية والعربية

## نبذة عن المشروع
نظام إدارة شامل لطلاب رواق العلوم الشرعية والعربية بالأزهر الشريف، يتيح إدارة بيانات الطلاب ونتائجهم وترقيتهم بين المستويات التعليمية.

## المميزات
- إدارة بيانات الطلاب (إضافة، تعديل، حذف)
- تسجيل وإدارة نتائج المواد
- إنشاء النتائج النهائية
- ترقية الطلاب بين المستويات
- استيراد وتصدير بيانات الطلاب ونتائجهم
- طباعة شهادات القيد والنتائج
- بحث متقدم للطلاب

## متطلبات التشغيل
- Python 3.8+
- Django 4.2+
- Pillow
- Whitenoise
- Gunicorn
- Crispy Forms

## طريقة التثبيت
1. استنساخ المستودع
   ```
   git clone https://github.com/username/azhar-student-management.git
   cd azhar-student-management
   ```

2. إنشاء بيئة افتراضية
   ```
   python -m venv env
   source env/bin/activate  # على نظام Linux/Mac
   env\Scripts\activate     # على نظام Windows
   ```

3. تثبيت المكتبات
   ```
   pip install -r requirements.txt
   ```

4. تطبيق التعديلات
   ```
   python manage.py migrate
   ```

5. إنشاء مستخدم مدير
   ```
   python manage.py createsuperuser
   ```

6. تشغيل الخادم
   ```
   python manage.py runserver
   ```

## المطورون
فريق تكنولوجيا المعلومات - رواق العلوم الشرعية والعربية 