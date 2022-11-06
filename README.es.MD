# Despliegue en servidor LAMP de aplicación en Flask-Python (2022).

![Banner](.media/banner.png)

***Idioma***
* 🇪🇸 Español
* [🇺🇸 English](https://github.com/jerorguez/flask-lamp-deployment)

# Índice
* [Resumen](#resumen)
* [Instalación LAMP](#instalación-lamp)
* [Configuración e Instalación de la aplicación](#configuración-e-instalación-de-la-aplicación)
* [Configuración Apache](#configuración-apache)

# Resumen
Esta guía es una recopilación de todos los pasos necesarios para desplegar en un servidor **LAMP** una aplicación escrita en **Flask-Python** a partir de una instalación limpia basada en **Ubuntu 22.x** . Voy a asumir que te manejas bien con sistemas operativos basados en Linux y sus líneas de comandos, asumiré también que conoces y usas un entorno de desarrollo Python.

---

# Instalación LAMP
El punto de partida de esta guía es justo tras una instalación limpia de Ubuntu 22.x . Puedes decargar la última versión de Ubuntu en este [enlace](https://ubuntu.com/download/desktop).

## Instalación de Apache
Dado que vamos a desplegar en un servidor Apache, procedemos a instalarlo.

```bash
sudo apt install apache2

# Habilitamos el firewall y le damos permisos a Apache
ufw enable
ufw allow in 'Apache'
```

Flask es un micro-framework para python, pero no es un lenguaje web nativo. Entonces hacer que nuestro código Python se ejecute en un servidor web es complicado. El adaptador mod_wsgi es un módulo de Apache que proporciona una interfaz compatible con WSGI (Web Server Gateway Interface), una interfaz estándar entre el software del servidor web y las aplicaciones web escritas en Python, de este modo podremos alojarlas dentro de Apache.

```bash
sudo apt install libapache2-mod-wsgi-py3

# Habilitamos el mod_wsgi
sudo a2enmod wsgi
```

## Inslación de la Base de Datos
Dependiendo de la base de datos que hayas preferido usar en tu aplicación, puedes instalar [MySQL](#instalación-de-mysql) o [MariaDB](#instalación-de-mariadb);

### Instalación de MySQL
```bash
sudo apt install mysql-server

# Configuración MySQL
sudo mysql_secure_installation

# Esta opción te guiará a través de una serie de instrucciones mediante las cuales
# podrás realizar cambios en las opciones de seguridad.
```

***Configuramos un usuario***
```bash
sudo mysql

# Creamos el usuario de nuestra aplicación y le asignamos una contraseña
mysql> CREATE USER '[username]'@'localhost' IDENTIFIED WITH MYSQL_NATIVE_PASSWORD BY '[password]';

# Le otorgamos los privilegios apropiados. Por ejemplo, con el siguiente comando
# podría conceder privilegios de usuario a todas las tablas de la base de datos.
mysql> GRANT ALL PRIVILEGES ON *.* TO '[username]'@'localhost' WITH GRANT OPTION;
```

---

### Instalación de MariaDB
```bash
sudo apt install mariadb-server
```

***Configuramos un usuario***
```bash
sudo mariadb

# Creamos el usuario y le otorgamos los privilegios apropiados.
mariadb> GRANT ALL ON *.* TO '[username]'@'localhost' IDENTIFIED BY '[password]' WITH GRANT OPTION;
```

---

# Configuración e Instalación de la aplicación
Para hacer pruebas puedes usar la aplicación que hemos creado [Flask-Python App](flask-todo).

El repositorio irá alojado en la carpeta **`/var/www/`**

Si se producen errores debido a permisos a la hora de mover el repositorio a la carpeta destino, podemos alojarlo en cualquier carpeta del **`/home`** del usuario y moverlo con el siguiente comando:

```bash
sudo cp -r [app_path] /var/www
```

## Creación del entorno virtual en el proyecto
Python3 viene por defecto instalado en nuestro sistema Ubuntu, pero para la instalación de paquetes de software escritos en Python necesitamos instalar su instalador de paquetes.

```bash
sudo apt install python3-pip
```

Una vez instalado, procedemos a instalar de forma global el paquete `VirtualEnv`

```bash
sudo pip3 install virtualenv
```

***Creación del entorno virtual e instalación de los paquetes***

```bash
# Nos dirigimos a la carpeta del proyecto
cd /var/www/project

# Creamos la carpeta venv
sudo virtualenv venv

# Activamos el entorno virtual
source venv/bin/activate

# Procedemos a instalar los paquetes contenidos en requirements.txt
(venv)> pip3 install -r requirements.txt
```

**Warning**: Es posible que al instalar las dependencias, nos de un error al instalar la interfaz de mysqlclient, para solucionarlo deberemos ejecutar el siguiente comando:

```bash
sudo apt install libmysqlclient-dev
```

**Nota**: En este paso deberemos asegurar que el programa funciona ejecutando el lanzador.

## Configuración WSGI
El **`app.wsgi`** es el fichero que va a leer apache para lanzar la aplicacion en flask.

Es necesario crearlo dentro de la carpeta **`/var/www/[project_name]`** e introducir el siguiente código.

**app.wsgi**
```python
#!/usr/bin/python

import sys

sys.path.insert(0, '/var/www/[project_name]/')
activate_this = '/var/www/[project_name]/venv/bin/activate_this.py'

with open(activate_this) as file:
    exec(file.read(), dict(__file__=activate_this))

# Del lanzador se importa la instancia que inicia la applicacion Flask
from [lanzador] import app as application
```

---

# Configuración Apache
Vamos a configurar un nuevo site para nuestra aplicación, para ello nos dirigimos a la carpeta **`/ect/apache2/sites-available/`** y creamos el archivo de configuración.

**[name].conf**
```bash
ServerName [name].[domain]
<VirtualHost *:80>

    ServerAdmin webmaster@localhost.[domain]
    ServerAlias www.[name].[domain]
    DocumentRoot /var/www/[project_path]

    WSGIDaemonProcess [process_name] user=www-data group=www-data threads=5
    WSGIScriptAlias / /var/www/[project_path]/app.wsgi

    # Recordar tener creadas las carpetas en las que queramos guardar los logs
    ErrorLog /var/www/[project_path]/error.log
    CustomLog /var/www/[project_path]/access.log combined

    <Directory /var/www/[project_path]>
        WSGIProcessGroup [process_name]
        WSGIApplicationGroup %{GLOBAL}
        Require all granted
    </Directory>

</VirtualHost>
```

Una vez creado el archivo, lo guardamos y habilitamos el nuevo site.
```bash
sudo a2ensite [name].conf

# Reiniciamos el servidor Apache para que surjan efectos los cambios
systemctl restart apache2
```

Ahora solo tendremos que añadir el nuevo dominio al archivo **`/etc/hosts/`***
```bash
[IP]            [ServerAlias]
127.0.0.1       www.example.son
```

**Nota**: Llegamos a este punto ya su aplicación esta corriendo en http://[ServerAlias].

---
Jerobel Rodriguez - [@jerorguez](https://github.com/jerorguez)
