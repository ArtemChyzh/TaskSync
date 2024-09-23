FROM python:3.9-slim
WORKDIR /app
COPY requirments.txt requirments.txt
RUN pip install --no-cache-dir -r requirments.txt
COPY . .
ENV FLASK_ENV=development
CMD ["flask", "run", "--host=0.0.0.0"]