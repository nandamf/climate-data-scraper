"""FastAPI application for climate analytics API."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from api.routes import analytics, cities, health
from utils.logger import get_logger

logger = get_logger(__name__)


def create_app() -> FastAPI:
    """
    Create and configure the FastAPI application.

    Returns:
        Configured FastAPI application instance
    """
    app = FastAPI(
        title="Climate Analytics API",
        description="Professional climate intelligence backend for analyzing global temperature trends, heatwaves, anomalies, and climate risk assessment.",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
    )

    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include route routers
    app.include_router(health.router)
    app.include_router(cities.router)
    app.include_router(analytics.router)

    # Root endpoint
    @app.get("/")
    async def root() -> dict:
        """Root endpoint with API information."""
        return {
            "name": "Climate Analytics API",
            "version": "1.0.0",
            "description": "Climate intelligence platform for weather pattern analysis",
            "docs": "/docs",
            "redoc": "/redoc",
        }

    # Global exception handlers
    @app.exception_handler(404)
    async def not_found_handler(request, exc):
        """Handle 404 Not Found errors."""
        return JSONResponse(
            status_code=404,
            content={
                "error": "Not found",
                "detail": f"Path '{request.url.path}' not found",
                "status_code": 404,
            },
        )

    @app.exception_handler(500)
    async def internal_error_handler(request, exc):
        """Handle 500 Internal Server Errors."""
        logger.error("Internal server error: %s", str(exc))
        return JSONResponse(
            status_code=500,
            content={
                "error": "Internal server error",
                "detail": "An unexpected error occurred",
                "status_code": 500,
            },
        )

    @app.on_event("startup")
    async def startup_event():
        """Log startup information."""
        logger.info("Climate Analytics API starting up")
        logger.info("API documentation available at /docs and /redoc")

    @app.on_event("shutdown")
    async def shutdown_event():
        """Log shutdown information."""
        logger.info("Climate Analytics API shutting down")

    return app


# Create the application instance
app = create_app()
