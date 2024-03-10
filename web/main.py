from flask import Flask
from data import db_session
from flask_login import LoginManager
from data.users import User
from data.jobs import Jobs
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


def main():
    db_session.global_init("db/blogs.db")
    user = User()
    user2 = User()
    user3 = User()
    user4 = User()
    job = Jobs()
    user.name = "Ridley"
    user.surname = 'Scott'
    user.age = 31
    user.position = "captain"
    user.speciality = 'research engineer'
    user.address = 'module_1'
    user.email = 'scott_chief@mars.org'
    user2.name = "Andy"
    user2.surname = 'Uir'
    user2.age = 23
    user2.position = "comrad"
    user2.speciality = 'austranaut'
    user2.address = 'module_1'
    user2.email = 'Andy@mars.org'
    user3.name = "Mark"
    user3.surname = 'Uotny'
    user3.age = 22
    user3.position = "pilot"
    user3.speciality = 'pilot'
    user3.address = 'module_2'
    user3.email = 'Uotny@mars.org'
    user4.name = "Teddy"
    user4.surname = 'Sanders'
    user4.age = 26
    user4.position = "comrad"
    user4.speciality = 'chief'
    user4.address = 'module_4'
    user4.email = 'Sanders@mars.org'
    job.team_leader = 1
    job.job = 'deployment of residential modules 1 and 2'
    job.work_size = 15
    job.collaborators = [2, 3]
    job.start_date = datetime.datetime.now()
    job.is_finished = False
    db_sess = db_session.create_session()
    db_sess.add(user)
    db_sess.commit()
    app.run()


if __name__ == '__main__':
    main()