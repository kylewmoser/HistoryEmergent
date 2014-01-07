History Emergent
-------

This is the web application to facilitate the development of History Emergent, a collaborative project to create a chronicle of the future of Earth. It currently supports viewing and annotating documents with the following file extensions:

 - .PDF
 - .DOC
 - .DOCX

Quickstart
----------

Before running History Emergent, you'll need:

 - An [**Amazon Web Services**][1] account (credit card required)
 - A [**Crocodoc**][2] account (no billing method required, the evaluation mode is sufficient)
 - A **PostgreSQL** database (You can get a free one from [Heroku Postgres][3] under the Dev Plan)
 - A [**Recaptcha**][4] account with Google

To get started, clone this repo:

    git clone https://github.com/scascketta/DocHost.git


History Emergent uses the `app.config` dictionary in Flask for configuration details. To keep things neat, `app.config` loads those details from the `config.py` file. 

Add the following values to their appropriate variable in `config.py` :

 - **SECRET_KEY** (must be reasonably long enough to generate secure CSRF tokens)
 - **RECAPTCHA_PUBLIC_KEY** and **RECAPTCHA_PRIVATE_KEY**  (get these from your [Recaptcha account page][5])
 - **DEV_DB_URL** and **PROD_DB_URL** (the connection URL(s) for your database(s)). 
     - If you're just using a single database, put the connection URL in **DEV_DB_URL**
 - **CROC_API_TOKEN** (the API token to authenticate requests to Crocodoc, find it in your [Crocodoc dashboard][6])
 - **BUCKET_NAME** (the name of your Amazon S3 bucket used to store documents and thumbnails)
 - **AWS_ACCESS_KEY** and **AWS_SECRET_KEY** (this provides these credentials to [Boto][7] if you don't have them in `~/.boto`)

Install the Python package requirements for DocHost using [pip][8] (**please, please, please use a [virtualenv][9] to keep your Python environments isolated**). 

    pip install -r requirements.txt

Finally, start the application with the Flask development server:

    python run.py


----------


 To run the server in an externally visible fashion, edit the `app.run()` statement in run.py to use `'0.0.0.0'`. Remember, *if you bind to port 80, **you need to start the server with root permissions***.
 
 

Using Gunicorn
--------------

 You can also deploy the server with [Gunicorn][10], a Python WSGI HTTP server as an alternative to the built-in Flask development server.
 
 To use Gunicorn, remove or comment out the `app.run()` statement in `run.py`.
 
 Install Gunicorn with `pip install gunicorn`.
 
 Start Gunicorn with:

     gunicorn -w 2 -b 0.0.0.0:5000 run:app

 This starts Gunicorn with 2 worker processes.


  [1]: http://aws.amazon.com/
  [2]: https://crocodoc.com/
  [3]: https://www.heroku.com/postgres
  [4]: http://www.google.com/recaptcha
  [5]: https://www.google.com/recaptcha/admin/list
  [6]: https://crocodoc.com/dashboard/
  [7]: http://boto.readthedocs.org/en/latest/
  [8]: http://www.pip-installer.org/en/latest/
  [9]: http://www.virtualenv.org/en/latest/virtualenv.html
  [10]: http://docs.gunicorn.org/en/latest/index.html
