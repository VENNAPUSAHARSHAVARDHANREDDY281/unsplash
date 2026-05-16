from flask import Flask
from flask_cors import CORS
from config import Config
from extensions import db

app = Flask(__name__)
app.config.from_object(Config)

CORS(app)

db.init_app(app)

@app.route("/")
def home():
    return {"message": "Rental Zonn Backend Running"}

with app.app_context():
    from models import User
    db.create_all()

if __name__ == "__main__":
    from routes import register_routes
    register_routes(app)

    app.run(debug=True)