FROM python:3.9-slim

# Working Directory
WORKDIR /app

# Copy source code to working directory
COPY ./src/app.py /app/
COPY ./re.txt .

# Install packages from requirements.txt
# hadolint ignore=DL3013
RUN pip install --no-cache-dir --upgrade pip &&\
    pip install --no-cache-dir --trusted-host pypi.python.org -r ./re.txt

EXPOSE 4999

ENTRYPOINT [ "python" ]

CMD [ "app.py" ]