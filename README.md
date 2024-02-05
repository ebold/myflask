# myflask

Flask web application.

## 1. Development

### 1.1. Run a Flask app locally on a development host

Start the flask app:

```
$ source ~/venv/.venv/bin/activate  # optional, activate the virtual environment
$ flask --app app run
```

Open a web browser and nagivate to the local host with port 5000: *http://127.0.0.1:5000*

## 2. Deployment

### 2.1. What to do on the local web server after updating the local repo

After update just reload the 'nginx' and 'gunicorn' services:

```
$ sudo systemctl restart nginx
$ sudo systemctl restart gunicorn
```