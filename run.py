from project.config import DevelopmentConfig
from project.dao.models import Genre, Director, Movie, User
from project.server import create_app, db

app = create_app(DevelopmentConfig)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80, debug=True)
