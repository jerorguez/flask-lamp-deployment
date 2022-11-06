# Deployment of Flask-Python application on LAMP server (2022).

![Banner](.media/banner.png)

***Language***
* [🇪🇸 Español](README.es.MD)
* 🇺🇸 English

# Table of contents
* [Overview](#overview)
* [Lamp installation](#lamp-installation)
* [Configuration and Installation of the application](#configuration-and-installation-of-the-application)
* [Apache configuration](#apache-configuration)

# Overview
This guide is a compilation of all the necessary steps to deploy on a **LAMP** server an application written in **Flask-Python** from a clean installation based on **Ubuntu 22.x** . I'm going to assume that you are good with Linux based operating systems and their command lines, I'll also assume that you know and use a Python development environment.

---

# LAMP installation
The starting point of this guide is right after a clean install of Ubuntu 22.x . You can download the latest version of Ubuntu at this [link](https://ubuntu.com/download/desktop).

## Apache installation
Since we are going to deploy on an Apache server, we proceed to install it.

```bash
sudo apt install apache2

# Enable the firewall and give permissions to Apache
ufw enable
ufw allow in 'Apache'
```

Flask is a micro-framework for Python, but it is not a native web language. So getting our Python code to run on a web server is complicated. The mod_wsgi adapter is an Apache module that provides an interface compatible with WSGI (Web Server Gateway Interface), a standard interface between web server software and web applications written in Python, so we can host them inside Apache.

```bash
sudo apt install libapache2-mod-wsgi-py3

# Enable mod_wsgi
sudo a2enmod wsgi
```

## Database installation
Depending on the database you have preferred to use in your application, you can install [MySQL](#mysql-installation) or [MariaDB](#mariadb-installation);

### MySQL installation
```bash
sudo apt install mysql-server

# MySQ configuration
sudo mysql_secure_installation

# This option will guide you through a series of instructions by which 
# you will be able to make changes to the security settings.
```

***User creation***
```bash
sudo mysql

# Create the user of our application and assign a password to it
mysql> CREATE USER '[username]'@'localhost' IDENTIFIED WITH MYSQL_NATIVE_PASSWORD BY '[password]';

# Grant it the appropriate privileges. For example, with the following 
# command you could grant user privileges to all tables in the database.
mysql> GRANT ALL PRIVILEGES ON *.* TO '[username]'@'localhost' WITH GRANT OPTION;
```
---

### MariaDB installation
```bash
sudo apt install mariadb-server
```

***User creation***
```bash
sudo mariadb

# Create the user and grant it the appropriate privileges.
mariadb> GRANT ALL ON *.* TO '[username]'@'localhost' IDENTIFIED BY '[password]' WITH GRANT OPTION;
```

---

# Configuration and Installation of the application
To test you can use the application we have created [Flask-Python App](flask-todo).

The repository will be hosted in the folder **`/var/www/`**

If errors occur due to permissions when moving the repository to the destination folder, we can place it in any folder in the user's **`/home`** and move it with the following command:

```bash
sudo cp -r [app_path] /var/www
```

## Creation of the virtual environment in the project
Python3 comes by default installed on our Ubuntu system, but for the installation of software packages written in Python we need to install its package installer.

```bash
sudo apt install python3-pip
```

Once installed, we proceed to install globally the package `VirtualEnv`

```bash
sudo pip3 install virtualenv
```

***Creation of the virtual environment and installation of packages***

```bash
# Go to the project folder
cd /var/www/project

# Create the folder venv
sudo virtualenv venv

# Activate the virtual environment
source venv/bin/activate

# Proceed to install the packages contained in requirements.txt
(venv)> pip3 install -r requirements.txt
```

**Warning!** It is possible that when installing the dependencies, we get an error when installing the mysqlclient interface, to solve it we must execute the following command:

```bash
sudo apt install libmysqlclient-dev
```

**Note**: In this step we must ensure that the program is running by executing the launcher.

## WSGI configuration
The **`app.wsgi`** is the file that apache will read to launch the application in flask.

It is necessary to create it inside the **`/var/www/[project_name]`** folder and enter the following code.

**app.wsgi**
```python
#!/usr/bin/python

import sys

sys.path.insert(0, '/var/www/[project_name]/')
activate_this = '/var/www/[project_name]/venv/bin/activate_this.py'

with open(activate_this) as file:
    exec(file.read(), dict(__file__=activate_this))

# The instance that starts the Flask application is imported from the launcher.
from [launcher] import app as application
```

---

# Apache configuration
We are going to configure a new site for our application, for this we go to the folder **`/ect/apache2/sites-available/`** and create the configuration file.

**[name].conf**
```bash
ServerName [name].[domain]
<VirtualHost *:80>

    ServerAdmin webmaster@localhost.[domain]
    ServerAlias www.[name].[domain]
    DocumentRoot /var/www/[project_path]

    WSGIDaemonProcess [process_name] user=www-data group=www-data threads=5
    WSGIScriptAlias / /var/www/[project_path]/app.wsgi

    # Remember to have created the folders in which you want to save the logs.
    ErrorLog /var/www/[project_path]/error.log
    CustomLog /var/www/[project_path]/access.log combined

    <Directory /var/www/[project_path]>
        WSGIProcessGroup [process_name]
        WSGIApplicationGroup %{GLOBAL}
        Require all granted
    </Directory>

</VirtualHost>
```

Once the file is created, save it and enable the new site.
```bash
sudo a2ensite [name].conf

# Reset the Apache server for the changes to take effect
systemctl restart apache2
```

Now we only have to add the new domain to the file **`/etc/hosts/`***
```bash
[IP]            [ServerAlias]
127.0.0.1       www.example.son
```

**Note**: At this point, your application is already running in http://[ServerAlias].

---
Jerobel Rodriguez - [@jerorguez](https://github.com/jerorguez)