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
```
{
    "username": "user001",
    "password": "StrongPassword321!",
    "email": "user001@fakemail.com"
}
```
**Відповіді:**
**201 *Created***
```
{
    "message": "User created successfully.",
    "user_id": 1
}
```
**422 *Unprocessable Entity***
```
{
    "error": "Invalid data. 'username', 'email' and 'password' are required."
}
```
**409 *Conflict***
```
{
    "error": "User already exists. 'username' and 'email' must be unique".
}
```
**500 *Internal Server Error***
```
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
```
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
```
{
    "error": "details"
}
```
</details>

<details>

<summary>

**Отримання користувача за id**

</summary>



</details>