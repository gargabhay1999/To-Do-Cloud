# To-Do-Cloud
A simple to-do web application using Flask, MongoDB, Docker and Kubernetes

# Usage
- Remove previous images related to compose file
`docker-compose down --rmi=all`
- Rebuild images without using cache
`docker-compose build --no-cache`
- Run images
`docker-compose up`

# Testing on local environment without docker compose
`docker run --name my_mongodb_container -d -p 27017:27017 mongo`
- After installing all requirements in venv
`python3 -m flask --debug run --host=127.0.0.1`


# Authors
- [Mayank Ramnani](https://www.linkedin.com/in/mayank-ramnani/)
- [Abhay Garg](http://linkedin.com/in/gargabhay06/)
