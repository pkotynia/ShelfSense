# Router for user preferences endpoints
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Annotated # Using Annotated for better dependency readability

# Assumption: schemas, models, dependencies, and services modules exist in their respective locations
from .. import schemas, models, dependencies
from ..services import preferences_service

# Create a router instance
# The /users prefix is used to group user-related endpoints
# The "preferences" tag will be used in the OpenAPI documentation (Swagger UI)
router = APIRouter(
    prefix="/users",
    tags=["preferences"],
)

# Type definitions for injected dependencies, using Annotated for readability
# DBSession will provide the SQLAlchemy database session
DBSession = Annotated[Session, Depends(dependencies.get_db)]
# CurrentUser will provide the SQLAlchemy model of the logged-in user (after JWT verification)
CurrentUser = Annotated[models.User, Depends(dependencies.get_current_user)]

@router.get("/me/preferences", response_model=schemas.PreferenceResponse)
async def read_user_preferences(
    # Dependency injection: database session
    db: DBSession,
    # Dependency injection: currently logged-in user
    current_user: CurrentUser,
):
    """
    Retrieves the preferences for the currently authenticated user.

    Raises:
        HTTPException(404): If the user preferences are not found.
    """
    # Call the service function to get user preferences
    preferences = preferences_service.get_user_preferences(db, current_user.id)

    # Check if preferences were found
    if preferences is None:
        # If not found, raise an HTTP 404 Not Found exception
        raise HTTPException(status_code=404, detail="User preferences not found")

    # If found, return the preferences object
    # FastAPI will automatically convert the SQLAlchemy model to the Pydantic model (PreferenceResponse)
    return preferences

@router.put("/me/preferences", response_model=schemas.PreferenceResponse)
async def update_user_preferences(
    # Request body: preference data to set/update
    # FastAPI will automatically validate it against the PreferenceRequest model
    preferences_data: schemas.PreferenceRequest,
    # Dependency injection: database session
    db: DBSession,
    # Dependency injection: currently logged-in user
    current_user: CurrentUser,
):
    """
    Sets or updates the preferences for the currently authenticated user.

    The request body must contain `preferences_text` which cannot be empty.

    Raises:
        HTTPException(500): If an internal server error occurs during the update.
    """
    # try...except block to handle potential errors during database operations
    try:
        # Call the service function to create or update preferences
        updated_preferences = preferences_service.upsert_user_preferences(
            db=db, user_id=current_user.id, preferences_data=preferences_data
        )
        # Return the updated/created preferences
        # FastAPI will automatically convert the SQLAlchemy model to the Pydantic model (PreferenceResponse)
        return updated_preferences
    except Exception as e:
        # In case of any exception during the service operation:
        # TODO: Add server-side error logging for diagnostic purposes
        # e.g., logger.error(f"Error updating preferences for user {current_user.id}: {e}")

        # Raise an HTTP 500 Internal Server Error exception with a generic message
        raise HTTPException(status_code=500, detail="Internal server error while updating preferences")
