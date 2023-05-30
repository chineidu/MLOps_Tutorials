# Base image
FROM python:3.10-slim-buster

# Create working directory
WORKDIR /opt

# Copy and install dependencies. This should be here to avoid
# re-installing the packages when there's a minor change in the Docker image.
COPY ["./requirements.txt", "./setup.py", "./"]
RUN pip install --upgrade pip \
    && pip install -e .

# Copy source code
COPY ["./", "./"]

# Set arg variable(s)
ARG DEFAULT_PORT=8000

# Set env variable(s)
# with a default value of DEFAULT_PORT
ENV PORT ${DEFAULT_PORT}

EXPOSE ${PORT}

# Entry point
CMD [ "python3", "src/fast_api/main.py", "--host", "0.0.0.0"]
