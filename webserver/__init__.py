from flask import Flask
from flask_mail import Mail, Message
#app = Flask(__name__)
#app.config.update(
	#DEBUG=True,
	#MAIL_SERVER="smtp.gmail.com",
	#MAIL_PORT=465,
	#MAIL_USE_SSL=True,
	#MAIL_USERNAME='scoliagatech@gmail.com',
	#MAIL_PASSWORD='Team3-WebServer'
	#)

mail = Mail()

from webserver.backend import db_util
db_util.init_db()
#db_util.clean_db()
def create_app(config_class=None):
	app = Flask(__name__)
	mail.init_app(app)
	app.config.update(
	DEBUG=True,
	MAIL_SERVER="smtp.gmail.com",
	MAIL_PORT=465,
	MAIL_USE_SSL=True,
	MAIL_USERNAME='scoliagatech@gmail.com',
	MAIL_PASSWORD='Team3-WebServer'
	)
	with app.app_context():	
		from webserver.backend.routes import mod
		from webserver.frontend.routes import mod

		app.register_blueprint(frontend.routes.mod)
		app.register_blueprint(backend.routes.mod)
		return app
