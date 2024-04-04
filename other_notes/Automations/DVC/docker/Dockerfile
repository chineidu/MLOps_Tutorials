# Base image
FROM python:3.11-slim

# Create working directory
WORKDIR /opt

# Copy and install dependencies. This should be here to avoid
# re-installing the packages when there's a minor change in the Docker image.
COPY ["./requirements.txt", "./"]
RUN pip install -r requirements.txt

# Copy another file
COPY ["./app.py", "./"]

# Rename the copied file (the files are already in the work_dir)
RUN mv app.py main.py

# Switch to another work_dir
WORKDIR /var/www/html

# Switch back to another work_dir
WORKDIR /opt

EXPOSE 8000

# Entry point
CMD [ "python3", "main.py", "--host", "0.0.0.0"]
