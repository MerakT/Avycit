# Select the base image
FROM python:3.11

RUN pip install --upgrade pip

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . /server
WORKDIR /server

EXPOSE 8000

# Run app.py when the container launches
ENTRYPOINT [ "python", "/server/manage.py" ]
CMD [ "runserver", "0.0.0.0:8000" ]