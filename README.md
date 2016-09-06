##Falcon Twitter API Example

Falcon 1.0.0 Python 2 application. 

###Making Requests
Example request, note that the username:password should be `base64` (e.g. `echo -n 'lorena:supersecretpassword' | openssl base64`) encoded. 

```curl 'http://localhost:9000/home_timeline?count=20' -i -H 'Authorization: Basic username:password'```

###Authorization
You'll need to create a `htpasswd` [password file](https://httpd.apache.org/docs/current/programs/htpasswd.html) and add users via `htpasswd -c /path/to/thing/.htpasswd lorena`.

The project makes use of the [Talon's auth middleware](https://github.com/talons/talons) package with some adjustments to [support Falcon > 0.4](https://github.com/talons/talons/issues/40).

###Getting Started

1. Create a `virtualenv`, installing the requirements found in `requirements.txt`. 
2. Set credentials in a `config.yml` file in project root, use `example_config.yml` as a template.
3. Run `gunicorn app` 

*Note: If you are running the application with PyCharm you can follow these [instructions](http://stackoverflow.com/questions/20732904/how-to-debug-flask-app-with-pycharm-2-x-thats-running-on-gunicorn) to run the application.*

