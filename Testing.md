# Документация

Административная панель http://keeper-p2p.teegra.io/admin/

Swagger http://keeper-p2p.teegra.io/admin/swagger-ui/#

https://github.com/Capstane/antarex-copy-api/blob/dev/API.md - основые эндпойнты, запросы/ответы

# Сценарий тестирования сервиса

Потребуется окно браузера и что-то вроде Postman, например, сам постман).

## Создание пользователей

Пользователи создаются в административной панели, раздел Пользователи -> Добавить пользователя, прямая ссылка http://keeper-p2p.teegra.io/admin/users/user/add/

Суперпользователь создает Администраторов.
Администраторы создают Операторов и Партнёров.

### Суперпользователь

Логин: admin@admin.ru
Пароль: admin

### Администратор
- Указать реальный email
- ФИО - по желанию
- Выбрать Роль пользователя - Администратор
- Поставить галочку Статус персонала
- Поставить галочку Подтверждён
- Нажать Сохранить

На указанную почту придет пароль.

Для теста:
```
administrator@687687.ru
hoC2uQS1Q2Q2
```

### Оператор
- Указать реальный email
- ФИО - по желанию
- Выбрать Роль пользователя - Оператор
- Поставить галочку Статус персонала
- Поставить галочку Подтверждён
- Нажать Сохранить

На указанную почту придет пароль.

Для теста:
```
operator@687687.ru
qwerty
```

### Партнёр
- Указать реальный email
- ФИО - по желанию
- Выбрать Роль пользователя - Партнёр
- галочку Статус персонала НЕ СТАВИТЬ!
- Поставить галочку Подтверждён
- Нажать Сохранить

На указанную почту придет пароль.

Для теста:
```
partner@687687.ru
qwerty
```

## Авторизация

Окно браузера. Оператор авторизуется через форму на http://keeper-p2p.teegra.io/admin/ .

Постман. Описание запросов см. в https://github.com/Capstane/antarex-copy-api/blob/dev/API.md

- Партнёр авторизуется запросом в систему, в ответ получает токен авторизации;
- Партнер направляет запрос в систему на получение секретного ключа, используя токен авторизации. В ответ получает секретный ключ;
(ВНИМАНИЕ! Этот пункт действует толькое в процессе разработки, в проде партнер будет получать секретный ключ в ЛК);

## Пополнение/списание

Постман. Описание запросов см. в API.md

- Партнер направляет запрос на пополнение/списание;
- проверяет статус платежного поручения;
- после подтверждения успешного статуса проверяет баланс.

Окно браузера http://keeper-p2p.teegra.io/admin/finances/payroll/

- Если данный оператор выбран системой, то в окне браузера появляется индикатор о поступившем запросе на пополнение/списание;
- Оператор обновляет страницу (клик на иконку или Ctrl-R);
- Нажимает на ссылку платежного поручения (uid) и переходит в форму редактирования;
- проверяет поступление/осуществляет операцию списания с помощью сторонных программных средств;
- выбирает статус платежного поручения ```одобрен``` или ```не прошёл``` в зависимости от результата и нажимает Сохранить;
