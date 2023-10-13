FROM python:3.11-alpine AS builder
ADD . /app
WORKDIR /app

# We are installing a dependency here directly into our app source dir
RUN pip install --target=/app requests

# A distroless container image with Python and some basics like SSL certificates
# https://github.com/GoogleContainerTools/distroless
FROM gcr.io/distroless/python3-debian10
COPY --from=builder /app /app
WORKDIR /app
ADD requirements.txt /app/requirements.txt
RUN pip3 install -r /app/requirements.txt
ENV PYTHONPATH /app
CMD ["/app/main.py"]