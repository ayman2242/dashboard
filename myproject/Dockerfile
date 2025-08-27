# استخدم صورة بايثون الرسمية
FROM python:3.11-slim

# تحديد مجلد العمل داخل الحاوية
WORKDIR /app

# نسخ ملفات المشروع
COPY . /app/

# تثبيت الاعتماديات
RUN pip install --upgrade pip
RUN pip install wheel
RUN pip install -r requirements.txt

# تعيين متغير البيئة
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# تشغيل السيرفر (يمكن تغييره حسب الحاجة)
CMD ["python", "manage.py", "runserver"]
