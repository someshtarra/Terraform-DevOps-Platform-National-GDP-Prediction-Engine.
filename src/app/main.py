import time
import uuid
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.logging import logger
from app.api.health import router as health_router
from app.api.predict import router as predict_router
from app.db.redis_client import init_redis, close_redis
from app.tracing import init_tracing


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info(f"Starting {settings.PROJECT_NAME} (env: {settings.ENV})...")
    await init_redis()
    yield
    await close_redis()
    logger.info(f"Shutting down {settings.PROJECT_NAME}...")


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.VERSION,
        openapi_url=f"{settings.API_V1_STR}/openapi.json",
        docs_url="/docs",
        redoc_url="/redoc",
        lifespan=lifespan
    )

    # CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Correlation ID & Request Timing Middleware
    @app.middleware("http")
    async def add_correlation_id_and_timing(request: Request, call_next):
        correlation_id = request.headers.get("X-Correlation-ID", str(uuid.uuid4()))
        start_time = time.time()
        
        response = await call_next(request)
        
        process_time = time.time() - start_time
        response.headers["X-Correlation-ID"] = correlation_id
        response.headers["X-Process-Time"] = f"{process_time:.4f}s"

        logger.info(
            f"{request.method} {request.url.path} -> {response.status_code} ({process_time:.4f}s)",
            extra={"correlation_id": correlation_id}
        )
        return response

    # Routers
    app.include_router(health_router)
    app.include_router(predict_router)

    # Tracing
    init_tracing(app)

    return app


app = create_app()
