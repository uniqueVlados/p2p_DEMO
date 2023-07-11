# API

## Users

## Заголовки
Для всех запросов:
```
Content-Type: application/json
```
Дополнительно для запросов с авторизацией:
```
Authorization: Token <token>
```
где `<token>` - токен авторизации, выдаваемый при регистрации.

Дополнительно для запросов от партнёра:
```
Secretkey: <secret_key>
```
где `<secret_key>` - секретный ключ, выдаваемый при регистрации.


### Создать пользователя

**POST** `api/users/user/create/`
```json
{
    "email": "btp442-4@mail.ru",
    "password": "ksjdjklkkUUgh"
}
```
**Ответ**
```json
{
    "success": true,
    "token": "3060ceb29905cebc675cd0eb90b93e5a0c8f88eb"
}
```
После создания пользователя его регистрацию необходимо подтвердить в админке Джанго (`confirmed=True`).

### Авторизация
**POST** `api/users/token-auth/`
```json
{
    "email": "btp442-4@mail.ru",
    "password": "ksjdjklkkUUgh"
}
```

**Ответ**
```json
{
    "success": true,
    "token": "7129892431b8dafe942714bb54ee62749a7e78e7",
    "user_id": 2
}
```

### Сменить пароль

**GET** `api/users/user/reset-password/`

**Ответ**
```json
{
    "success": true
}
```
Новый пароль высылается на email пользователя, указанный при регистрации.

В среде тестирования в ответе может возвращаться
```json
{
    "success": true,
    "password": "<новый пароль>"
}
```

### Секретный ключ

Список ключей пользователя

**GET** `/api/users/keys/`

Получить ключ по id

**GET** `api/users/key/get/<id>/`

Редактировать ключ

**PATCH** `api/users/key/update/<id>/`
```json
{
    "name": "Test API updated",
    "is_available": false
}
```

Создать ключ

**POST** `api/users/key/create/`
```json
{
    "name": "Test API"
}
```

Удалить ключ по id

**DELETE** `api/users/key/delete/<id>/`


## Переводы

### Пополнение

**POST** `api/finances/replenish/`
```json
{
    "amount": 500
}
```
**Ответ**
```json
{
    "status": "new",
    "uid": "fa1a7eab-38f2-4716-912a-d999878b2663"
}
```

### Списание

**POST** `api/finances/withdraw/`
```json
{
    "amount": 600,
     "card_number": 1234123412349876
}
```
**Ответ**
```json
{
    "status": "new",
    "uid": "eb8761af-edec-4858-aeea-86fcab997469"
}
```


### Статус платежного поручения

**POST** `api/finances/get-payment-status/`
```json
{
     "uid": "ae5c2ee7-31cb-4f22-baaf-64551a05a313"
}
```
**Ответ**
```json
{
    "status": "approved"
}
```


### Баланс счёта партнёра

**GET** `api/finances/get-balance/`

**Ответ**
```json
{
    "balance": 2112.0
}
```

### Список платежных поручений

**GET** `api/finances/get-payrolls/`

**Ответ**
```json
[
{
"uid": "ae5c2ee7-31cb-4f22-baaf-64551a05a313",
"amount": "600.00",
"payment_type": "replenishment",
"status": "approved"
},
{
"uid": "dd4ef3c4-8b53-4e88-aa8f-015beedbe5eb",
"amount": "800.00",
"payment_type": "replenishment",
"status": "approved"
},
{
"uid": "26c2c7f1-34ef-4fc4-a281-358dc140df2d",
"amount": "1000.00",
"payment_type": "replenishment",
"status": "failed"
},
{
"uid": "144ed652-3242-42bc-a595-fb07ac48ab5d",
"amount": "500.00",
"payment_type": "replenishment",
"status": "rejected"
},
{
"uid": "8320593b-2c92-40d6-81b4-d79a5bd71f12",
"amount": "550.00",
"payment_type": "replenishment",
"status": "approved"
},
{
"uid": "416f8b9b-90e0-4bb2-9ed8-f87bb2844db2",
"amount": "600.00",
"payment_type": "withdrawl",
"status": "approved"
}
]
```


### Статистика по дням за период

**GET** `api/finances/get-days-amounts/?date_from=22.10.2022&date_until=24.10.2022`

**Ответ**
```json
{
    "per_days":{
        "2022.10.24":{
            "replenishment":{
                "approved": 1950.0,
                "failed": 1000.0
            },
            "withdrawl":{
                "approved": 600.0,
                "failed": null
                }
        },
        "2022.10.23":{
            "replenishment":{
                "approved": 1950.0,
                "failed": 1000.0
                },
            "withdrawl":{
                "approved": 600.0,
                "failed": null
                }
        },
        "2022.10.22":{
            "replenishment":{
                "approved": null,
                "failed": null
                 },
            "withdrawl":{
                "approved": null,
                "failed": null
                }
            }
        },
"for_period":{
    "replenishment":{
        "approved": 1950.0,
        "failed": 1000.0
         },
    "withdrawl":{
        "approved": 600.0,
        "failed": null
        }
    }
}

```



### Получить секретный ключ (ТОЛЬКО в режиме разработки)

**GET** `/api/users/get-key/`

**Ответ**
```json
{
    "secret_key": "l>?7R7uswqX|wEzg_*~QIi7+%^N|Oh}gqV#{$H=0)5D0;5O,Tlro;c*v,+gADm.1(oe,2HD,REXc<=x*a1^QtX/tF_eqy[wCtoE=j#neS{?{YiZX.|eK;b/NY4?V?1B/"
}
```



