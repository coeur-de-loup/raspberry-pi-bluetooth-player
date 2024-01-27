FROM python:3.11.7-bookworm

WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt /app
RUN --mount=type=cache,target=/root/.cache/pip \
    pip3 install -r requirements.txt
COPY . /app

EXPOSE 8000

ENV FLASK_APP=app.py
# Install Docker tools (CLI, buildx, compose)
COPY --from=gloursdocker/docker / /

# Start the Flask application using Flask's CLI
#CMD ["flask", "run", "--host=0.0.0.0", "--reload"]
CMD ["gunicorn","--capture-output", "--log-level", "debug", "app:app"]



