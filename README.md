# funbox_test

[![Python](https://img.shields.io/badge/-Python-464646?style=flat-square&logo=Python)](https://www.python.org/)
[![Django](https://img.shields.io/badge/-Django-464646?style=flat-square&logo=Django)](https://www.djangoproject.com/)
[![Django REST Framework](https://img.shields.io/badge/-Django%20REST%20Framework-464646?style=flat-square&logo=Django%20REST%20Framework)](https://www.django-rest-framework.org/)
![Redis](https://img.shields.io/badge/redis-%23DD0031.svg?style=for-the-badge&logo=redis&logoColor=white)

Приложение выполняет не много не мало две функции:
 - при POST запросе на адрес 'api/visited_links' принимает массив URL адресов, выделяет из них домен и сохраняет в Redis в паре (key, value) где key - время запроса в Unix, value - строка с уникальными доменами
 - при GET запросе на адрес 'api/visited_domains?from=1545217638&to=1545217638' отдает уникальные домены в диапазоне from - to
#### Пример POST запроса:
{<br/>
      &#8195;"links": [<br/>
     &#8195;&#8195; "https://ya.ru",<br/>
     &#8195;&#8195; "https://ya.ru?q=123",<br/>
     &#8195;&#8195; "funbox.ru",<br/>
     &#8195;&#8195; "https://stackoverflow.com/questions/11828270/how-to-exit-the-vim-editor"<br/>
      &#8195;]<br/>
}&#8195;<br/>

#### Пример GET запроса:
{<br/>
      &#8195;"domains": [<br/>
     &#8195;&#8195; "ya.ru",<br/>
     &#8195;&#8195; "funbox.ru",<br/>
     &#8195;&#8195; "stackoverflow.com"<br/>
      &#8195;]<br/>
 &#8195;"status": "ok"<br/>
}&#8195;
## Подготовка и запуск проекта
### У вас должен быть запущен сервер Redis!
### Склонировать репозиторий на локальную машину:
```
git clone git@github.com:Komappp/funbox_test.git
```
### Перейдите в директорию funbox_test и:
 - установите виртуальное окружение
```
python3 -m venv venv
```
 - активация в Linux и MacOS
```
source venv/bin/activate 
```
 - активация в Windows
```
venv\Scripts\activate.bat
```
 - установите библиотеки
```
pip install -r requirements
```
 - запустите
```
cd backend/&&python manage.py runserver
```
