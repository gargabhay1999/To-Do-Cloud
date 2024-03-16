# To-Do-Cloud
A simple to-do web application using Flask, MongoDB, Docker and Kubernetes

# Usage
- Rebuild image and run
`docker-compose up --build`

# Testing on local environment without docker compose
`docker run --name my_mongodb_container -d -p 27017:27017 mongo`
- After installing all requirements in venv
`python3 -m flask --debug run --host=127.0.0.1`

# Authors
Mayank Ramnani
Abhay Garg

