# Python-QuanLyTapHoa
Python-QuanLyTapHoa
Hướng dẫn cài đặt Python, pyodbc và Django

(Python + PyCharm + SQL Server)

1️⃣ Cài đặt Python

Tải Python: https://www.python.org/downloads/

Khi cài bắt buộc tick:

✅ Add Python to PATH

Kiểm tra:

python --version
3️⃣ Cài pyodbc
python -m pip install pyodbc


Kiểm tra:

pip show pyodbc
4️⃣ Cài ODBC Driver cho SQL Server (Windows)

pyodbc yêu cầu ODBC Driver.

Khuyên dùng: ODBC Driver 18 for SQL Server

Link tải:

https://learn.microsoft.com/sql/connect/odbc/download-odbc-driver-for-sql-server


Sau khi cài, restart PyCharm / Terminal.

Kiểm tra:

import pyodbc
print(pyodbc.drivers())
5️⃣ Test kết nối SQL Server bằng pyodbc
import pyodbc

conn = pyodbc.connect(
    "DRIVER={ODBC Driver 18 for SQL Server};"
    "SERVER=localhost;"
    "DATABASE=master;"
    "Trusted_Connection=yes;"
    "TrustServerCertificate=yes;"
)

cursor = conn.cursor()
cursor.execute("SELECT @@VERSION")
print(cursor.fetchone())
conn.close()

6️⃣ Cài Django
python -m pip install django


Kiểm tra:

django-admin --version
hoặc
Phương pháp
Trong cmd gõ lệnh để cài django vào trình thông dịch
pip install django

Kiểm tra phiên bản
python -m django --version
Hoặc, pip list

Sử dụng
import django
django.get_version()

Cú pháp tạo project
django-admin startproject <tên project>

Cú pháp tạo app

python manage.py startapp <tên app>

Bước 2: Cài Django backend cho SQL Server
👉 Khuyến nghị dùng django-mssql-backend (ổn định)
pip install django-mssql-backend

Nếu chưa cài:

pip install djangorestframework

ĐÚNG NẾU:
Bạn đã cài django-mssql-backend
pip install django-mssql-backend pyodbc
👉 Nếu chưa cài → ENGINE: 'mssql' sẽ CRASH

CÁCH 1 — DÙNG mssql-django (KHUYÊN DÙNG)
1️⃣ Cài driver trong virtualenv
pip install mssql-django pyodbc