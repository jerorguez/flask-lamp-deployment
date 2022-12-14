# Despliegue en servidor LAMP de aplicaci贸n en Flask-Python (2022).

![Banner](.media/banner.png)

***Idioma***
* 馃嚜馃嚫 Espa帽ol
* [馃嚭馃嚫 English](https://github.com/jerorguez/flask-lamp-deployment)

# 脥ndice
* [Resumen](#resumen)
* [Instalaci贸n LAMP](#instalaci贸n-lamp)
* [Configuraci贸n e Instalaci贸n de la aplicaci贸n](#configuraci贸n-e-instalaci贸n-de-la-aplicaci贸n)
* [Configuraci贸n Apache](#configuraci贸n-apache)

# Resumen
Esta gu铆a es una recopilaci贸n de todos los pasos necesarios para desplegar en un servidor **LAMP** una aplicaci贸n escrita en **Flask-Python** a partir de una instalaci贸n limpia basada en **Ubuntu 22.x** . Voy a asumir que te manejas bien con sistemas operativos basados en Linux y sus l铆neas de comandos, asumir茅 tambi茅n que conoces y usas un entorno de desarrollo Python.

---

# Instalaci贸n LAMP
El punto de partida de esta gu铆a es justo tras una instalaci贸n limpia de Ubuntu 22.x . Puedes decargar la 煤ltima versi贸n de Ubuntu en este [enlace](https://ubuntu.com/download/desktop).

## Instalaci贸n de Apache
Dado que vamos a desplegar en un servidor Apache, procedemos a instalarlo.

```bash
sudo apt install apache2

# Habilitamos el firewall y le damos permisos a Apache
ufw enable
ufw allow in 'Apache'
```

Flask es un micro-framework para python, pero no es un lenguaje web nativo. Entonces hacer que nuestro c贸digo Python se ejecute en un servidor web es complicado. El adaptador mod_wsgi es un m贸dulo de Apache que proporciona una interfaz compatible con WSGI (Web Server Gateway Interface), una interfaz est谩ndar entre el software del servidor web y las aplicaciones web escritas en Python, de este modo podremos alojarlas dentro de Apache.

```bash
sudo apt install libapache2-mod-wsgi-py3

# Habilitamos el mod_wsgi
sudo a2enmod wsgi
```

## Inslaci贸n de la Base de Datos
Dependiendo de la base de datos que hayas preferido usar en tu aplicaci贸n, puedes instalar [MySQL](#instalaci贸n-de-mysql) o [MariaDB](#instalaci贸n-de-mariadb);

### Instalaci贸n de MySQL
```bash
sudo apt install mysql-server

# Configuraci贸n MySQL
sudo mysql_secure_installation

# Esta opci贸n te guiar谩 a trav茅s de una serie de instrucciones mediante las cuales
# podr谩s realizar cambios en las opciones de seguridad.
```

***Configuramos un usuario***
```bash
sudo mysql

# Creamos el usuario de nuestra aplicaci贸n y le asignamos una contrase帽a
mysql> CREATE USER '[username]'@'localhost' IDENTIFIED WITH MYSQL_NATIVE_PASSWORD BY '[password]';

# Le otorgamos los privilegios apropiados. Por ejemplo, con el siguiente comando
# podr铆a conceder privilegios de usuario a todas las tablas de la base de datos.
mysql> GRANT ALL PRIVILEGES ON *.* TO '[username]'@'localhost' WITH GRANT OPTION;
```

---

### Instalaci贸n de MariaDB
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

# Configuraci贸n e Instalaci贸n de la aplicaci贸n
Para hacer pruebas puedes usar la aplicaci贸n que hemos creado [Flask-Python App](flask-todo).

El repositorio ir谩 alojado en la carpeta **`/var/www/`**

Si se producen errores debido a permisos a la hora de mover el repositorio a la carpeta destino, podemos alojarlo en cualquier carpeta del **`/home`** del usuario y moverlo con el siguiente comando:

```bash
sudo cp -r [app_path] /var/www
```

## Creaci贸n del entorno virtual en el proyecto
Python3 viene por defecto instalado en nuestro sistema Ubuntu, pero para la instalaci贸n de paquetes de software escritos en Python necesitamos instalar su instalador de paquetes.

```bash
sudo apt install python3-pip
```

Una vez instalado, procedemos a instalar de forma global el paquete `VirtualEnv`

```bash
sudo pip3 install virtualenv
```

***Creaci贸n del entorno virtual e instalaci贸n de los paquetes***

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

## Configuraci贸n WSGI
El **`app.wsgi`** es el fichero que va a leer apache para lanzar la aplicacion en flask.

Es necesario crearlo dentro de la carpeta **`/var/www/[project_name]`** e introducir el siguiente c贸digo.

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

# Configuraci贸n Apache
Vamos a configurar un nuevo site para nuestra aplicaci贸n, para ello nos dirigimos a la carpeta **`/ect/apache2/sites-available/`** y creamos el archivo de configuraci贸n.

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

Ahora solo tendremos que a帽adir el nuevo dominio al archivo **`/etc/hosts/`***
```bash
[IP]            [ServerAlias]
127.0.0.1       www.example.son
```

**Nota**: Llegamos a este punto ya su aplicaci贸n esta corriendo en http://[ServerAlias].

---
Jerobel Rodriguez - [@jerorguez](https://github.com/jerorguez)
