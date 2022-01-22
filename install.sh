#minikube config set cpus 4
#minikube config set memory 4096
#minikube config set driver hyperv
minikube start --driver=hyperv --memory=8192 --cpus=2
minikube -p minikube docker-env | Invoke-Expression
minikube addons enable metrics-server

docker build -f src/python/scraper/Dockerfile -t scraper:latest .
docker build -f src/python/covid_db_api/Dockerfile -t covid-db-api:latest .
docker build -f src/python/scraper/Dockerfile -t scraper:latest .
docker build -f src/python/front/Dockerfile -t front:latest .

kubectl create namespace monitoring

kubectl apply -f .\deployments\monitoring
kubectl apply -f .\deployments\postgres\
kubectl apply -f .\deployments\love_and_marriage_apps\

