# gmail-autotests
Для запуска тестов в контейнере необходимо: 
 1. Скачать файл docker-compose.yml(лежит в корне репозитория)
 2. Перейти в директорию с скаченным файлом docker-compose.yml
  a. Если порт 8181 занят можно отредактировать docker-compose.yml и отредактировать значение ports(http://joxi.ru/KAxxV9DH1QdNyA)
 3. В терминале выполнить команду 'docker-compose up'
 4. Когда allure сгенерирует отчет перейти по ссылке, которая будет отображена в терминале: http://joxi.ru/krDJ8DWCJ6Q8b2
  a. Если по ссылке отчет не открывается, то необходимо перейти по ссылке: http://localhost:8181/ (порт 8181 стоит по умолчанию если ранее порт был изменен то необходимо выбрать свой порт например http://localhost:9999/)
 5. Если закрыть allure с помощью Ctrl+C, то контейнер остановится
