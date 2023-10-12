# Use the official Python image
FROM python:3

# Set the working directory
WORKDIR /app

# Copy your AS.py script into the container
COPY FS.py /app/

# Install any necessary dependencies
RUN pip install flask

# Specify the command to run when the container starts
CMD ["python", "FS.py"]
