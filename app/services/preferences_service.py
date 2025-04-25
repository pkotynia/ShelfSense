# Service layer for user preferences
from sqlalchemy.orm import Session
from sqlalchemy import select, update, insert
from uuid import UUID

from .. import models, schemas

def get_user_preferences(db: Session, user_id: UUID) -> models.UserPreference | None:
    """
    Fetches preferences for a specific user from the database.

    Args:
        db: The SQLAlchemy database session.
        user_id: The UUID of the user whose preferences are to be fetched.

    Returns:
        The UserPreference object if found, otherwise None.
    """
    # Construct a SELECT statement to find the UserPreference record
    # matching the provided user_id.
    statement = select(models.UserPreference).where(models.UserPreference.user_id == user_id)
    # Execute the statement and retrieve the first result (or None if no match).
    # scalar_one_or_none() is suitable for fetching zero or one row.
    result = db.execute(statement)
    return result.scalar_one_or_none()

def upsert_user_preferences(db: Session, user_id: UUID, preferences_data: schemas.PreferenceRequest) -> models.UserPreference:
    """
    Creates or updates preferences for a specific user in the database.
    'Upsert' means it will UPDATE if the record exists, or INSERT if it doesn't.

    Args:
        db: The SQLAlchemy database session.
        user_id: The UUID of the user whose preferences are being set/updated.
        preferences_data: The Pydantic model containing the new preferences text.

    Returns:
        The created or updated UserPreference object.
    """
    # First, try to get existing preferences for the user.
    existing_prefs = get_user_preferences(db, user_id)

    if existing_prefs:
        # If preferences already exist, update the text.
        # SQLAlchemy tracks changes to the object.
        existing_prefs.preferences_text = preferences_data.preferences_text
        # Note: The 'updated_at' timestamp is handled automatically by the
        # database trigger defined in schema.sql.
        db.commit() # Commit the transaction to save the changes.
        db.refresh(existing_prefs) # Refresh the object to get the latest state from DB (like updated_at).
        return existing_prefs
    else:
        # If preferences don't exist, create a new record.
        new_prefs = models.UserPreference(
            user_id=user_id,
            preferences_text=preferences_data.preferences_text
            # 'id', 'created_at', 'updated_at' are handled by the database defaults/triggers.
        )
        db.add(new_prefs) # Add the new object to the session.
        db.commit() # Commit the transaction to insert the new record.
        db.refresh(new_prefs) # Refresh the object to get DB-generated values (id, timestamps).
        return new_prefs
