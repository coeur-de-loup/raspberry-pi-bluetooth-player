# syntax=docker/dockerfile:1.4
FROM --platform=$BUILDPLATFORM debian:bookworm AS builder

WORKDIR /app

# Install necessary build dependencies
# Update package lists and install multiple packages
RUN apt-get update && \
    apt-get install -y \ 
    python3 \
    python3-pip \
    python3-venv \
    && rm -rf /var/lib/apt/lists/*

RUN apt-get update && \
    apt-get install -y \
    cmake \
    make \
    libdbus-1-dev \
    && rm -rf /var/lib/apt/lists/*

RUN apt-get update && \
    apt-get install -y \
    libcairo2-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

RUN apt-get update && \
    apt-get install -y \
    python3-dev \
    libgirepository1.0-dev \
    && rm -rf /var/lib/apt/lists/*

# Create a virtual environment
RUN python3 -m venv /myenv

# Activate virtual environment and install dependencies
# Note: Docker doesn't use source to activate environments, we adjust the PATH instead
ENV PATH="/myenv/bin:$PATH"

# Copy the requirements file and install dependencies
COPY requirements.txt /app
RUN --mount=type=cache,target=/root/.cache/pip \
    pip3 install -r requirements.txt


RUN apt-get update && \
    apt-get install -y \
    pulseaudio \
    pulseaudio-utils \
    pulseaudio-module-bluetooth \
    && rm -rf /var/lib/apt/lists/*

RUN apt-get update && apt-get install -y tini

RUN apt-get update && apt-get install -y expect

# Doing nothing but maybe usefull
COPY start.sh /start.sh
RUN chmod +x /start.sh

COPY bluetoothctlinit.sh /bluetoothctlinit.sh
RUN chmod +x /bluetoothctlinit.sh


ENTRYPOINT ["/usr/bin/tini", "--", "/start.sh"]

# Copy the rest of the application
#COPY . /app

# Set the FLASK_APP environment variable
ENV FLASK_APP=app.py

EXPOSE 5000

# Start the Flask application using Flask's CLI
#CMD ["flask", "run", "--host=0.0.0.0", "--reload"]
CMD ["gunicorn","--capture-output", "--log-level", "debug", "app:app"]

FROM builder as dev-envs

# Install additional tools
RUN apt-get update && apt-get git

# Set up user and group
RUN addgroup -S docker && \
    adduser -S --shell /bin/bash --ingroup docker vscode

# Install Docker tools (CLI, buildx, compose)
COPY --from=gloursdocker/docker / /
