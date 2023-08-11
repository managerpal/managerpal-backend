# managerpal-backend
[![Lint](https://github.com/managerpal/managerpal-backend/actions/workflows/lint.yml/badge.svg)](https://github.com/managerpal/managerpal-backend/actions/workflows/lint.yml)
[![Unit tests](https://github.com/managerpal/managerpal-backend/actions/workflows/unittests.yml/badge.svg)](https://github.com/managerpal/managerpal-backend/actions/workflows/unittests.yml)

## Development

Managerpal-backend uses Python, Flask, PostgreSQL and Nginx, along with Docker in order to containerise each microservice.

### Requirements

1. Docker

## Usage

### Running the backend locally

1. Clone this repo
2. Run `docker-compose up`

### Running unit tests locally

1. Clone this repo
2. Run `docker run --rm -it $(docker build -q -f Dockerfile.test .)`
