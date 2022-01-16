# Таблица для всех ресусов ФО
create table domain_fin (orgName VARCHAR(200), regNumber INT, domen VARCHAR(200))

# Таблица для статистики по пингу ресурсов ФО
create table ping_status (orgName VARCHAR(200), domen VARCHAR(200), ping int1)

# Запрос для сервиса детекта сообщений пользователей
select * from domain_fin where orgName like '%Сбербанк%'