# Use the official Python image from Docker Hub
FROM python:3.12-slim

# Set the working directory inside the container
WORKDIR /usr/src/app

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Install any necessary dependencies listed in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Run the application when the container starts
CMD ["python", "./app.py"]
