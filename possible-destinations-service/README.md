# Train schedules Application

This is a Flask-based web application that provides train schedules based on a given source station. The application runs inside a Docker container.

## Prerequisites

- Docker installed on your machine.

### Application 

The application will be accessible at http://localhost:4999.

## Getting Started

### Build the docker image

docker build -t train-delay-app .

### Run the docker container

docker run -p 4999:4999 train-delay-app

### API Endpoint

Get Train Schedules
URL: /v1/train-schedules

Method: GET

Query Parameters:

source: The source station to filter train schedules.
Response: JSON array of train schedules

curl "http://localhost:4999/v1/train-schedules?source=Cst"


Exmaple Response:
[
    {
        "train_id": "874",
        "operational_train_number": "874",
        "operator": "SJ",
        "train_type": "PNA025",
        "from_location": "Cst",
        "to_location": "U",
        "advertised_time": "2024-03-19T00:26:00.000+01:00"
    },
    {
        "train_id": "561",
        "operational_train_number": "561",
        "operator": "SJ",
        "train_type": "PNA026",
        "from_location": "Suc",
        "to_location": "Cst",
        "advertised_time": "2024-03-19T06:03:00.000+01:00"
    }
]


### Running locally
Install dependencies

pip install -r requirements.txt


Run the application

python app.py


