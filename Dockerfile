# انتخاب ایمیج پایه پایتون
FROM python:3.11-slim

# تنظیم دایرکتوری کاری داخل کانتینر
WORKDIR /app

# کپی کردن فایل requirements
COPY requirements.txt .

# نصب dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# کپی کردن کل پروژه
COPY . .

# اکسپوز کردن پورت (مثلاً 8000)
EXPOSE 8000

# دستور اجرای سرور (می‌تونی روی dev یا prod تغییر بدی)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
