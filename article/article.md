# `ARTICLES_MODULE.md`

# CattleCare Articles Module Documentation

## Overview

The Articles Module provides:

- Article Publishing
- Article Approval Workflow
- Categories & Tags
- SEO Optimization
- Likes & Comments
- Bookmarks
- Search System
- Moderation Dashboard

Articles are stored in MongoDB.

---

# Features

- MongoDB Storage
- Rich Article System
- Role-based Moderation
- SEO Metadata
- Tags & Categories
- Search Functionality
- Likes System
- Comment System
- Bookmark System
- Draft & Approval Workflow

---

# Article Workflow

```text
Author Creates Article
        ↓
Status = Pending
        ↓
Moderator Review
        ↓
Approved / Rejected
        ↓
Published Publicly

---

# MongoDB Collections

| Collection  | Purpose              |
| ----------- | -------------------- |
| `articles`  | Main article storage |
| `likes`     | Article likes        |
| `comments`  | User comments        |
| `bookmarks` | Saved articles       |

---

# Article Document Structure

```json
{
  "title": "AI in Smart Farming",
  "category": "Technology",
  "article_tags": [
    "AI",
    "IoT"
  ],
  "image": "https://example.com/image.jpg",
  "content": "Full article content",
  "author": "rahul",
  "status": "approved",
  "approved_by": "manager01",
  "approver_post": "Chief Editor",
  "meta_title": "AI in Smart Farming",
  "meta_description": "AI improves smart farming...",
  "created_at": "2026-05-15"
}
```

---

# Article Status

| Status     | Description           |
| ---------- | --------------------- |
| `pending`  | Awaiting review       |
| `approved` | Published             |
| `rejected` | Rejected by moderator |
| `draft`    | Private draft         |

---

# Article Features

## Categories

Examples:

* Technology
* Health
* Nutrition
* IoT
* Dairy
* Research

---

## Tags

Examples:

```text
AI
IoT
Machine Learning
Farming
Livestock
Sensors
Health Monitoring
```

---

# Article APIs

## Create Article

```http
POST /articles/create/
```

---

## Article List

```http
GET /articles/
```

---

## Article Detail

```http
GET /articles/<article_id>/
```

---

## Edit Article

```http
POST /articles/edit/<article_id>/
```

---

## Delete Article

```http
POST /articles/remove/<article_id>/
```

---

# Likes System

Users can:

* Like articles
* Remove likes
* View total likes

---

# Comments System

Users can:

* Add comments
* Delete comments
* Reply system ready

---

# Bookmark System

Users can:

* Save articles
* View saved articles
* Remove bookmarks

---

# Search System

Supports:

* Title search
* Content search
* Category filtering
* Tag filtering

MongoDB Full-Text Search is used.

---

# SEO Optimization

Each article contains:

| Field              | Purpose                   |
| ------------------ | ------------------------- |
| `meta_title`       | SEO title                 |
| `meta_description` | Search engine description |

---

# Moderation System

Moderators can:

* Approve articles
* Reject articles
* Delete inappropriate content
* Manage reports

---

# Approver Posts

Examples:

```text
Chief Editor
Senior Moderator
Research Manager
AI Content Reviewer
```

---

# Recommended User Roles

| Role      | Access                   |
| --------- | ------------------------ |
| User      | Read articles            |
| Author    | Create/Edit own articles |
| Moderator | Approve/Reject           |
| Manager   | Manage moderation        |
| Admin     | Full access              |

---

# Article Detail Features

* Hero banners
* Tags
* Share button
* Related articles ready
* Dark mode support
* Responsive UI
* Comments section
* Like system
* Bookmark system

---

# Security Features

* Role-based permissions
* Author ownership checks
* MongoDB validation
* CSRF protection
* API security ready

---

# Future Enhancements

* Rich Text Editor
* Markdown Support
* AI Article Generation
* Scheduled Publishing
* Reading Analytics
* Trending Articles
* Recommendation Engine
* Related Articles
* AI Moderation
* Voice Articles
* Image Uploads
* Video Embeds
* Newsletter Integration

---

# Recommended Production Stack

| Component     | Technology          |
| ------------- | ------------------- |
| Backend       | Django              |
| Database      | MongoDB             |
| Search        | MongoDB Text Search |
| Media Storage | Cloudinary / AWS S3 |
| Cache         | Redis               |
| Realtime      | WebSockets          |

---

# License

CattleCare Articles Module

MIT License
