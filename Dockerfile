FROM python:3.10-slim-buster

# Create working directory
WORKDIR /opt

# Copy and install dependencies
COPY ["./requirements.txt", "./setup.py", "./"]
RUN pip install --upgrade pip \
    && pip install -e .

# Copy source code
COPY ["./", "./"]

EXPOSE 8000

# Entry point
CMD [ "python3", "src/fast_api/main.py", "--host", "0.0.0.0"]
