Ось документація у форматі `.md` для вашого проєкту:

---

# TaskSync Documentation

## Table of Contents
- [Overview](#overview)
- [Services](#services)
  - [API Gateway](#api-gateway)
  - [Users Service](#users-service)
  - [Rooms Service](#rooms-service)
  - [Tasks Service](#tasks-service)
- [Database Setup](#database-setup)
- [Endpoints](#endpoints)
  - [API Gateway Endpoints](#api-gateway-endpoints)
  - [Users Service Endpoints](#users-service-endpoints)
  - [Rooms Service Endpoints](#rooms-service-endpoints)
  - [Tasks Service Endpoints](#tasks-service-endpoints)
- [Docker Compose Setup](#docker-compose-setup)

---

## Overview

**TaskSync** is a microservices-based application that enables users to manage tasks within rooms. The system consists of four main services: API Gateway, Users Service, Rooms Service, and Tasks Service. Each service interacts with a dedicated PostgreSQL database, and the services are containerized using Docker.

## Services

### API Gateway

The API Gateway aggregates the data from the `Users`, `Rooms`, and `Tasks` services and serves as the main entry point for the client. It caches data using `Flask-Caching` to reduce load on the underlying services.

### Users Service

The `Users Service` handles user management, including creating, updating, retrieving, and deleting users. It uses PostgreSQL as its database.

### Rooms Service

The `Rooms Service` manages rooms and the users assigned to them. It allows adding/removing users to/from rooms and automatically deletes rooms when they no longer have any users.

### Tasks Service

The `Tasks Service` manages the creation, updating, deletion, and retrieval of tasks. Each task is associated with a room and a user, and tasks have statuses (`pending`, `in progress`, `completed`).

## Database Setup

Each service uses its own PostgreSQL database, which is automatically set up by Docker Compose. The databases are as follows:
- `users_db`: Used by the `Users Service`
- `rooms_db`: Used by the `Rooms Service`
- `tasks_db`: Used by the `Tasks Service`

## Endpoints

### API Gateway Endpoints

**Base URL**: `/`

- **GET `/`**  
  Retrieves aggregated data from the `Users`, `Rooms`, and `Tasks` services.

  **Response**:
  ```json
  {
    "users": [...],
    "rooms": [...],
    "tasks": [...]
  }
  ```

- **GET `/rooms`**  
  Fetches the list of rooms.

- **GET `/tasks`**  
  Fetches the list of tasks.

### Users Service Endpoints

**Base URL**: `/users`

- **GET `/users`**  
  Fetches the list of users.

  **Response**:
  ```json
  [
    {
      "id": 1,
      "username": "user1"
    }
  ]
  ```

- **GET `/users/<int:id>`**  
  Fetches details of a specific user by `id`.

  **Response**:
  ```json
  {
    "id": 1,
    "username": "user1",
    "password_hash": "hashed_password"
  }
  ```

- **POST `/users`**  
  Creates a new user. Requires `username` and `password`.

  **Request**:
  ```json
  {
    "username": "user1",
    "password": "secure_password"
  }
  ```

  **Response**:
  ```json
  {
    "message": "User created successfully"
  }
  ```

- **PUT `/users/<int:id>`**  
  Updates an existing user.

  **Request**:
  ```json
  {
    "username": "new_username",
    "password_hash": "new_password_hash"
  }
  ```

- **DELETE `/users/<int:id>`**  
  Deletes an existing user by `id`.

  **Response**:
  ```json
  {
    "message": "User deleted successfully"
  }
  ```

### Rooms Service Endpoints

**Base URL**: `/rooms`

- **GET `/rooms`**  
  Fetches the list of rooms with associated users.

  **Response**:
  ```json
  [
    {
      "room_id": 1,
      "code": "room123",
      "user_ids": [1, 2]
    }
  ]
  ```

- **GET `/rooms/<int:id>`**  
  Fetches details of a specific room by `id`.

  **Response**:
  ```json
  {
    "room_id": 1,
    "code": "room123",
    "user_ids": [1, 2]
  }
  ```

- **POST `/rooms`**  
  Creates a new room. Requires `user_id` and `code`.

  **Request**:
  ```json
  {
    "user_id": 1,
    "code": "room123"
  }
  ```

  **Response**:
  ```json
  {
    "message": "Room created successfully"
  }
  ```

- **POST `/rooms/<int:room_id>/users`**  
  Adds a user to a room.

  **Request**:
  ```json
  {
    "user_id": 1
  }
  ```

  **Response**:
  ```json
  {
    "message": "User added to the room successfully"
  }
  ```

- **DELETE `/rooms/<int:room_id>/users/<int:user_id>`**  
  Removes a user from a room.

  **Response**:
  ```json
  {
    "message": "User removed from the room successfully"
  }
  ```

### Tasks Service Endpoints

**Base URL**: `/tasks`

- **GET `/tasks`**  
  Fetches the list of tasks.

  **Response**:
  ```json
  [
    {
      "id": 1,
      "user_id": 1,
      "room_id": 1,
      "title": "Task title",
      "description": "Task description",
      "status": "pending",
      "deadline": "2023-12-01T00:00:00Z"
    }
  ]
  ```

- **GET `/tasks/<int:id>`**  
  Fetches details of a specific task by `id`.

  **Response**:
  ```json
  {
    "id": 1,
    "user_id": 1,
    "room_id": 1,
    "title": "Task title",
    "description": "Task description",
    "status": "pending",
    "deadline": "2023-12-01T00:00:00Z"
  }
  ```

- **POST `/tasks`**  
  Creates a new task.

  **Request**:
  ```json
  {
    "user_id": 1,
    "room_id": 1,
    "title": "New Task",
    "description": "Task description",
    "deadline": "2023-12-01T00:00:00Z"
  }
  ```

  **Response**:
  ```json
  {
    "message": "Task created successfully"
  }
  ```

- **PUT `/tasks/<int:id>`**  
  Updates an existing task.

  **Request**:
  ```json
  {
    "title": "Updated title",
    "status": "in progress"
  }
  ```

- **DELETE `/tasks/<int:id>`**  
  Deletes a task by `id`.

  **Response**:
  ```json
  {
    "message": "Task deleted successfully"
  }
  ```

## Docker Compose Setup

This project uses `Docker Compose` to manage services. Below is the setup for the `docker-compose.yml` file:

```yaml
version: '3.8'

services:
  db_users:
    image: postgres:13
    environment:
      POSTGRES_USER: username
      POSTGRES_PASSWORD: password
      POSTGRES_DB: users_db
    volumes:
      - postgres_data_users:/var/lib/postgresql/data
    ports:
      - "5431:5432"

  db_rooms:
    image: postgres:13
    environment:
      POSTGRES_USER: username
      POSTGRES_PASSWORD: password
      POSTGRES_DB: rooms_db
    volumes:
      - postgres_data_rooms:/var/lib/postgresql/data
    ports:
      - "5433:5432"

  db_tasks:
    image: postgres:13
    environment:
      POSTGRES_USER: username
      POSTGRES_PASSWORD: password
      POSTGRES_DB: tasks_db
    volumes:
      - postgres_data_tasks:/var/lib/postgresql/data
    ports:
      - "5434:5432"

  users_service:
    build: ./users_service
    environment:
      DATABASE_URL: postgresql://username:password@db_users:5432/users_db
    depends_on:
      - db_users
    ports:
      - "5001:5000"

  rooms_service:
    build: ./rooms_service
    environment:
      DATABASE_URL: postgresql://username:password@db_rooms:5432/rooms_db
    depends_on:
      - db_rooms
    ports:
      - "5002:5000"
    
  tasks_service:
    build: ./tasks_service
    environment:
      DATABASE_URL: postgresql://username:password@db_tasks:5432/tasks_db
    depends_on:
      - db_tasks
    ports:
      - "5003:500

0"

  api_gateway:
    build: ./api_gateway
    ports:
      - "5000:5000"
    depends_on:
      - users_service
      - rooms_service
      - tasks_service

volumes:
  postgres_data_users:
  postgres_data_rooms:
  postgres_data_tasks:
```

### Running the Project

1. Install `Docker` and `Docker Compose`.
2. Clone the repository.
3. Run the following command to start all services:
   ```bash
   docker-compose up --build
   ```
4. Access the API Gateway at `http://localhost:5000`.