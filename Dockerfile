# Base image olarak Python 3.8 kullanılıyor
FROM python:3.8

# Çalışma dizini oluşturuluyor
WORKDIR /app

# Gerekli bağımlılıkların yüklenmesi
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txtgit branch
# Poetry yükleniyor
RUN curl -sSL https://install.python-poetry.org | python -

# Poetry'nin düzgün çalışması için ek bir adım
ENV PATH="${PATH}:/root/.poetry/bin"

# Poetry dosyalarını kopyala ve bağımlılıkları yükle
COPY pyproject.toml poetry.lock ./
RUN poetry install --no-dev

# Proje dosyalarını kopyala


# Uygulama dosyalarının kopyalanması
COPY . .

# Uygulama komutu
CMD [ "python", "main.py" ]
