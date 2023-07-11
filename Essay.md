# Документация

[Административная панель](http://keeper-p2p.teegra.io/admin/)

Логин: admin@admin.ru Пароль: admin

Данные для входа других пользователей см. в [Сценарии тестирования](https://github.com/Capstane/antarex-copy-api/blob/dev/Testing.md)

[Репозиторий](https://github.com/Capstane/antarex-copy-api) (ветка dev)

[Swagger](http://keeper-p2p.teegra.io/swagger-ui/#)

[API](https://github.com/Capstane/antarex-copy-api/blob/dev/API.md) - основые эндпойнты, запросы/ответы

# Сценарий тестирования сервиса

[Тестирование сервиса](https://github.com/Capstane/antarex-copy-api/blob/dev/Testing.md)

# Flow

1. Оператор подключается к административной панели (админка);
2. Партнёрский сервис отправляет (предварительный) запрос на пополнение/списание с указанием суммы на бэк;
3. Бэк проверяет баланс партнёра (если списание), создает платежное поручение (ПП) со статусом new и в ответ отправляет ссылку на страницу с формой. В адресе страницы указан uid ПП в качестве query-параметра. В теле ответа указывается uid платежа, сумма и, в случае списания, номер карты, на которую производить пополнение;
4. Пользователь партнёрского сервиса (ППС) переходит по ссылке на форму оплаты (страницы макета payment.html);
5. Фронт выводит сумму и номер карты (если пополнение) или форму для ввода номера карты (если списание).
6. ППС нажимает ```Я оплатил``` (если пополнение) или вводит номер своей карты и нажимает ```Ок``` (если списание). Фронт направляет на бэк запрос на проведение транзакции. В запросе указывается uid ПП и, если списание, номер карты ППС. После этого фронт переходит на страницу с таймером и периодически опрашивает бэк на статус ПП (будет переделываться под веб-сокет);
7. На бэке по запросу в ПП устанавливается статус processing и записывается номер карты (если списание). По сигналу post_save при таком статусе у оператора появляется сообщение о необходимости обработать ПП (сделано через веб-сокеты, см. django-eventstream).
8. Оператор проверяет платеж и устанавливает статус Одобрен (approved) или Не прошёл/Отклонён (failed/rejected);
9. По сигналу post_save при статусе approved обновляется баланс партнёра, зачисляются комиссионные на системный счёт, атрибут performed ПП устанавливается в True.
При статусе failed/rejected атрибут performed ПП устанавливается в True.
10. Фронт получает статус и выводит соответствующее сообщение - успех/неуспех.

# Прочие процессы

- Авторизация;
- Смена пароля;
- Генерирование дополнительных секретных ключей;
- Цифровая подпись: функционал сделан, но на стадии разработки не подключен. Код для шифрования HMAC создается при создании пользователя-партнёра;
- Мониторинг банковских карт - текущих оборотов, сроков действия, каникул для карт: сделан на базе celery-beat, не протестирован.
- Раздел документации: тексты частично подготовлены, но не внесены.

# Структура проекта

```
.
├── backlog
├── btasks (фоновые задачи celery)
├── core (middlewares, по flow ничего)
├── encryption (шифрование hmac, сейчас не подключено)
├── finances (вся бизнес логика здесь)
├── logs (логи)
├── notifications (веб-пуши, не подключены)
├── project (настройки)
├── role_permissions (роли пользователей)
├── templates
├── users (пользователи и действия: авторизация, секр. ключи)
└── utils (общие утилиты)
```