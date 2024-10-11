### TaskSync project for unified task management between several users
The project consists of a server part and a client part. 
The server operates on the basis of microservice architecture and consists of **user**, **task** and **room** services (for users to work together on tasks), as well as **key service** (for passing external keys from the database through various microservices). 
All services are connected through an **api gateway**. It is based on synchronous communication between services (HTTP requests).
A minimalistic client for server requests (**C#** and **WPF**) has also been created.

## Server
Each microservice is lifted using the built-in flask server. The Flask framework is used for request management. Databases are based on PostgreSQL.