stripe-potato-demo
==================

Example [heroku] app that shows how [django-stripe-payments] and [checkout.js] work together.

Development:
---------------
1- Install [postgres] ([for Mac])

(You can use sqlite, but using different databases on production and development is not a good idea)

2- [Install & setup Heroku]

3- Install [virtualenv] & create one

4- Run bootstrap.py
```sh
python bootstrap.py
```
5- Install dependencies via fabric
```sh
fab deps
```
6- Put your Stripe and AWS keys in local_settings.py

7- Create Stripe plans
```sh
python app/manage.py init_plans
```
8- Start devserver
```sh
fab runserver
```
or
```sh
python app/manage.py runserver
```

[postgres]: http://www.postgresql.org/
[for Mac]: http://postgresapp.com/
[heroku]: http://heroku.com  
[Install & setup Heroku]: https://devcenter.heroku.com/articles/quickstart
[virtualenv]: http://virtualenvwrapper.readthedocs.org/en/latest/
[django-stripe-payments]: https://github.com/eldarion/django-stripe-payments
[checkout.js]: https://stripe.com/docs/checkout
