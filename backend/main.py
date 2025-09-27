from fastapi import FastAPI, HTTPException, Request, Header, status
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from backend.routers import plans
from backend.db.connection import connect_to_mongo, close_mongo_connection
import uvicorn
from fastapi.exceptions import RequestValidationError

# Initialize FastAPI app
app = FastAPI(
    title="FirstDemo REST API",
    description="REST API that can handle any structured data in JSON format using FastAPI and MongoDB",
    version="1.0.0",
)
# startup and shutdown events for MongoDB connection management
@app.on_event("startup")
async def startup_event():
    await connect_to_mongo()

@app.on_event("shutdown")
async def shutdown_event():
    await close_mongo_connection()

# Include routers
app.include_router(plans.router, prefix="/api/v1", tags=["plans"])

@app.get("/", status_code=status.HTTP_200_OK)
async def root():
    """Root endpoint providing API information"""
    return {
        "message": "FirstDemo REST API",
        "version": "1.0.0",
        "description": "REST API with support for CRD operations on structured JSON data"
    }

@app.get("/health", status_code=status.HTTP_200_OK)
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "message": "API is running"}

@app.exception_handler(RequestValidationError)
async def request_validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=400,  
        content={
            "error": "Invalid request payload",
            "details": exc.errors()
        },
    )

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)