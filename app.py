from flask import Flask

app = Flask(__name__, template_folder='template')

# Using a development configuration
app.config.from_object('config.DevConfig')

# Using a production configuration
# app.config.from_object('config.ProdConfig')


# app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://admin:12345678@localhost:3306/flask_blog"
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
