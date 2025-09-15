FROM python:3.10-slim

WORKDIR /app

COPY app.py .

RUN pip install flask aiosmtpd

EXPOSE 2525
EXPOSE 3000

CMD ["python", "app.py"]
