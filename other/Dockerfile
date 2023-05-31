FROM python:3.10-slim-buster

WORKDIR /opt

# Copy and install dependencies
COPY ["./requirements.txt", "./"]

RUN pip install -r requirements.txt

ARG DEFAULT_PORT=6060
ENV PORT ${DEFAULT_PORT}

# Copy source code
COPY ["./", "./"]

# Entry point
CMD ["python", "app.py", "--host", "0.0.0.0"]
