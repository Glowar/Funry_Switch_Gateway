FROM python:3

# Copy data for add-on
COPY src /
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "main.py"]
