from app import app,db
from app.models import User, Post
# Работа со второй базой данных
import gunicorn


@app.shell_context_processor
def make_shell_context():
    return {"db": db, 'User': User, 'Post': Post}


if __name__ == '__main__':



    app.debug = False


    app.run()

# исправляет ошибку когда не находит вышеперечисленные аргументы
# set FLASK_DEBUG=1
# set FLASK_APP=microblog.py
