# `ACCOUNTS_MODULE.md`

# CattleCare Accounts Module Documentation

## Overview

The Accounts Module handles:

- User Registration
- Login & Authentication
- Role Management
- User Profiles
- Permissions
- Moderators & Managers
- Article Approval Roles

The system uses a custom Django authentication model.

---

# Features

- Custom User Model
- Email Authentication
- Role-based Access Control
- Admin / Manager / Moderator Roles
- Email Verification Ready
- Phone Verification Ready
- Profile Management
- Secure Password Hashing
- JWT Ready
- OAuth Ready

---

# User Roles

| Role | Description |
|---|---|
| User | Basic user |
| Author | Can create articles |
| Moderator | Can approve/reject articles |
| Manager | Can manage moderators |
| Admin | Full system access |

---

# Account Model

## Fields

| Field | Type | Description |
|---|---|---|
| `email` | EmailField | User email |
| `username` | CharField | Unique username |
| `name` | CharField | Full name |
| `phone` | CharField | Phone number |
| `location` | CharField | User location |
| `role` | CharField | User role |
| `approver_post` | CharField | Moderator designation |
| `email_verified` | Boolean | Email verification |
| `phone_verified` | Boolean | Phone verification |
| `date_joined` | DateTime | Registration time |
| `last_login` | DateTime | Last login |
| `is_admin` | Boolean | Admin access |
| `is_staff` | Boolean | Staff access |
| `is_superuser` | Boolean | Superuser access |

---

# Authentication Flow

```text
User Signup
     ↓
Account Created
     ↓
Login Authentication
     ↓
Role Permissions Applied
     ↓
Dashboard Access

---

# Signup API

## Endpoint

```http
POST /accounts/signup/
```

---

# Signup Payload

```json
{
  "email": "rahul@example.com",
  "username": "rahul",
  "password": "securepassword",
  "name": "Rahul Malu",
  "phone": "9876543210",
  "location": "Pune"
}
```

---

# Login API

## Endpoint

```http
POST /accounts/login/
```

---

# Login Payload

```json
{
  "email": "rahul@example.com",
  "password": "securepassword"
}
```

---

# Profile Features

Users can:

* Edit profile
* Change password
* Upload profile image
* View articles
* View bookmarks
* View comments

---

# Role Permissions

## User

* Read articles
* Comment
* Like
* Bookmark

---

## Author

* Create articles
* Edit own articles
* Delete own articles

---

## Moderator

* Approve articles
* Reject articles
* Moderate comments

---

## Manager

* Manage moderators
* Approve/reject articles
* View moderation analytics

---

## Admin

* Full access
* User management
* Role assignment
* System settings

---

# Admin Role Assignment

Admins can assign roles from Django Admin Panel.

## Example Roles

```text
Moderator
Manager
Chief Editor
Senior Content Reviewer
AI Research Analyst
```

---

# Security Features

* Password hashing
* CSRF protection
* Session authentication
* JWT ready
* API key support
* Rate limiting ready

---

# Future Enhancements

* OTP Verification
* Google Login
* GitHub OAuth
* Two-Factor Authentication
* JWT Authentication
* Social Login
* Profile Images
* Activity Logs
* Device Sessions
* Password Reset Email
* Account Locking
* AI-based Fraud Detection

---

# Recommended Production Setup

| Component        | Technology            |
| ---------------- | --------------------- |
| Authentication   | Django Auth           |
| Password Hashing | PBKDF2                |
| API              | Django REST Framework |
| Cache            | Redis                 |
| Email            | SMTP / SendGrid       |
| Storage          | AWS S3                |

---

# License

CattleCare Accounts Module

MIT License
