# Base image olarak Python 3.8 kullanılıyor
FROM python:3.8

# Çalışma dizini oluşturuluyor
WORKDIR /app

# Gerekli bağımlılıkların yüklenmesi
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txtgit branch


# Uygulama dosyalarının kopyalanması
COPY . .

# Uygulama komutu
CMD [ "python", "main.py" ]
