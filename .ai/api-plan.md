# REST API Plan

## 1. Resources

| Resource                | Database Table                      |
|------------------------|-------------------------------------|
| User                   | shelfsense.users                    |
| User Preferences       | shelfsense.user_preferences         |
| Book                   | shelfsense.books                    |
| User Library Entry     | shelfsense.user_library_entries     |
| Review                 | shelfsense.reviews                  |
| Recommendation         | shelfsense.recommendations          |
| Recommendation Rating  | shelfsense.recommendation_ratings   |

## 2. Endpoints

### 2.1. Authentication

#### Register
- **POST** `/auth/register`
- Create a new user account
- Request: `{ "email": string, "password": string }`
- Response: `{ "id": uuid, "email": string, "token": string }`
- Success: 201 Created
- Errors: 400 (invalid data), 409 (email exists)

#### Login
- **POST** `/auth/login`
- Authenticate user
- Request: `{ "email": string, "password": string }`
- Response: `{ "id": uuid, "email": string, "token": string }`
- Success: 200 OK
- Errors: 401 (invalid credentials)

### 2.2. User Profile

#### Get current user
- **GET** `/users/me`
- Get authenticated user's profile
- Response: `{ "id": uuid, "email": string, "created_at": string, "updated_at": string }`
- Success: 200 OK
- Errors: 401 (unauthorized)

#### Update user password
- **PUT** `/users/me/password`
- Change password
- Request: `{ "old_password": string, "new_password": string }`
- Response: `{ "message": string }`
- Success: 200 OK
- Errors: 400 (invalid), 401 (unauthorized)

### 2.3. User Preferences

#### Get preferences
- **GET** `/users/me/preferences`
- Response: `{ "id": uuid, "preferences_text": string, "updated_at": string }`
- Success: 200 OK
- Errors: 404 (not set), 401 (unauthorized)

#### Set/update preferences
- **PUT** `/users/me/preferences`
- Request: `{ "preferences_text": string }`
- Response: `{ "id": uuid, "preferences_text": string, "updated_at": string }`
- Success: 200 OK
- Errors: 400 (invalid), 401 (unauthorized)

### 2.4. Books

#### List books
- **GET** `/books`
- Query: `?search=string&author=string&genre=string&page=int&limit=int&sort=field`
- Response: `{ "items": [ ... ], "total": int, "page": int, "limit": int }`
- Success: 200 OK

#### Add book
- **POST** `/books`
- Request: `{ "title": string, "author": string, "isbn"?: string, "genre"?: string, "description"?: string, "publication_date"?: string, "page_count"?: int }`
- Response: `{ "id": uuid, ... }`
- Success: 201 Created
- Errors: 400 (invalid)

#### Get book by id
- **GET** `/books/{book_id}`
- Response: `{ ... }`
- Success: 200 OK
- Errors: 404

#### Update book
- **PUT** `/books/{book_id}`
- Request: `{ ... }`
- Response: `{ ... }`
- Success: 200 OK
- Errors: 400, 404

#### Delete book
- **DELETE** `/books/{book_id}`
- Success: 204 No Content
- Errors: 404, 409 (referenced)

### 2.5. User Library

#### List user's library
- **GET** `/users/me/library`
- Query: `?page=int&limit=int&sort=field`
- Response: `{ "items": [ ... ], "total": int, "page": int, "limit": int }`
- Success: 200 OK

#### Add book to library
- **POST** `/users/me/library`
- Request: `{ "book_id": uuid }`
- Response: `{ "id": uuid, "book_id": uuid, "created_at": string }`
- Success: 201 Created
- Errors: 400, 409 (already added)

#### Remove book from library
- **DELETE** `/users/me/library/{entry_id}`
- Success: 204 No Content
- Errors: 404

### 2.6. Reviews

#### Add review
- **POST** `/users/me/library/{entry_id}/review`
- Request: `{ "review_text": string }`
- Response: `{ "id": uuid, "review_text": string, "created_at": string }`
- Success: 201 Created
- Errors: 400, 409 (already exists)

#### Get review
- **GET** `/users/me/library/{entry_id}/review`
- Response: `{ "id": uuid, "review_text": string, "created_at": string }`
- Success: 200 OK
- Errors: 404

#### Update review
- **PUT** `/users/me/library/{entry_id}/review`
- Request: `{ "review_text": string }`
- Response: `{ "id": uuid, "review_text": string, "updated_at": string }`
- Success: 200 OK
- Errors: 400, 404

#### Delete review
- **DELETE** `/users/me/library/{entry_id}/review`
- Success: 204 No Content
- Errors: 404

### 2.7. Recommendations

#### Get recommendations
- **GET** `/users/me/recommendations`
- Query: `?page=int&limit=int&sort=field`
- Response: `{ "items": [ ... ], "total": int, "page": int, "limit": int }`
- Success: 200 OK

#### Rate recommendation
- **POST** `/users/me/recommendations/{recommendation_id}/rating`
- Request: `{ "rating": number }`
- Response: `{ "id": uuid, "rating": number, "created_at": string }`
- Success: 201 Created
- Errors: 400, 409 (already rated)

#### Update rating
- **PUT** `/users/me/recommendations/{recommendation_id}/rating`
- Request: `{ "rating": number }`
- Response: `{ "id": uuid, "rating": number, "updated_at": string }`
- Success: 200 OK
- Errors: 400, 404

#### Delete rating
- **DELETE** `/users/me/recommendations/{recommendation_id}/rating`
- Success: 204 No Content
- Errors: 404

### 2.8. AI Review Generation

#### Generate review template
- **POST** `/ai/review-template`
- Request: `{ "book_id": uuid, "notes"?: string }`
- Response: `{ "template": string }`
- Success: 200 OK
- Errors: 400

## 3. Authentication & Authorization
- JWT-based authentication (access token in Authorization header)
- Endpoints under `/users/me/*` and `/users/me` require authentication
- Passwords hashed with bcrypt
- RLS in DB for user data isolation

## 4. Validation & Business Logic

### Validation
- Email: valid format, unique
- Password: min length, complexity
- Book: title and author required, ISBN optional, page_count positive integer
- Preferences: non-empty string
- Review: non-empty string, one review per library entry
- Recommendation rating: 1.0-5.0, step 0.5, one rating per recommendation per user

### Business Logic
- User can only access/modify their own data (enforced by RLS and API checks)
- Cannot add the same book to library twice
- Cannot review a book not in user's library
- Cannot rate the same recommendation twice
- AI review template uses OpenAI SDK, not persisted until user saves
- Pagination, filtering, and sorting for list endpoints
- Defensive error handling and clear error messages

---
This plan is designed for a FastAPI backend with Pydantic models, JWT authentication, and PostgreSQL with RLS. All endpoints return JSON. Error responses follow a consistent structure: `{ "error": string, "details"?: object }`.
