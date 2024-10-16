# TaskSync API Documentation
## Overview
**TaskSync** - is a multi-user task management system with support for shared task lists (rooms). This documentation is intended for third-party developers and contains information about the public api of the project.

## Base URL
All requests should be sent to the API Gateway:
[http://localhost:5000/api](http://localhost:5000/api)

## Endpoints
### Users
<details>
<summary>

#### User registration

</summary>

- **URL:** `api/users`
- **Method**: <mark>POST</mark>
- **Description**: Створює нового користувача
**Request body**
```json
{
    "username": "user001",
    "password": "StrongPassword321!",
    "email": "user001@fakemail.com"
}
```
**Responses:**
**201 *Created***
```json
{
    "message": "User created successfully.",
    "user_id": 1
}
```
**422 *Unprocessable Entity***
```json
{
    "error": "Invalid data. 'username', 'email' and 'password' are required."
}
```
**409 *Conflict***
```json
{
    "error": "User already exists. 'username' and 'email' must be unique".
}
```
**500 *Internal Server Error***
```json
{
    "error": "details"
}
```
</details>

<details>
<summary>

#### Getting the user

</summary>

- **URL:** `api/users/{user_id}`
- **Method**: <mark>GET</mark>
- **Description**: Getting a user by id

- **URL:** `api/user/{username}`
- **Method**: <mark>GET</mark>
- **Description**: Getting a user by username

**Responses:**
**200 *OK***
```json
{
    "user_id": 1,
    "username": "user001",
    "password": "StrongPassword321!",
    "email": "user001@fakemail.com"
}
```
**404 *Not found***
```json
{
    "error": "User is not found"
}
```
**500 *Internal Server Error***
```json
{
    "error": "details"
}
```
</details>

<details>
<summary>

#### Editing users

</summary>

- **URL:** `api/users/{user_id}`
- **Method**: <mark>PUT</mark>
- **Description**: Getting a user by id
**Request body**
```json
{
    "username": "user002",
    "email": "new@fakemail.com",
    "password": "NewPass"
}
```

**Responses**
**200 *OK***
```json
{
    "message": "User updated successfully."
}
```
**404 *Not found***
```json
{
    "error": "User is not found."
}
```
**500 *Internal server error***
```json
{
    "error": "details"
}
```
</details>

<details>
<summary>

#### Deleting a user

</summary>

- **URL:** `api/users/{user_id}`
- **Method**: <mark>DELETE</mark>
- **Description**: Deleting a user by id

**Responses**
**204 *No Content***
**404 *Not found***
```json
{
    "error": "User is not found."
}
```
**500 *Internal server error***
```json
{
    "error": "details"
}
```
</details>

<details>
<summary>

#### Getting user rooms

</summary>

- **URL:** `api/users/{user_id}/rooms`
- **Method**: <mark>GET</mark>
- **Description**: Get all the rooms the user enters

**Responses**
**200 *OK***
```json
[
    {
        "room_id": 1,
        "user_id": 1,
        "code": "1AoQ",
        "title": "Awesome room",
        "description": "Lorem ipsum dolor laborum"
    },
    {
        "room_id": 16,
        "user_id": 1,
        "code": "123AAA",
        "title": "AHAHAHAHA Penis",
        "description": ""
    }
]
```
**404 *Not found***
```json
{
    "error": "User is not found or has no rooms"
}
```
**500 *Internal Server Error***
```json
{
    "error": "details"
}
```
</details>

<details>
<summary>

#### Receiving user tasks

</summary>

- **URL:** `api/users/{user_id}/rooms`
- **Method**: <mark>GET</mark>
- **Description**: Receive all tasks created by the user

**Responses**
**200 *OK***
```json
[
    {
        "task_id": 1,
        "title": "Buy a cow",
        "user_id": 1,
        "room_id": 6,
        "deadline": "01-04-2024",
        "status": 2
    },
    {
        "task_id": 125,
        "title": "Create a farm",
        "user_id": 1,
        "room_id": 8,
        "deadline": "01-04-2024",
        "status": 3
    }
]
```
**404 *Not found***
```json
{
    "error": "User is not found or has no tasks"
}
```
**500 *Internal Server Error***
```json
{
    "error": "details"
}
```
</details>

### Tasks
<details>
<summary>

#### Create a task

</summary>

- **URL:** `/api/tasks`
- **Method:** <mark>POST</mark>
- **Description:** Publishing a new task
**Request body**
```json
{
    "title": "Default",
    "user_id": 1,
    "room_id": 1,
    "deadline": "2024-04-01T00:00:00Z",
    "status": 3 
}
```

**Responses**
**201 *Created***
```json
{
    "message": "Task creared successfully",
    "task_id": 6
}
```
**422 *Unprocessable value***
```json
{
    "error": "Invalid data. 'title', 'user_id' and 'room_id' are required"
}
```
**500 *Internal Server Error***
```json
{
    "error": "details"
}
```
</details>

<details>
<summary>

#### Getting a specific task by ID

</summary>

- **URL:** `/api/tasks/{task_id}`
- **Methodи:** <mark>GET</mark>
- **Description:** 

**Responses**
- **200 *OK***
```json
{
  "id": 1,
  "title": "Fix the bug in the authentication system",
  "description": "There's a critical bug in the login feature that prevents users from logging in under certain conditions.",
  "user_id": 2,
  "room_id": 1,
  "deadline": "2024-10-20T10:00:00Z",
  "status": "pending"
}
```
- **404 *Not Found***
```json
{
  "error": "Task is not found."
}
```
- **500 *Internal Server Error***
```json
{
  "error": "details"
}
```
</details>

<details>
<summary>

#### Edit a specific task by ID

</summary>

- **URL:** `/api/tasks/{task_id}`
- **Methodи:** <mark>PUT</mark>
- **Description:** Updates an existing task by its ID.

**Тіло запиту**
```json
{
  "title": "New title",
  "description": "New description",
  "user_id": 5,
  "room_id": 2,
  "deadline": "2024-11-01T12:00:00Z",
  "status": "completed"
}
```

**Responses**
- **200 *OK***
```json
{
  "message": "Task updated successfully."
}
```
- **404 *Not Found***
```json
{
  "error": "Task is not found."
}
```
- **422 *Unprocessable Entity***
```json
{
  "error": "Invalid status value. (1, 2, 3) are possible."
}
```
- **500 *Internal Server Error***
```json
{
  "error": "details"
}
```
</details>

<details>
<summary>

#### Delete a specific task by ID

</summary>

- **URL:** `/api/tasks/{task_id}`
- **Methodи:** <mark>DELETE</mark>
- **Description:** Deletes an existing task by its ID.

**Responses**
- **204 *No Content***    
- **404 *Not Found***
```json
{
  "error": "Task is not found."
}
```
- **500 *Internal Server Error***
```json
{
  "error": "details"
}
```
</details>

### Rooms
<details>
<summary>

#### Creating a room

</summary>

- **URL:** `/api/rooms`
- **Method:** <mark>POST</mark>
- **Description:** Creating a new room, to which the user who created it is automatically added (tasks cannot exist without belonging to any room)
**Request body**
```json
{
    "user_id": 1,
    "code": "0000",
    "title": "Default Room",
    "description": "AAAAAAAAAAAAAAAAAAAA Im so tired"
}
```

**Responses**
**201 *Created***
```json
{
    "message": "Room created successfully",
    "room_id": "1"
}
```
**422 *Unprocessable Entity***
```json
{
    "error": "Invalid data. 'user_id' and 'code' are required"
}
```
**409 *Conflict***
```json
{
    "error": "Room already exists. 'code' must be unique"
}
```
**500 *Internal Service Error***
```json
{
    "error": "details"
}
```
</details>

<details>
<summary>

#### Getting a specific room (code)

</summary>

- **URL:** `/api/rooms/{code}`
- **Method:** <mark>GET</mark>
- **Description:** Getting a room by its individual code

**Responses**
**200 *OK***
```json
{
    "id": 2,
    "user_id": 3,
    "code": "XYZ456",
    "title": "Design Team",
    "description": "Room for the design team to share ideas and collaborate."
}
```
**404 *Not found***
```json
{
    "error": "Room is not found."
}
```
**500 *Internal Server Error***
```json
{
    "error": "details"
}
```
</details>

<details>
<summary>

#### Getting a specific room (number)

</summary>

- **URL:** `/api/rooms/{room_id}`
- **Method:** <mark>GET</mark>
- **Description:** Getting a room by its id

**Responses**
**200 *ОК***
```json
{
    "id": 1,
    "user_id": 2,
    "code": "ABC123",
    "title": "Project Planning",
    "description": "Room for project planning and task coordination."
}
```
**404 *Not found***
```json
{
    "error": "Room is not found."
}
```
**500 *Internal Server Error***
```json
{
    "error": "details"
}
```
</details>

<details>
<summary>

#### Delete a room

</summary>

- **URL:** `/api/rooms/{room_id}`
- **Method:** <mark>DELETE</mark>
- **Description:** Deleting a room by its id

**Responses**
**204 *No Content***
**404 *Not found***
```json
{
    "error": "Room is not found."
}
```
**500 *Internal Server Error***
```json
{
    "error": "details"
}
```
</details>

<details>
<summary>

#### Getting users in the room

</summary>

- **URL:** `/api/rooms/{room_id}/users`
- **Method:** <mark>GET</mark>
- **Description:** A list of all users assigned to a specific room.

**Responses**
**200 *ОК***
```json
[
    {
        "user_id": 1,
        "username": "user001",
        "password": "StrongPassword321!",
        "email": "user001@fakemail.com"
    },
    {
        "user_id": 2,
        "username": "user002",
        "password": "StrongPassword321!",
        "email": "user002@fakemail.com"
    }
]
```
**404 *Not found***
```json
{
    "fatal": "Room does not exist or there are no users in room."
}
```
**Примітка:** *If you receive this error, check the availability of the room by its room number. If the room exists, but you still receive the error, it may mean that the room was not deleted after all users were removed, which can lead to significant memory leaks.*

**500 *Internal Server Error***
```json
{
    "error": "details"
}
```
</details>

<details>
<summary>

#### Receiving room assignments

</summary>

- **URL:** `/api/rooms/{room_id}/tasks`
- **Method:** <mark>GET</mark>
- **Description:** A list of all tasks inside the room.

**Responses**
**200 *ОК***
```json
[
  {
    "id": 1,
    "title": "Fix the bug in the authentication system",
    "description": "There's a critical bug in the login feature that prevents users from logging in under certain conditions.",
    "user_id": 2,
    "room_id": 1,
    "deadline": "2024-10-20T10:00:00Z",
    "status": "pending"
  },
  {
    "id": 2,
    "title": "Create project documentation",
    "description": "Document the API endpoints, data models, and overall project architecture for future reference.",
    "user_id": 4,
    "room_id": 1,
    "deadline": "2024-10-22T16:30:00Z",
    "status": "in_progress"
  }
]
```
**404 *Not found***
```json
{
    "error": "Room is not found or contains no tasks"
}
```
**500 *Internal Server Error***
```json
{
    "error": "details"
}
```
</details>

<details>
<summary>

#### Join a user to a room

</summary>

- **URL:** `/api/rooms/join`
- **Method:** <mark>POST</mark>
- **Description:** Assigns a specific user to a specific room.
**Request body**
```json
{
    "user_id": 1,
    "room_id": 1
}
```

**Responses**
**201 *ОК***
```json
{
    "message": "User joined the room."
}
```
**404 *Not found***
```json
{
    "error": "User is not found"
}
```
or
```json
{
    "error": "Room is not found" 
}
```
**409 *Conflict***
```json
{
    "error": "User is already joined."
}
```
**422 *Unprocessable value***
```json
{
    "error": "Invalid data. 'user_id' and 'room_id' are required"
}
```
**500 *Internal Server Error***
```json
{
    "error": "details"
}
```
</details>

<details>
<summary>

#### Disconnecting a user from a room

</summary>

- **URL:** `/api/rooms/remove`
- **Methodи:** <mark>DELETE</mark>
- **Description:** Disconnects a specific user from a specific room
**Request body**
```json
{
    "user_id": 1,
    "room_id": 1
}
```

**Responses**
**200 *OK***
```json
{
    "message": "User removed from room successfully."
}
```
**204 *No Content***
**Примітка:** *The user is disconnected and the room is deleted because there are no users left in it*
**404 *Not found**
```json
{
    "error": "Relation is not found."
}
```
**422 *Unprocessable Entity***
```json
{
    "error": "Invalid data. 'user_id' and 'room_id' are required"
}
```
**500 *Internal Server Error***
```json
{
    "error": "details"
}
```
</details>