FROM python:3.12

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /bot

COPY . .

RUN pip install -r requirements.txt --no-cache-dir

CMD ["python", "src/main.py"]
