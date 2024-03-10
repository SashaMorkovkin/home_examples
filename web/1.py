from flask import Flask, render_template, redirect, request, make_response, abort, url_for
from flask import session
from data import db_session, new_api
import datetime
import datetime as dt
from forms.user import LoginForm, RegisterForm
from data.users import User
from data.jobs import Jobs
from flask_login import LoginManager, login_user, login_required, logout_user
from flask_login import current_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
app.config['PERMANENT_SESSION_LIFETIME'] = dt.timedelta(days=1)
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/')
def index():
    db_sess = db_session.create_session()
    users = db_sess.query(User).all()
    jobs = db_sess.query(Jobs).all()
    return render_template('profs.html', users=users, jobs=jobs)


@app.route("/cookie_test")
def cookie_test():
    visits_count = int(request.cookies.get("visits_count", 0))
    if visits_count:
        res = make_response(
            f"Вы пришли на эту страницу {visits_count + 1} раз")
        res.set_cookie("visits_count", str(visits_count + 1),
                       max_age=60 * 60 * 24 * 365 * 2)
    else:
        res = make_response(
            "Вы пришли на эту страницу в первый раз за последние 2 года")
        res.set_cookie("visits_count", '1',
                       max_age=60 * 60 * 24 * 365 * 2)
    return res


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form, message='Пароли разные')
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.name == form.name.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form, message='Пользователь уже существует')
        user = User(
            name=form.name.data,
            email=form.email.data,
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/')
    return render_template('register.html', title='Регистрация',
                           form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.name == form.name.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect('/')
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/training/<prof>')
def traning(prof):
    return render_template('index.html', prof=prof)


@app.route('/photo', methods=['POST', 'GET'])
def sample_file_upload():
    if request.method == 'GET':
        return f'''<!doctype html>
                        <html lang="en">
                          <head>
                            <meta charset="utf-8">
                            <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
                             <link rel="stylesheet"
                             href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta1/dist/css/bootstrap.min.css"
                             integrity="sha384-giJF6kkoqNQ00vy+HMDP7azOuL0xtbfIcaT9wjKHr8RbDVddVHyTfAAsrekwKmP1"
                             crossorigin="anonymous">
                            <link rel="stylesheet" type="text/css" href="{url_for('static', filename='css/style.css')}" />
                            <title>Пример загрузки файла</title>
                          </head>
                          <body>
                            <h1>Загрузим файл</h1>
                            <form method="post" enctype="multipart/form-data">
                               <div class="form-group">
                                    <label for="photo">Выберите файл</label>
                                    <input type="file" class="form-control-file" id="photo" name="file">
                                </div>
                                <button type="submit" class="btn btn-primary">Отправить</button>
                            </form>
                          </body>
                        </html>'''
    elif request.method == 'POST':
        f = request.files['file']
        return f'''<!doctype html>
                                <html lang="en">
                                  <head>
                                    <meta charset="utf-8">
                                    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
                                     <link rel="stylesheet"
                                     href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta1/dist/css/bootstrap.min.css"
                                     integrity="sha384-giJF6kkoqNQ00vy+HMDP7azOuL0xtbfIcaT9wjKHr8RbDVddVHyTfAAsrekwKmP1"
                                     crossorigin="anonymous">
                                    <link rel="stylesheet" type="text/css" href="{url_for('static', filename='css/style.css')}" />
                                    <title>Пример загрузки файла</title>
                                  </head>
                                  <body>
                                    <h1>Загрузим файл</h1>
                                    <form method="post" enctype="multipart/form-data">
                                       <div class="form-group">
                                            <label for="photo">Выберите файл</label>
                                            <input type="file" class="form-control-file" id="photo" name="file">
                                        </div>
                                        <div>{f}</div>
                                        <button type="submit" class="btn btn-primary">Отправить</button>
                                    </form>
                                  </body>
                                </html>'''


@app.route('/list_prof')
def list_prof():
    list = 'ol'
    arr = ['инженер-исследователь', 'пилот', 'строитель', 'экзобиолог', 'врач', 'инженер по терраформированию',
           'климатолог', 'специалист по радиационной защите', 'астрогеолог', 'гляциолог', 'инженер жизнеобеспечения',
           'метеоролог', 'оператор марсохода', 'киберинженер', 'штурман', 'пилот дронов']
    return render_template('list_prof.html', tegs=list, proffecions=arr)


@app.route('/answer')
@app.route('/auto_answer')
def answer():
    dict = {'title': 'Анкета', 'surname': 'Wathy', 'name': 'Mark', 'education': 'Хорошее', 'profession': 'штурман',
            'sex': 'мужской', 'motivation': 'Всегда мечтал торчать на Марсе!', 'ready': 'True'}
    return render_template('auto_answer.html', dict=dict)


@app.route('/login', methods=['GET', 'POST'])
def alert_form():
    form = LoginForm()
    return render_template('login.html', title='Аварийный доступ', form=form)


@app.route('/distribution')
def distribution():
    arr = ['Беренс Евгений', 'Басаргин Владимир', 'Балк Захар', 'Бурачек Павел', 'Васильев Михаил',
           'Воеводский Аркадий']
    return render_template('rooms.html', title='По каютам!', arr=arr)


@app.route('/promotion')
def promoution():
    return """<!doctype html>
                <html lang="en">
                    <head>
                        <meta charset="utf-8">
                    </head>
                    <body>
                        <h3>Человечество вырастает из детства.</h3><br><h3>Человечеству мала 
                        одна планета.</h3><br><h3>Мы сделаем обитаемыми безжизненные пока
                         планеты.</h3><br><h3>И начнем с Марса!</h3><br><h3>Присоединяйся!</h3>
                    </body>
                </html>"""


@app.route('/promotion_image')
def promotion_image():
    return f"""<!doctype html>ц
                <html lang="en">
                    <head>
                        <meta charset="utf-8">
                        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.7.2/dist/css/
                        bootstrap.min.css">
                        <link rel="stylesheet" type="text/css" href="{url_for('static', filename='css/style.css')}" />
                        <title>Отбор космонавтов</title>
                    </head>
                    <body>
                        <h1>Жди нас, Марс!</h1>
                        <img src="{url_for('static', filename='images/mars.png')}" 
                        alt="здесь должна была быть картинка, но не нашлась">
                        <h3 class="text-secondary">Человечеству мала одна планета.</h3>
                        <h3>Мы сделаем обитаемыми безжизненные пока планеты.</h3>
                        <h3>И начнем с Марса!</h3>
                        <h3>Присоединяйся!</h3>
                    </body>
                </html>"""


@app.route('/astronaut_selection', methods=['POST', 'GET'])
def astronaut_selection():
    if request.method == 'GET':
        return f'''<!doctype html>
                        <html lang="en">
                          <head>
                            <meta charset="utf-8">
                            <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
                            <link rel="stylesheet"
                   href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta1/dist/css/bootstrap.min.css"
                   integrity="sha384-giJF6kkoqNQ00vy+HMDP7azOuL0xtbfIcaT9wjKHr8RbDVddVHyTfAAsrekwKmP1"
                   crossorigin="anonymous">
                            <link rel="stylesheet" type="text/css" href="{url_for('static', filename='css/style.css')}" />
                            <title>Пример формы</title>
                          </head>
                          <body>
                            <h1 style="text-align: center">Анкета претендента на участие в миссии</h1>
                            <div>
                                <form class="login_form" method="post">
                                    <input type="text" class="form-control" id="email" aria-describedby="emailHelp" placeholder="Введите фамилию" name="email">
                                    <input type="text" class="form-control" id="password" placeholder="Введите имя" name="password"><br>
                                    <input type="email" class="form-control" id="password" placeholder="Введите email" name="password"><br>
                                    <div class="form-group">
                                        <label for="classSelect">Какое у вас образование?</label>
                                        <select class="form-control" id="classSelect" name="class">
                                          <option>Начальное</option>
                                          <option>Среднее</option>
                                          <option>Высшее</option>
                                        </select>
                                     </div><br>
                                     <label for="form-check">Какие у вас профессии?</label><br>
                                     <div class="form-check">
                                          <input class="form-check-input" type="checkbox" value="" id="flexCheckDefault">
                                          <label class="form-check-label" for="flexCheckDefault">
                                            инженер-исследователь
                                          </label>
                                        </div>
                                        <div class="form-check">
                                          <input class="form-check-input" type="checkbox" value="" id="flexCheckChecked">
                                          <label class="form-check-label" for="flexCheckChecked">
                                            пилот
                                          </label>
                                        </div>
                                    <div class="form-check">
                                          <input class="form-check-input" type="checkbox" value="" id="flexCheckChecked">
                                          <label class="form-check-label" for="flexCheckChecked">
                                            строитель
                                          </label>
                                        </div>
                                    <div class="form-check">
                                          <input class="form-check-input" type="checkbox" value="" id="flexCheckChecked">
                                          <label class="form-check-label" for="flexCheckChecked">
                                            экзобиолог
                                          </label>
                                        </div>
                                    <div class="form-check">
                                          <input class="form-check-input" type="checkbox" value="" id="flexCheckChecked">
                                          <label class="form-check-label" for="flexCheckChecked">
                                            врач
                                          </label>
                                        </div>
                                    <div class="form-check">
                                          <input class="form-check-input" type="checkbox" value="" id="flexCheckChecked">
                                          <label class="form-check-label" for="flexCheckChecked">
                                            инженер по терраформированию
                                          </label>
                                        </div>
                                    <div class="form-check">
                                          <input class="form-check-input" type="checkbox" value="" id="flexCheckChecked">
                                          <label class="form-check-label" for="flexCheckChecked">
                                            климатолог
                                          </label>
                                        </div>
                                    <div class="form-check">
                                          <input class="form-check-input" type="checkbox" value="" id="flexCheckChecked">
                                          <label class="form-check-label" for="flexCheckChecked">
                                            специалист по радиационной защите,
                                          </label>
                                        </div>
                                    <div class="form-check">
                                          <input class="form-check-input" type="checkbox" value="" id="flexCheckChecked">
                                          <label class="form-check-label" for="flexCheckChecked">
                                            астрогеолог
                                          </label>
                                        </div>
                                    <div class="form-check">
                                          <input class="form-check-input" type="checkbox" value="" id="flexCheckChecked">
                                          <label class="form-check-label" for="flexCheckChecked">
                                            гляциолог
                                          </label>
                                        </div>
                                    <div class="form-check">
                                          <input class="form-check-input" type="checkbox" value="" id="flexCheckChecked">
                                          <label class="form-check-label" for="flexCheckChecked">
                                            инженер жизнеобеспечения
                                          </label>
                                        </div>
                                    <div class="form-check">
                                          <input class="form-check-input" type="checkbox" value="" id="flexCheckChecked">
                                          <label class="form-check-label" for="flexCheckChecked">
                                            метеоролог
                                          </label>
                                        </div>
                                    <div class="form-check">
                                          <input class="form-check-input" type="checkbox" value="" id="flexCheckChecked">
                                          <label class="form-check-label" for="flexCheckChecked">
                                            оператор марсохода
                                          </label>
                                        </div>
                                    <div class="form-check">
                                          <input class="form-check-input" type="checkbox" value="" id="flexCheckChecked">
                                          <label class="form-check-label" for="flexCheckChecked">
                                            киберинженер
                                          </label>
                                        </div>
                                    <div class="form-check">
                                          <input class="form-check-input" type="checkbox" value="" id="flexCheckChecked">
                                          <label class="form-check-label" for="flexCheckChecked">
                                            штурман
                                          </label>
                                        </div>
                                    <div class="form-check">
                                          <input class="form-check-input" type="checkbox" value="" id="flexCheckChecked">
                                          <label class="form-check-label" for="flexCheckChecked">
                                            пилот дронов
                                          </label>
                                        </div><br>
                                    <div class="form-group">
                                        <label for="about">Почему вы хотите принять участие в миссии?</label>
                                        <textarea class="form-control" id="about" rows="3" name="about"></textarea>
                                    </div><br>
                                    <div class="form-group">
                                        <label for="form-check">Укажите пол</label>
                                        <div class="form-check">
                                          <input class="form-check-input" type="radio" name="sex" id="male" value="male" checked>
                                          <label class="form-check-label" for="male">
                                            Мужской
                                          </label>
                                        </div>
                                        <div class="form-check">
                                          <input class="form-check-input" type="radio" name="sex" id="female" value="female">
                                          <label class="form-check-label" for="female">
                                            Женский
                                          </label>
                                        </div><br>
                                    </div>
                                    <div class="form-group">
                                        <label for="photo">Приложите фотографию</label>
                                        <input type="file" class="form-control-file" id="photo" name="file">
                                    </div><br>
                                    <div class="form-group form-check">
                                        <input type="checkbox" class="form-check-input" id="acceptRules" name="accept">
                                        <label class="form-check-label" for="acceptRules">Готов остаться на марсе?</label>
                                    </div>
                                    <button type="submit" class="btn btn-primary">Записаться</button>
                                </form>
                            </div>
                          </body>
                        </html>'''
    elif request.method == 'POST':
        print(request.form['email'])
        print(request.form['password'])
        print(request.form['class'])
        print(request.form['file'])
        print(request.form['about'])
        print(request.form['accept'])
        print(request.form['sex'])
        return "Форма отправлена"


@app.route('/choice/<planet_name>')
def choice(planet_name):
    return f"""<!doctype html>
                <html lang="en">
                    <head>
                    <meta charset="utf-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
                    <link rel="stylesheet"
                   href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta1/dist/css/bootstrap.min.css"
                   integrity="sha384-giJF6kkoqNQ00vy+HMDP7azOuL0xtbfIcaT9wjKHr8RbDVddVHyTfAAsrekwKmP1"
                   crossorigin="anonymous">
                    <title>Варианты выбора</title>
                  </head>
                    <body>
                        <h1>Моё предложение: {planet_name}</h1>
                        <h2>Эта планета близка к земле</h2>
                    <div class="alert alert-primary" role="alert">
                      На ней много необходимых ресурсов
                    </div>
                    <div class="alert alert-secondary" role="alert">
                      На ней есть вода и атмосфера
                    </div>
                    <div class="alert alert-success" role="alert">
                      На ней сть небольшое магнитное поле
                    </div>
                    <div class="alert alert-danger" role="alert">
                      Наконец, она красива!
                    </div>
                    </body>
                </html>"""


@app.route('/results/<nickname>/<int:level>/<float:rating>')
def results(nickname, level, rating):
    return f"""<!doctype html>
                <html lang="en">
                    <head>
                    <meta charset="utf-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
                    <link rel="stylesheet"
                   href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta1/dist/css/bootstrap.min.css"
                   integrity="sha384-giJF6kkoqNQ00vy+HMDP7azOuL0xtbfIcaT9wjKHr8RbDVddVHyTfAAsrekwKmP1"
                   crossorigin="anonymous">
                    <title>Результаты</title>
                  </head>
                    <body>
                        <h1>Результаты отбора</h1>
                        <h2>Претендента на участие в миссии {nickname}</h2>
                    <div class="alert alert-primary" role="alert">
                      <h4>Поздравляем! Ваш рейтинг после {str(level)} этапа отбора</h4>
                    </div>
                      <h4>составляет {rating} балла</h4>
                    </div>
                    <div class="alert alert-success" role="alert">
                      <h4>Желаем удачи</h4>
                    </div>
                    </body>
                </html>"""


@app.route('/carousel')
def carousel():
    return f"""<!doctype html>ц
                <html lang="en">
                    <head>
                        <meta charset="utf-8">
                        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.7.2/dist/css/
                        bootstrap.min.css">
                        <link rel="stylesheet" type="text/css" href="{url_for('static', filename='css/style.css')}" />
                        <title>Пейзажи марса</title>
                    </head>
                    <body>
                        <div id="carousel" class="carousel slide" data-ride="carousel">
                              <div class="carousel-inner">
                                <div class="carousel-item active">
                                  <img class="d-block w-100" href="{url_for('static', filename='images/mars1.jpg')}" alt="fae">
                                </div>
                                <div class="carousel-item">
                                  <img class="d-block w-100" href="{url_for('static', filename='images/mars2.jpg')}" alt="wfa">
                                </div>
                                <div class="carousel-item">
                                  <img class="d-block w-100" href="{url_for('static', filename='images/mars3.jpg')}" alt="fawf">
                                </div>
                                <div class="carousel-item">
                                  <img class="d-block w-100" href="{url_for('static', filename='images/mars4.jpg')}" alt="wfa">
                                </div>
                                <div class="carousel-item">
                                  <img class="d-block w-100" href="{url_for('static', filename='images/mars5.jpg')}" alt="wfaf">
                                </div>
                              </div>
                              <a class="carousel-control-prev" href="#" role="button" data-slide="prev">
                                <span class="carousel-control-prev-icon" aria-hidden="true"></span>
                                <span class="sr-only">Previous</span>
                              </a>
                              <a class="carousel-control-next" href="#" role="button" data-slide="next">
                                <span class="carousel-control-next-icon" aria-hidden="true"></span>
                                <span class="sr-only">Next</span>
                              </a>
                            </div>
                    </body>
                </html>"""


def main():
    db_session.global_init('db/blogs.db')
    comand = User()
    comand2 = User()
    comand3 = User()
    comand4 = User()
    job = Jobs()
    comand.id = 1
    comand.name = "Ridley"
    comand.surname = 'Scott'
    comand.age = 31
    comand.position = "captain"
    comand.speciality = 'research engineer'
    comand.address = 'module_1'
    comand.email = 'scott_chief@mars.org'
    comand2.id = 2
    comand2.name = "Andy"
    comand2.surname = 'Uir'
    comand2.age = 23
    comand2.position = "comrad"
    comand2.speciality = 'austranaut'
    comand2.address = 'module_1'
    comand2.email = 'Andy@mars.org'
    comand3.id = 3
    comand3.name = "Mark"
    comand3.surname = 'Uotny'
    comand3.age = 22
    comand3.position = "pilot"
    comand3.speciality = 'pilot'
    comand3.address = 'module_2'
    comand3.email = 'Uotny@mars.org'
    comand4.id = 4
    comand4.name = "Teddy"
    comand4.surname = 'Sanders'
    comand4.age = 26
    comand4.position = "comrad"
    comand4.speciality = 'chief'
    comand4.address = 'module_4'
    comand4.email = 'Sanders@mars.org'
    job.team_leader = 1
    job.job = 'deployment of residential modules 1 and 2'
    job.work_size = 15
    job.collaborators = '2, 3'
    job.start_date = datetime.datetime.now()
    job.is_finished = True
    db_sess = db_session.create_session()
    db_sess.add(comand)
    db_sess.add(comand2)
    db_sess.add(comand3)
    db_sess.add(comand4)
    db_sess.add(job)
    db_sess.commit()
    #  app.register_blueprint(new_api.blueprint)
    app.run()


if __name__ == '__main__':
    main()