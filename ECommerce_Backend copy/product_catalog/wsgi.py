import os
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from store_application.api.app import create_app
from dotenv import load_dotenv

load_dotenv()


app = create_app()

app.config.from_object(os.environ["APP_SETTINGS"])
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
db = SQLAlchemy(app)
migrate = Migrate(app, db, compare_type=True)

# from store_application.models.store_model import Users, Product, Category, Variant, UserProductMapping, Orders, OrderItem


@app.route("/")
def hello():
    return "Hello World!"


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port="5000")
