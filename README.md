# E-commerce Backend System with Django REST Framework

A sophisticated, production-ready backend system for e-commerce applications, developed using the Django REST Framework. This project delivers secure, scalable, and containerized RESTful APIs for product lifecycle management, user authentication, shopping cart workflows, and order processing. The backend is architected with Docker Compose, utilizing PostgreSQL for relational data storage, Redis for performance-oriented caching, and MinIO as an S3-compatible solution for object storage.

---


## Technology Stack

- **Language & Framework:** Python 3.11+, Django 5.2.4
- **API Framework:** Django REST Framework 3.16.0
- **Database:** PostgreSQL
- **Cache Layer:** Redis
- **Object Storage:** MinIO (S3 API-compatible)
- **Deployment & Orchestration:** Docker, Docker Compose
- **Network Tunnel (Optional):** Cloudflare Tunnel
- **Payment Service Provider (PSP):** (Stripe - Paymob)  

---

## Key Capabilities

- **User Authentication:** Secure JSON Web Token (JWT) authentication powered by .
- **Product and Category Management:** Full CRUD operations for both products and categories.
- **Shopping Cart System:** Add, remove, and update items with immediate backend synchronization and persistent storage.
- **Order Management:** Comprehensive order creation and historical retrieval.
- **Media Handling:** Efficient file uploads and retrievals through MinIO.
- **Caching Layer:** Integrated Redis support to improve performance and reduce latency.
- **Fully Dockerized:** Cross-platform deployment via Docker Compose.

