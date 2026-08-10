### Hexlet tests and linter status:
[![Actions Status](https://github.com/aigul-b/middle-python-project-83/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/aigul-b/middle-python-project-83/actions)
[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=aigul-b_middle-python-project-83&metric=coverage)](https://sonarcloud.io/summary/new_code?id=aigul-b_middle-python-project-83)


«Анализатор страниц» — это веб-приложение, написанное на Python с использованием фреймворка Flask. Он анализирует указанные страницы на SEO-пригодность. Пользователь добавляет адреса сайтов, запускает проверку и видит её результаты, сохранённые в базе данных.

Данное приложение не требует предварительной установки. 

Использование:
- Перейдите на https://hexlet-homework.onrender.com/ — это стартовая страница с формой «Добавить сайт».
- В поле ввода впишите полный URL с протоколом, например https://www.google.com.
- Сервис добавит сайт в базу и сразу выполнит его проверку: получит статус-код ответа, а также заголовок и описание главной страницы.
- Перейдите в раздел «Сайты» (https://hexlet-homework.onrender.com/urls), чтобы увидеть все добавленные адреса и статус их последней проверки.
- На странице сайта есть кнопка запуска новой проверки — она полезна, если содержимое страницы изменилось и нужно обновить данные.

