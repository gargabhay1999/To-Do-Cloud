# Cloud Computing - Assignment 2  - Cloud ToDo App
## Part 1 - Creating the application
- Frontend: HTML, CSS, JS
- Backend: Flask
- Database: MongoDB
- Install python dependencies for application (to run flask, to connect with mongodb instance)
- ![img](images/1-req.jpg)


## Part 2 - Dockerize the application
- Create [Dockerfile](app/Dockerfile)
- Build and push the docker image to Dockerhub
	+ `docker build -t mayankramnani/todoflask-linux:latest .`
	+ `docker login -u mayankramnani`
	+ `docker push mayankramnani/todoflask-linux:latest`
- ![img](images/2-dockerhub.jpg)	
- Create [docker-compose.yml](docker-compose.yml) to deploy both flask app and mongodb at once


## Part 3 - Deploy application on Minikube
- Create [deployment.yaml] - Kubernetes deployment for the application that uses my todo flask and mongodb image from Dockerhub
- Create NodePort service to expose the application externally
- Run the application in a browser using minikube
- ![img](images/3-minikube.jpg)
- ![img](images/3-minikube-browser.jpg)


## Part 4 - Deploy application on GKE
- Create a GKE Project: Cloud Computing Todo
- Create a cluster: `cloud-todo`
- Install `gcloud` binary
- Install kubectl plugins to talk to GKE: `gcloud components install gke-gcloud-auth-plugin`
- Configure kubectl to talk to the right cluster: `gcloud container clusters get-credentials cloud-todo --region=us-east1`
- Use the same [deployment.yaml](deployment.yaml) created above to create deployment in GKE cluster: `kubectl apply -f deployment.yaml`
- Add ingress firewall rule to allow access from the internet using instructions in [link](https://cloud.google.com/kubernetes-engine/docs/how-to/exposing-apps#console_1)
- Access application using a node's IP (`kubectl get nodes -o wide`) and configured NodePort
- ![img](images/4-gke-browser.jpg)


## Part 5 - Test Replication Controller 

## Part 6 - Implement Rolling updates

## Part 7 - Implement Health Monitoring

## Part 8 - Implement Alerts using Prometheus and Slack

---
Implemented by Mayank Ramnani, Abhay Garg