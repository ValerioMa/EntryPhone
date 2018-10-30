# Setup uWSGI and Nginx on Raspbian 4.14

For a more detailed description go [here](https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-uwsgi-and-nginx-on-ubuntu-16-04).

###### Get Python 3 and nginx:
Install the following pakages using apt:
```console
$ sudo apt-get update
$ sudo apt-get install python3-pip python3-dev python3-vev nginx
```

###### Create a Python Virtual Environment
Create a virtual python3 environment in the virtual_env folder
```console
$ PROJECT_ROOT=your_project_root_point
$ PYTHON_ENV_PATH=${PROJECT_ROOT}/virtual_env
$ python3 -m venv ${PYTHON_ENV_PATH}
$ source ${PYTHON_ENV_PATH}/bin/activate # activate the python environment
$ deactivate #deactivate the python environment
```

###### Install Flask and uWSGI
```console
(virtual_env) $ pip3 install uwsgi flask
```

###### Simple run of flask_server.py
To test the Flask app is needed to open the port 5000 before running the flask_server.py script:
```console
(virtual_env) $ sudo ufw allow 5000    #open up port 5000
(virtual_env) python3 flask_server.py
```
Visit 127.0.0.1:5000 in your web browser to see the served web pages.
After close the port:
```console
sudo ufw delete allow 5000
```

###### WSGI Entry Point
The file *${PROJECT_ROOT}/WebApp/wsgi.py* is the entry point file which tell uWSGI server how to interact with the application.

###### uWSGI Testing
Basic way to serve the application through uWSGI.
```console
(virtual_env) $ uwsgi --socket 0.0.0.0:5000 --protocol=http -w wsgi:app
```
The -w argument is followed by the name of the module (minus the .py extension) plus the name of the callable within the application. In our case, this would be wsgi:app.

Again, visit 127.0.0.1:5000 in your web browser to see the served web pages.

The file * ${PROJECT_ROOT}/WebApp/flask_server.ini*  is the uWSGI configuration file.

###### Create a systemd Unit File
Create a system service:
```console
$ sudo nano /etc/systemd/system/entryphone_app.service
```
Adding:
```
[Unit]
Description=uWSGI instance to serve entryphone
After=network.target

[Service]
User=pi
Group=pi
WorkingDirectory=${PROJECT_ROOT}
Environment="PATH=${PYTHON_ENV_PATH}/bin"
ExecStart=${PYTHON_ENV_PATH}/bin/uwsgi --ini flask_server.ini

[Install]
WantedBy=multi-user.target
```

Then start and enable the service at boot:
```console
sudo systemctl start entryphone_app
sudo systemctl enable entryphone_app
```


###### Configuration of Nginx 
Create a new server block configuration file in Nginx's sites-available directory
```console
$ sudo nano /etc/nginx/sites-available/entry_phone
```
Adding:
```
server {
    listen 80;
    server_name server_domain_or_IP;

    location / {
        include uwsgi_params;
        uwsgi_pass unix:${PROJECT_ROOT}/entry_phone.sock;
    }
}
```
To enable the Nginx server block configuration we've just created, link the file to the sites-enabled directory:
```console
$ sudo ln -s /etc/nginx/sites-available/entry_phone /etc/nginx/sites-enabled
```

With the file in that directory, we can test for syntax errors by typing:
```console
$ sudo nginx -t
$ sudo systemctl restart nginx
$ sudo ufw allow 'Nginx Full'
```
