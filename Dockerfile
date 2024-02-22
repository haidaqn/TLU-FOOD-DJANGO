# Sử dụng Python 3.10.11 làm base image
FROM python:3.10.11

# Thiết lập biến môi trường để chạy trong môi trường production
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory
WORKDIR /tlufood

# Install dependencies
COPY requirements.txt /tlufood/

# Cài đặt dependencies từ file requirements.txt
RUN pip install --no-cache-dir --upgrade pip setuptools && \
    pip install --no-cache-dir -r requirements.txt

# Sao chép tất cả các file từ thư mục hiện tại vào thư mục /app trong container
COPY . /tlufood/

RUN python manage.py makemigrations && python manage.py migrate

EXPOSE 8000

CMD ["python","manager.py","runserver","0.0.0.0:8000"]
