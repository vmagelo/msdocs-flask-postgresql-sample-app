# Deploy a Flask web app with PostgreSQL in Azure

This is a Python web app using the Flask framework and the Azure Database for PostgreSQL relational database service. The Flask app is hosted in a fully managed Azure App Service. This app is designed to be be run locally and then deployed to Azure. For more information on how to use this web app, see the tutorial [Deploy a Flask web app with PostgreSQL in Azure](TBD).

If you need an Azure account, you can [create on for free](https://azure.microsoft.com/en-us/free/).

Temporary instructions for running:

* clone
* specify .env variables based off of .env.example
* py -m venv .venv
* .venv\scripts\activate
* pip install -r requirements.txt
* cd restaurant_review
* flask db init
* flask db migrate -m "first migration"
* flask run

To do:

* create layout.html and put all common code in there
* ref bootstrap and others stuff from cdn
* investigate /admin functionality with Flask-Admin