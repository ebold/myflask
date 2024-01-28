# myflask

Flask web application.

## What to do on the local web server after updating the local repo

After update just reload the 'nginx' and 'gunicorn' services:

```
$ sudo systemctl restart nginx
$ sudo systemctl restart gunicorn
```