minikube start --driver=hyperv
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

