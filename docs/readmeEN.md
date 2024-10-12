## TaskSync Project Overview

## Project Description.
**TaskSync** is a multi-user task management system built on a microservice architecture. The project allows users to work together on tasks within rooms using a system of roles and access rights.

### Main components:
- **User Service**: User management functionality is available
- Task Service**: Responsible for creating, editing, viewing and deleting tasks.
- Room Service**: Provides creation and management of rooms for collaborative work on tasks.
- Key Service: Used to transfer foreign keys between databases and services.
- API Gateway: Provides a single point of access to all microservices, facilitating communication between them.

### Client side:
- **Test Client**: A minimalistic client for testing server requests. Written in **C#** using **WPF**. It allows you to execute HTTP requests to the server by selecting methods and entering JSON for requests.

## Technologies
- Flask: Used to build the API in each microservice.
- **PostgreSQL**: A relational database for storing information about users, tasks, rooms, and foreign keys.
- Docker: All services are containerized to simplify deployment and isolate environments.
- HTTP (synchronous communication): Services communicate via HTTP requests to perform operations.

## Microservices architecture.
The project is built on the basis of several separate microservices:
- **User Service**: User management (registration and authorization functionality is not ready yet).
- Task Service**: Operations with tasks.
- Room Service: Create rooms and add users.
- Key Service: Integration with external keys.

Synchronous interaction between microservices is used via HTTP. All requests are managed through the **API Gateway**, which provides a single interface for front-end clients.

## Deployment.

### 1. **Local launch of services**.
For each microservice, you need to set up a development environment. Here are the basic steps to run the project locally:

#### Steps to run:
1. **Install dependencies**:
   Each microservice has its own `requirements.txt` file. To install the dependencies, run:
   ```
   pip install -r requirements.txt
   ```

2. **Configure the database**:
   Each microservice connects to its own PostgreSQL database. The database is configured through configuration files or environment variables.
   - Create databases for each service.
   - Write the connection to them in the corresponding `.env` files.

3. **Starting microservices**:
   After installing the dependencies and configuring the databases, start each service using the command:
   ```bash
   flask run
   ```

4. **API Gateway**:
   Run the API Gateway, which provides access to all services through a single endpoint.

### 2. **Run via Docker (recommended)**.
The project is containerized using Docker, so to simplify deployment, you can use Docker Compose to raise all microservices and databases at the same time.

#### Steps to run in Docker:

1. **Create Docker images for each service**:
   Each service has a Dockerfile. To create the images, run:
   ```
   docker compose build.
   ```

2. **Run through Docker Compose**:
   In the root folder of the project there is `docker-compose.yml` containing all the necessary services and databases. To run the project via Docker Compose, use:
   ```
   docker-compose up
   ```

   This will automatically start all the microservices and necessary databases in the containers.

3. **Checking the work**:
   After successful startup, all services will be available through the API Gateway. To check if the project is working, you can send a test request to the API Gateway.

### 3. **Setting up the environment**.
Depending on the environment (development, testing, or production), you may need different configuration files:
- `.env': A file for configuring environment variables such as database connections, secrets for JWT (when implemented), and Flask configuration.

### 4. **Database**:
   The project uses PostgreSQL. Database migrations can be performed through the appropriate migration scripts (if migrations are configured), or by creating tables when the services are started.

## Important note:
At the moment, **registration** and **user authorization** are still under development. This also applies to the functionality for working with **JWT tokens**. In future updates, support for these features will be added, allowing users to interact only with their accounts and rooms.