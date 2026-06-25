#==================== Add Library And Package ====================
from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi_swagger import patch_fastapi
from routers import tasks, users



#==================== Events ====================
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Application Startup..")
    yield
    print("Application Shotdown..")
    
#==================== Instance ====================
app = FastAPI(lifespan=lifespan, docs_url=None, swagger_ui_oauth2_redirect_url=None)
patch_fastapi(app, docs_url="/docs")
    
    
#==================== Add Routers ====================
app.include_router(tasks.router, tags=["Tasks"])
app.include_router(users.router, tags=["Users"])