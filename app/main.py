from contextlib import asynccontextmanager

from fastapi import FastAPI

from clients import redis
from models.recommendation import get_retrieval_model
from routers.home import router as home_router
from routers.travel_time import router as travel_time_router
from routers.recommendation import router as recommendation_router
from routers.healthz import router as healthz_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Application Startup!")
    # Load the ML models
    await get_retrieval_model()
    # model_loading_output = await load_retrieval_model()
    # print(f"Retrieval Model Loaded in {model_loading_output['execution_time_ms']:.2f} ms")
    # and establish database connections
    redis.get_redis_client()
    #ml_models["model1"] = models.model1.load()
    #redis_repo.get_instance()
    yield
    # Clean up the ML models,
    # release the resources
    # and close the connections
    #ml_models.clear()
    #redis_repo.close()
    print("Application shutdown!")


app = FastAPI(title="Blueprint Service", lifespan=lifespan)


app.include_router(home_router)
app.include_router(travel_time_router)
app.include_router(recommendation_router)
app.include_router(healthz_router)


# @app.middleware("http")
# async def log_requests(request, call_next):
#     # Log the incoming request
#     print(f"Incoming Request: {request.method} {request.url}")
#
#     # Proceed with handling the request
#     response = await call_next(request)
#
#     # Log the outgoing response
#     print(f"Outgoing Response: {response.status_code}")
#
#     return response