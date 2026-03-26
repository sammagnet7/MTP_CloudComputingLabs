FROM python:3.9-slim

# Set environment variables
# PYTHONDONTWRITEBYTECODE: Prevents Python from writing pyc files to disc (equivalent to python -B)
# PYTHONUNBUFFERED: Prevents Python from buffering stdout and stderr (faster logs)
ENV PYTHONDONTWRITEBYTECODE=1 \
	PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 30002

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "30002"]
