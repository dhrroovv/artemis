# Artemis

Artemis is a small FastAPI-based authentication service built mainly as a learning project.

I made this project to practice FastAPI and to understand how authentication is commonly handled in real-world systems. The focus here was learning by building: user signup, login, password hashing, JWT-based access tokens, refresh tokens, protected routes, cookie handling, and logout flows.

This is not meant to be a full production-ready auth platform. It is a hands-on practice project that explores the core building blocks of an auth system using FastAPI, SQLAlchemy, PostgreSQL, and token-based authentication patterns.

## What this project covers

- User registration
- User login with credential validation
- Password hashing and verification
- JWT access token creation
- Refresh token creation and rotation flow basics
- Protected routes using bearer token auth
- `HttpOnly` refresh token cookies
- Logout by clearing the refresh token cookie
- Async database access with SQLAlchemy and PostgreSQL

## Why I built this

The goal of this project was to get practical experience with questions like:

- How does signup and login usually work in an API?
- How are passwords stored securely?
- What is the difference between access tokens and refresh tokens?
- Why do some systems return one token in the response body and store another in cookies?
- How do protected routes identify the currently authenticated user?
- What does logout look like in a token-based system?

## Tech stack

- FastAPI
- SQLAlchemy (async)
- PostgreSQL
- JWT-based authentication
- `pwdlib` for password hashing

## Authentication flow

This project uses a split token approach:

- On successful login, an `access_token` is returned in the response body.
- A `refresh_token` is stored as an `HttpOnly` cookie.
- Protected routes are accessed using `Authorization: Bearer <access_token>`.
- When the access token expires, the refresh token can be used to request a new access token.
- Logging out clears the refresh token cookie.

This setup was useful for practicing how modern auth systems often separate short-lived access tokens from longer-lived refresh tokens.

## API base path

All auth-related routes are mounted under:

```http
/artemis/auth
```

## Available endpoints

### `GET /artemis/auth/`

Simple test endpoint.

**Response**

```json
"hello world"
```

---

### `POST /artemis/auth/signup`

Creates a new user account.

**Request body**

```json
{
  "email": "user@example.com",
  "password": "your-password"
}
```

**Behavior**

- Checks whether the email already exists
- Hashes the password before storing it
- Creates and returns the new user
- Returns `403 Forbidden` if the email is already registered

---

### `POST /artemis/auth/login`

Authenticates a user and issues tokens.

**Request body**

```json
{
  "email": "user@example.com",
  "password": "your-password"
}
```

**Response behavior**

- Verifies the user exists
- Verifies the password against the stored hash
- Returns an `access_token` in the response body
- Sets a `refresh_token` as an `HttpOnly` cookie
- Returns `401 Unauthorized` for invalid credentials

**Example response**

```json
{
  "user": {
    "email": "user@example.com",
    "uid": "user-id"
  },
  "access_token": "<jwt-access-token>",
  "detail": "Login succesful!"
}
```

---

### `GET /artemis/auth/me`

Returns the currently authenticated user.

**Auth required**

Send the access token in the `Authorization` header:

```http
Authorization: Bearer <access_token>
```

**Behavior**

- Validates the access token
- Resolves the current authenticated user
- Returns user information for the active session

---

### `POST /artemis/auth/refresh`

Generates a new access token using the refresh token.

**Auth required**

- Expects a valid `refresh_token` cookie

**Behavior**

- Validates the refresh token from the cookie
- Returns a new access token if the refresh token is valid

---

### `POST /artemis/auth/logout`

Logs the user out by clearing the refresh token cookie.

**Behavior**

- Deletes the `refresh_token` cookie
- Returns a success message

**Example response**

```json
{
  "detail": "Logged out successfully"
}
```

## Notes

- In local development, cookie security behavior depends on environment settings.
- The refresh token cookie is set as `HttpOnly`.
- The project is intentionally focused on learning the mechanics of auth rather than covering every production hardening concern.
