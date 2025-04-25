from fastapi import FastAPI

# Import the router for user preferences
from .routers import preferences

# Create the FastAPI application instance
# You can add metadata like title, version, etc. here
# e.g., app = FastAPI(title="ShelfSense API", version="0.1.0")
app = FastAPI()

# Include the preferences router in the application
# All routes defined in the preferences router will now be available
# under the prefix specified in the router (e.g., /users)
app.include_router(preferences.router)

# You can add other routers here as the application grows
# from .routers import another_router
# app.include_router(another_router.router)

# Optional: Add a root endpoint for basic health check or welcome message
@app.get("/")
async def read_root():
    """
    Root endpoint providing a simple welcome message.
    """
    return {"message": "Welcome to ShelfSense API"}

# If you have database initialization or other startup/shutdown logic,
# you can add event handlers:
# @app.on_event("startup")
# async def startup_event():
#     # Initialize database, etc.
#     pass
#
# @app.on_event("shutdown")
# async def shutdown_event():
#     # Clean up resources, etc.
#     pass
