# Flask-Todo App

![Banner](../.media/flask-todo.png)

***Idioma***
* 🇪🇸 Español
* [🇺🇸 English](https://github.com/jerorguez/flask-lamp-deployment/tree/main/flask-todo)

# Resumen
Esta aplicación ha sido creada para el tutorial [Despliegue en servidor LAMP de aplicación en Flask-Python](https://github.com/jerorguez/flask-lamp-deployment). 

La aplicación consiste de una lista de tareas con conexión a base de datos mediante ORM.

# Requisitos de uso
Para el funcionamiento de la aplicación se han instalado los siguientes paquetes:
* Flask (micro-Framework Python)
* Flask-SQLAlchemy (ORM)
* MySQLClient (interfaz mysql para Python)

Todos los paquetes se encuentran en el archivo **`requirements.txt`**

![Requirements](../.media/requirements.png)

Es necesario la creación de un usuario y de una base de datos, para el correcto funcionamiento. La conexión a la misma será configurada en el archivo **`__init__.py`**.

**\_\_init\_\_.py**

![ORM configuration](../.media/orm-config.png)

---
Jerobel Rodriguez - [@jerorguez](https://github.com/jerorguez)
