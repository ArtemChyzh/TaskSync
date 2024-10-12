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
**201 *No Content***
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