from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI(
    title="Unified API Simulator",
    version="1.0.0",
    contact={
        "name": "minhngocnguyen",
        "email": "minh2210.nina@gmail.com",
        "linkedin": "https://www.linkedin.com/in/minnguyen2210/"
    },
    license_info={
        "name": "MIT License"
    },
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Import routers after app is defined to avoid circular imports
from routers import cart_tracking_router

app.include_router(cart_tracking_router.router, prefix="/cart", tags=["Cart Tracking"])

@app.on_event("startup")
async def startup_event():
    """Initialize shared data on startup"""
    print("🚀 Starting TechStore Vietnam API Simulator...")
    from shared.data_generator import initialize_shared_data
    await initialize_shared_data()
    print("✅ Shared data initialized")
    print("📡 API available at http://localhost:8000")
    print("📚 Documentation at http://localhost:8000/docs")


@app.get("/", tags=["Root"])
async def root():
    """
    ## Root Endpoint

    Returns API overview and available data sources.
    """
    return {
        "status": "success",
        "msg": "TechStore Vietnam - Unified API Simulator",
        "data": {
            "service": "TechStore Vietnam - Unified API Simulator",
            "version": "4.0.0",
            "market": "Vietnam Technology Retail",
            "documentation": "/docs",
            "data_sources": {
                "tracking": {
                    "cart": "/cart/"
                }
            },
            "endpoints": {
                "cart": "/cart/"
            }
        }
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint"""
    return {
        "status": "success",
        "msg": "Service is healthy",
        "data": {
            "service": "Unified API",
            "status": "healthy"
        }
    }


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)