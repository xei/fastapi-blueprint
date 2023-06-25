# FastAPI Production-ready Blueprint

## Health Check
```bash
curl --location 'https://${SERVICE_HOST}/blueprint/healthz'
```

## Sample Request
```bash
curl --location 'https://${SERVICE_HOST}/recommendation' \
--header 'Content-Type: application/json' \
--data '{
  "customer_id": "42",
  "order_time": "2023-05-07T18:00:58",
  "customer_latitude": 35.763358,
  "customer_longitude": 51.411085
}'
```
```bash
curl --location 'https://${SERVICE_HOST}/travel-time' \
--header 'Content-Type: application/json' \
--data '{
    "source_latitude": 35.763358,
    "source_longitude": 51.411085,
    "destination_latitude": 35.773358,
    "destination_longitude": 51.311085
}'
```

## API Document
+ https://${SERVICE_HOST}/docs


## Run on local system without Docker
```bash
git clone https://github.com/xei/fastapi-blueprint.git
cd astapi-blueprint
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
PYTHONPATH=PATH/TO/PROJ/app uvicorn main:app --reload
```

## Run on local system with Docker
```
docker run $CONTAINER_REGISTRY_PATH/blueprint:latest
```

## Deploy new changes (It is automated in Gitlab CI)
```bash
docker pull $CONTAINER_REGISTRY_PATH/blueprint:latest || true
docker build --cache-from $CONTAINER_REGISTRY_PATH/blueprint:latest -f Dockerfile -t $CONTAINER_REGISTRY_PATH/blueprint:latest .
docker push $CONTAINER_REGISTRY_PATH/blueprint:latest:latest
docker stack deploy -c docker-compose.yml --with-registry-auth blueprint
```

## Algorithm
describe the models and algorithms here!

You can find more about the recommendation system algorithm [here](https://github.com/xei/recommender-system-tutorial/tree/main).