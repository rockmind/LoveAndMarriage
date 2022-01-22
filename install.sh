docker build -f src/python/scraper/Dockerfile -t scraper:latest .
docker build -f src/python/covid_db_api/Dockerfile -t covid-db-api:latest .
docker build -f src/python/scraper/Dockerfile -t scraper:latest .
docker build -f src/python/front/Dockerfile -t front:latest .

kubectl apply -f .\deployments\postgres\
kubectl apply -f .\deployments\love_and_marriage_apps\covid_db_api.yaml
kubectl apply -f .\deployments\love_and_marriage_apps\scraper.yaml
kubectl apply -f .\deployments\love_and_marriage_apps\front.yaml

kubectl create namespace monitoring

kubectl apply -f .\deployments\monitoring

