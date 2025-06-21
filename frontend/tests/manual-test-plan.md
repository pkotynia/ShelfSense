# Manual Test Plan for Authentication

## Prerequisites
1. Start backend server: `python -m uvicorn app.main:app --reload`
2. Start frontend dev server: `npm run dev` in the frontend directory
3. Clear browser storage (localStorage) to ensure clean test state

## Test Cases

### 1. Registration Flow
- Navigate to /register
- Test form validation:
  - Empty email
  - Invalid email format
  - Password less than 8 characters
  - Password without numbers
  - Password without letters
- Test successful registration:
  - Valid email (e.g., test@example.com)
  - Valid password (e.g., TestPass123)
- Expected: Redirect to dashboard after success

### 2. Login Flow
- Navigate to /login
- Test form validation:
  - Empty email
  - Invalid email format
  - Empty password
- Test error cases:
  - Non-existent email
  - Wrong password for existing email
- Test successful login with registered credentials
- Expected: Redirect to dashboard after success

### 3. Protected Routes
- Try accessing /dashboard without auth
- Expected: Redirect to login
- Login successfully
- Try accessing /dashboard again
- Expected: Access granted

### 4. Navigation & Logout
- Verify navigation header appears after login
- Test logout button
- Expected: Redirect to login
- Try browser back button
- Expected: Should not access protected routes

### 5. Error Handling
- Test network errors:
  - Disable network to test offline state
  - Invalid API responses
- Test form error messages:
  - Should display validation errors below fields
  - Should display API errors in alert

## Test Results Template
For each test case, note:
- ✅ Pass / ❌ Fail
- Actual behavior if different from expected
- Browser console errors if any
- Network requests (status codes)
