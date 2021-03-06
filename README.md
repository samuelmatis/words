# Langmaster.io #

Web application for smarter memorizing vocabulary of a foreign language.

### New version in progress - [AngularJS and NodeJS rewrite](https://github.com/samuelmatis/langmaster-v2-angular) ###

### Technologies: ####

#### Server: ####
* Python (Flask framework)
* MongoDB (MongoEngine)

#### Client: ####
* Backbone.js with Marionette
* Twitter Bootstrap
* OAuth.io


### Running locally ###

1. Install dependencies : `(sudo) npm install && pip install -r requirements.txt && bower install`
2. Run the application : `python server/server.py`
3. Open a web browser with URL [http://localhost:5000](http://localhost:5000)


### Setting up database ###
* #### Use our demo database (publicly available) ####

    1. Go to the *server/db.py*
    2. Change `os.environ['MONGOLAB_URI']` to `'mongodb://admin:iicenajv@ds053948.mongolab.com:53948/words'`

* #### Use your own database ####

    1. Create your own database and create *users* collection
    2. Go to the *server/db.py*
    3. Change `os.environ['MONGOLAB_URI']` with your *mongodb://* database url


### Build the application ###

1. Run `grunt build` command from command line
2. Go to the *server/app.py*
3. Change `../app` folders to `../dist` (2x)
4. Run the application : `python server/server.py`


[![Bitdeli Badge](https://d2weczhvl823v0.cloudfront.net/samuelmatis/langmaster.io/trend.png)](https://bitdeli.com/free "Bitdeli Badge")

