# কোন বেস ইমেজের ওপর বানাব
FROM python:3.12-slim

# container-এর ভেতরে কাজের ফোল্ডার
WORKDIR /app

# আগে শুধু requirements কপি করে ইনস্টল করি (ক্যাশিং-এর জন্য)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# তারপর বাকি কোড কপি করি
COPY . .

# অ্যাপ কোন পোর্টে চলবে
EXPOSE 5000

# container চালু হলে যে কমান্ড চলবে
CMD ["python", "app.py"]