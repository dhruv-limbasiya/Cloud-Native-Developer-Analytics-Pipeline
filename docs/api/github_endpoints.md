# GitHub API Endpoints

## Overview

The platform extracts engineering data from the GitHub REST API.

Base URL

```
https://api.github.com
```

Authentication

```
Authorization: Bearer <GITHUB_TOKEN>
```

---

# Organization

Endpoint

```
GET /orgs/{organization}
```

Purpose

Retrieve organization information.

Fields

- id
- login
- name
- description
- blog
- location
- public_repos
- followers
- following
- created_at
- updated_at

---

# Repositories

Endpoint

```
GET /orgs/{organization}/repos
```

Purpose

Retrieve all repositories.

Important Fields

- id
- name
- full_name
- private
- language
- default_branch
- forks_count
- stargazers_count
- watchers_count
- open_issues_count
- created_at
- updated_at
- pushed_at

Used For

- Repository Analytics
- Language Analytics
- Growth Metrics

---

# Contributors

Endpoint

```
GET /repos/{owner}/{repo}/contributors
```

Fields

- login
- id
- contributions

Used For

- Developer Activity
- Top Contributors

---

# Commits

Endpoint

```
GET /repos/{owner}/{repo}/commits
```

Fields

- sha
- author
- commit date
- commit message

Used For

- Commit Analytics
- Engineering Productivity

---

# Pull Requests

Endpoint

```
GET /repos/{owner}/{repo}/pulls
```

Fields

- id
- number
- state
- title
- user
- created_at
- updated_at
- closed_at
- merged_at

Used For

- Merge Time
- PR Trends
- Developer Productivity

---

# Issues

Endpoint

```
GET /repos/{owner}/{repo}/issues
```

Fields

- id
- number
- state
- labels
- assignee
- created_at
- closed_at

Used For

- Issue Backlog
- Resolution Time

---

# Languages

Endpoint

```
GET /repos/{owner}/{repo}/languages
```

Purpose

Retrieve programming language distribution.

Example

```
{
    "Python": 240000,
    "C++": 52000,
    "Java": 14000
}
```

Used For

- Technology Distribution
- Language Popularity

---

# Pagination

GitHub returns paginated results.

Configuration

```
per_page = 100
page = 1
```

Pipeline continues until no more records are returned.

---

# Rate Limiting

Authenticated requests

```
5000 requests/hour
```

Pipeline strategy

- Retry
- Exponential Backoff
- Respect rate limit headers

---

# Error Handling

Handle

- 401 Unauthorized
- 403 Forbidden
- 404 Not Found
- 429 Rate Limited
- 500 Internal Server Error

Retry

Maximum retry count is configurable.

---

# Incremental Loading

The platform avoids unnecessary downloads by using

- Updated timestamps
- Pagination metadata
- Pipeline execution metadata

---

# Configuration

The organization is never hardcoded.

Example

```yaml
github:
  organizations:
    - tensorflow
```

Changing the organization requires only updating the configuration file.

---

# Endpoints Used

| Endpoint | Purpose |
|----------|---------|
| Organization | Organization metadata |
| Repositories | Repository information |
| Contributors | Developer analytics |
| Commits | Commit analytics |
| Pull Requests | PR analytics |
| Issues | Issue analytics |
| Languages | Technology analytics |

---

# Data Flow

```
GitHub API

↓

JSON Response

↓

Bronze Layer

↓

Silver Layer

↓

Gold Layer

↓

DuckDB

↓

Dashboard
```