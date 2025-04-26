import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, String, DateTime, Text, Integer, ForeignKey, Numeric, Date, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

# Read the database URL from environment variables
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL environment variable is not set.")

# Create the SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# Create a configured "SessionLocal" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class User(Base):
    __tablename__ = 'users'
    __table_args__ = {'schema': 'shelfsense'}

    id = Column(UUID(as_uuid=True), primary_key=True, server_default=func.uuid_generate_v4())
    email = Column(String(254), nullable=False, unique=True)
    username = Column(String(255), nullable=False)
    password_hash = Column(String(60), nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())

    preferences = relationship('UserPreference', back_populates='user', uselist=False)
    library_entries = relationship('UserLibraryEntry', back_populates='user')
    recommendations = relationship('Recommendation', back_populates='user')
    recommendation_ratings = relationship('RecommendationRating', back_populates='user')

class Book(Base):
    __tablename__ = 'books'
    __table_args__ = {'schema': 'shelfsense'}

    id = Column(UUID(as_uuid=True), primary_key=True, server_default=func.uuid_generate_v4())
    title = Column(String(255), nullable=False)
    author = Column(String(255), nullable=False)
    isbn = Column(String(13), nullable=True)
    genre = Column(Text, nullable=True)
    description = Column(Text, nullable=True)
    publication_date = Column(Date, nullable=True)
    page_count = Column(Integer, nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())

    library_entries = relationship('UserLibraryEntry', back_populates='book')
    recommendations = relationship('Recommendation', back_populates='recommended_book')

class UserPreference(Base):
    __tablename__ = 'user_preferences'
    __table_args__ = {'schema': 'shelfsense'}

    id = Column(UUID(as_uuid=True), primary_key=True, server_default=func.uuid_generate_v4())
    user_id = Column(UUID(as_uuid=True), ForeignKey('shelfsense.users.id', ondelete='CASCADE'), nullable=False, unique=True)
    preferences_text = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())

    user = relationship('User', back_populates='preferences')

class UserLibraryEntry(Base):
    __tablename__ = 'user_library_entries'
    __table_args__ = {'schema': 'shelfsense'}

    id = Column(UUID(as_uuid=True), primary_key=True, server_default=func.uuid_generate_v4())
    user_id = Column(UUID(as_uuid=True), ForeignKey('shelfsense.users.id', ondelete='CASCADE'), nullable=False)
    book_id = Column(UUID(as_uuid=True), ForeignKey('shelfsense.books.id', ondelete='RESTRICT'), nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())

    user = relationship('User', back_populates='library_entries')
    book = relationship('Book', back_populates='library_entries')
    review = relationship('Review', back_populates='library_entry', uselist=False)

class Review(Base):
    __tablename__ = 'reviews'
    __table_args__ = {'schema': 'shelfsense'}

    id = Column(UUID(as_uuid=True), primary_key=True, server_default=func.uuid_generate_v4())
    user_library_entry_id = Column(UUID(as_uuid=True), ForeignKey('shelfsense.user_library_entries.id', ondelete='CASCADE'), nullable=False, unique=True)
    review_text = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())

    library_entry = relationship('UserLibraryEntry', back_populates='review')

class Recommendation(Base):
    __tablename__ = 'recommendations'
    __table_args__ = {'schema': 'shelfsense'}

    id = Column(UUID(as_uuid=True), primary_key=True, server_default=func.uuid_generate_v4())
    user_id = Column(UUID(as_uuid=True), ForeignKey('shelfsense.users.id', ondelete='CASCADE'), nullable=False)
    recommended_book_id = Column(UUID(as_uuid=True), ForeignKey('shelfsense.books.id', ondelete='RESTRICT'), nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())

    user = relationship('User', back_populates='recommendations')
    recommended_book = relationship('Book', back_populates='recommendations')
    rating = relationship('RecommendationRating', back_populates='recommendation', uselist=False)

class RecommendationRating(Base):
    __tablename__ = 'recommendation_ratings'
    __table_args__ = {'schema': 'shelfsense'}

    id = Column(UUID(as_uuid=True), primary_key=True, server_default=func.uuid_generate_v4())
    recommendation_id = Column(UUID(as_uuid=True), ForeignKey('shelfsense.recommendations.id', ondelete='CASCADE'), nullable=False, unique=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey('shelfsense.users.id', ondelete='CASCADE'), nullable=False)
    rating = Column(Numeric(2, 1), nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())

    recommendation = relationship('Recommendation', back_populates='rating')
    user = relationship('User', back_populates='recommendation_ratings')
