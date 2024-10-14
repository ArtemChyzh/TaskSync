# TaskSync API Документація
## Огляд
**TaskSync** - це система управління завданнями з підтримкою багатьох користувачів та спільних списків завдань (кімнат). Ця документація призначена для сторонній розробників і містить інформацію про публічне api проекту.

## Базовий URL
Усі запити слід надсилати на API Gateway:
[http://localhost:5000/api](http://localhost:5000/api)

## Ендпоїнти
### Користувачі
<details>
<summary>

**Реєстрація користувача**

</summary>

- **URL:** `api/users`
- **Метод**: ==POST==
- **Опис**: Створює нового користувача
**Параметри запиту**
```json
{
    "username": "user001",
    "password": "StrongPassword321!",
    "email": "user001@fakemail.com"
}
```
**Відповіді:**
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

**Отримання всіх користувачів**

</summary>

- **URL:** `api/users`
- **Метод**: ==GET==
- **Опис**: Отримує список всіх користувачів

**Відповіді:**
**200 *OK***
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
**500 *Internal Server Error***
```json
{
    "error": "details"
}
```
</details>

<details>
<summary>

**Отримання користувача**

</summary>

- **URL:** `api/users/{user_id}`
- **Метод**: ==GET==
- **Опис**: Отримання користувача за id

- **URL:** `api/user/{username}`
- **Метод**: ==GET==
- **Опис**: Отримання користувача за username

**Відповіді:**
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

**Редагування користувачів** 

</summary>

- **URL:** `api/users/{user_id}`
- **Метод**: ==PUT==
- **Опис**: Отримання користувача за id
**Параметри запиту (мінімум один)**
```json
{
    "username": "user002",
    "email": "new@fakemail.com",
    "password": "NewPass"
}
```

**Відповіді**
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

**Видалення користувача** 

</summary>

- **URL:** `api/users/{user_id}`
- **Метод**: ==DELETE==
- **Опис**: Видалення користувача за id

**Відповіді**
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

**Отримання кімнат користувача**

</summary>

- **URL:** `api/users/{user_id}/rooms`
- **Метод**: ==GET==
- **Опис**: Отримання всіх кімнат, в які входить користувач

**Відповіді**
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

**Отримання завдань користувача**

</summary>

- **URL:** `api/users/{user_id}/rooms`
- **Метод**: ==GET==
- **Опис**: Отримання всіх завдань, які створив користувач

**Відповіді**
**200 *OK***
```json
[
    {
        "task_id": 1,
        "title": "Купити корову",
        "user_id": 1,
        "room_id": 6,
        "deadline": "01-04-2024",
        "status": 2
    },
    {
        "task_id": 125,
        "title": "Створити ферму",
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

### Завдання
<details>
<summary>

**Створення завдання**

</summary>

- **URL:** `/api/tasks`
- **Метод:** ==POST==
- **Опис:** Публікація нового завдання
**Параметри запиту**
```json
{
    "title": "Default",
    "user_id": 1,
    "room_id": 1,
    "deadline": "2024-04-01T00:00:00Z",
    "status": 3 
}
```

**Відповіді**
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

**Отримання всіх завдань**

</summary>

- **URL:** `/api/tasks`
- **Методи:** ==GET==
- **Опис:** Отримує список всіх завдань

**Відповіді**
**200 *OK***
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
    "room_id": 3,
    "deadline": "2024-10-22T16:30:00Z",
    "status": "in_progress"
  },
  {
    "id": 3,
    "title": "Design new homepage layout",
    "description": "Work on the redesign of the main website page to improve user experience and increase conversion rates.",
    "user_id": 3,
    "room_id": 2,
    "deadline": "2024-10-25T08:00:00Z",
    "status": "pending"
  },
  {
    "id": 4,
    "title": "Optimize database queries",
    "description": "Refactor database queries in the tasks service to improve performance for larger datasets.",
    "user_id": 1,
    "room_id": 4,
    "deadline": "2024-10-23T12:00:00Z",
    "status": "completed"
  },
  {
    "id": 5,
    "title": "Prepare user feedback report",
    "description": "Analyze feedback from beta testers and compile a report on their suggestions and concerns.",
    "user_id": 5,
    "room_id": 2,
    "deadline": "2024-10-28T14:45:00Z",
    "status": "pending"
  }
]
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

**Отримання конкретного завдання за ID**

</summary>

- **URL:** `/api/tasks/{task_id}`
- **Методи:** ==GET==
- **Опис:** Отримує конкретне завдання за його ID.

**Відповіді**
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

**Редагування конкретного завдання за ID**

</summary>

- **URL:** `/api/tasks/{task_id}`
- **Методи:** ==PUT==
- **Опис:** Оновлює існуюче завдання за його ID.

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

**Відповіді**
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

**Видалення конкретного завдання за ID**

</summary>

- **URL:** `/api/tasks/{task_id}`
- **Методи:** ==DELETE==
- **Опис:** Видаляє існуюче завдання за його ID.

**Відповіді**
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

### Кімнати
<details>
<summary>

**Створення кімнати**

</summary>

- **URL:** `/api/rooms`
- **Метод:** ==POST==
- **Опис:** Створення нової кімнати, в яку автоматично додається користувач, що її створив (завдання не можуть існувати, не належачи до жодної кімнати)
**Параметри запиту**
```json
{
    "user_id": 1,
    "code": "0000",
    "title": "Default Room",
    "description": "AAAAAAAAAAAAAAAAAAAA я дуже втомився"
}
```

**Відповіді**
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

**Отримання кімнат**

</summary>

- **URL:** `/api/rooms`
- **Метод:** ==GET==
- **Опис:** Список всіх кімнат, що існують

**Відповіді**
**200 *ОК***
```json
[
  {
    "id": 1,
    "user_id": 2,
    "code": "ABC123",
    "title": "Project Planning",
    "description": "Room for project planning and task coordination."
  },
  {
    "id": 2,
    "user_id": 3,
    "code": "XYZ456",
    "title": "Design Team",
    "description": "Room for the design team to share ideas and collaborate."
  },
  {
    "id": 3,
    "user_id": 4,
    "code": "LMN789",
    "title": "Development Room",
    "description": "Room for developers to discuss progress and technical challenges."
  }
]
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

**Отримання конкретної кімнати (шифр)**

</summary>

- **URL:** `/api/rooms/{code}`
- **Метод:** ==GET==
- **Опис:** Отримання кімнати за її індивідуальним шифром

**Відповіді**
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

**Отримання конкретної кімнати (номер)**

</summary>

- **URL:** `/api/rooms/{room_id}`
- **Метод:** ==GET==
- **Опис:** Отримання кімнати за її id

**Відповіді**
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

**Видалення кімнати**

</summary>

- **URL:** `/api/rooms/{room_id}`
- **Метод:** ==DELETE==
- **Опис:** Видалення кімнати за її id

**Відповіді**
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

**Отримання користувачів в кімнаті**

</summary>

- **URL:** `/api/rooms/{room_id}/users`
- **Метод:** ==GET==
- **Опис:** Список всіх користувачів, що прикріплені до конкретної кімнати.

**Відповіді**
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
**Примітка:** *Якщо ви отримали цю помилку перевірте наявність кімнати за її номером. Якщо кімната існує, але ви все ж отримали помилку - це може означати, що кімната не була видалена після видалення всіх користувачів, що може призвести до значних витоків пам'яті.*

**500 *Internal Server Error***
```json
{
    "error": "details"
}
```
</details>

<details>
<summary>

**Отримання завдань кімнати**

</summary>

- **URL:** `/api/rooms/{room_id}/tasks`
- **Метод:** ==GET==
- **Опис:** Список всіх завдань всередині кімнати.

**Відповіді**
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

**Доєднання користувача до кімнати**

</summary>

- **URL:** `/api/rooms/join`
- **Метод:** ==POST==
- **Опис:** Прикріплює певного користувача до певної кімнати.
**Параметри запиту**
```json
{
    "user_id": 1,
    "room_id": 1
}
```

**Відповіді**
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

**Від'єднання користувача від кімнати**

</summary>

- **URL:** `/api/rooms/remove`
- **Методи:** ==DELETE==
- **Опис:** Від'єднує конкретного користувача від конкретної кімнати
**Параметри запиту**
```json
{
    "user_id": 1,
    "room_id": 1
}
```

**Відповіді**
**200 *OK***
```json
{
    "message": "User removed from room successfully."
}
```
**204 *No Content***
**Примітка:** *Користувача від'єднано, а кімнату видалено, оскільки в ній не лишилось користувачів*
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