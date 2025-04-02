import flask as f
from flask import render_template, request, redirect, flash, url_for
import os
from werkzeug.utils import secure_filename
from flask_login import (
    LoginManager,
    login_user,
    logout_user,
    login_required,
    current_user,
)
from forms.edit_profile import SettingsForm
from forms.login_form import LoginForm
from data import db_session
from data.comments import Comments
from data.users import User
from data.posts import Posts
from data.chats import Chat
from forms.create_post_form import CreatePostForm
from forms.registr_form import *
from forms.serch_user import SerchUserForm


app = f.Flask(__name__)
db_session.global_init("db/Code.db")
app.config["SECRET_KEY"] = "code_secret_key"
app.config["UPLOAD_FOLDER"] = os.path.join(app.root_path, "static/uploads")
app.config["ALLOWED_EXTENSIONS"] = {"png", "jpg", "jpeg", "gif"}


login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)

# EXEMPT_VIEWS = ['login', '/create_accaunt']

# @app.before_request
# def before_request():
#     if request.endpoint in EXEMPT_VIEWS:
#         return None
#     if not current_user.is_authenticated:
#         return redirect(url_for('login'))

@app.route("/create_accaunt", methods=["GET", "POST"])
def form():
    form = Registration()
    if form.validate_on_submit():
        if form.password.data != form.password_repeat.data:
            return render_template(
                "registr.html", form=form, message="Пароли не совпадают"
            )

        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template(
                "registr.html", form=form, message="Такой пользователь уже есть"
            )

        user = User(
            surname=form.surname.data,
            name=form.name.data,
            age=form.age.data,
            city=form.city.data,
            sex=form.sex.data,
            email=form.email.data,
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect("/")

    return render_template("registr.html", form=form)


@app.route('/main', methods=['POST', 'GET'])
def main():
    if not current_user.is_authenticated:
        return redirect("/")
    form = SerchUserForm()
    createPostForm = CreatePostForm()
    if form.validate_on_submit() and form.serch_user_id.data:
        return redirect(f"/id/{form.serch_user_id.data}")
    if createPostForm.validate_on_submit():
        print("OK")
        print(current_user.id)
        return redirect(f"/id/{current_user.id}")
    #Из пост запроса получаем id пользователя и меняем страницу в зависимости от полученной информации
    html = f.render_template(r"post_block_main.html",
                             createPostForm = createPostForm, 
                            post_id=[1, 2, 3], 
                            form=form, 
                            ClientId=f'id/{current_user.id}',  
                            cntBlocks=3, 
                            imgs=[
                                ['../static/img/post_test_1.jpg', 
                                 '../static/img/post_test_2.jpg', 
                                 '../static/img/post_test_3.jpg', 
                                 '../static/img/avatar.jpg'], 
                                ['../static/img/post_test_1.jpg', 
                                 '../static/img/post_test_2.jpg', 
                                 '../static/img/post_test_3.jpg', 
                                 '../static/img/avatar.jpg'], 
                                ['../static/img/post_test_1.jpg', 
                                 '../static/img/post_test_2.jpg', 
                                 '../static/img/post_test_3.jpg', 
                                 '../static/img/avatar.jpg']], 
                                likesBool=[0, 0, 0], 
                                id=['#aa', '#bb', '#cc'], 
                                caption=["Описание 1","Описание 2","Описание 3"],
                                cntRequests=2,
                                friend_request_id=[2, 3],
                                friend_request_avatar=['../static/img/post_test_2.jpg', '../static/img/logo.png'],
                                friend_request_name=['rrrrr', 'hhhhhh'],
                                friend_request_surname=['ggggg', 'jjjjj'],
                                seeFilter = True,
                                chat_id = ['1', '2', '3'],
                                postCntLikes = [25, 60, 5],
                                postCntComments = [3, 40, 1],
                                postCreators = [1, 2, 1])
    filter_value = request.args.get('filter')
    print(filter_value)
    return html


@app.route('/likes', methods=['POST', 'GET'])
def likes():
    if not current_user.is_authenticated:
        return redirect("/")
    form = SerchUserForm()
    createPostForm = CreatePostForm()
    if form.validate_on_submit() and form.serch_user_id.data:
        return redirect(f"/id/{form.serch_user_id.data}")
    if createPostForm.validate_on_submit():
        print("OK")
        print(current_user.id)
        return redirect(f"/id/{current_user.id}")
    #Из пост запроса получаем id пользователя и меняем страницу в зависимости от полученной информации
    html = f.render_template(r"post_block_likes.html",
                            createPostForm=createPostForm, 
                            post_id=[1, 2, 3], 
                            form=form, 
                            ClientId=f'id/{current_user.id}',  
                            cntBlocks=3, 
                            imgs=[['../static/img/post_test_1.jpg', 
                                   '../static/img/post_test_2.jpg', 
                                   '../static/img/post_test_3.jpg', 
                                   '../static/img/avatar.jpg'], 
                                ['../static/img/post_test_1.jpg', 
                                 '../static/img/post_test_2.jpg', 
                                 '../static/img/post_test_3.jpg', 
                                 '../static/img/avatar.jpg'], 
                                ['../static/img/post_test_1.jpg', 
                                 '../static/img/post_test_2.jpg', 
                                 '../static/img/post_test_3.jpg', 
                                 '../static/img/avatar.jpg']], 
                                likesBool=[1, 1, 1], 
                                id=['#aa', '#bb', '#cc'], 
                                caption=["Описание 1","Описание 2","Описание 3"],
                                cntRequests=0,
                                friend_request_id=[],
                                friend_request_avatar=[],
                                friend_request_name=[],
                                friend_request_surname=[],
                                seeFilter = True,
                                chat_id = ['1', '2', '3'],
                                postCntLikes = [25, 60, 5],
                                postCntComments = [3, 40, 1],
                                postCreators = [2, 2, 1])
    return html


@app.route('/friends', methods=['POST', 'GET'])
def friends():
    if not current_user.is_authenticated:
        return redirect("/")
    form = SerchUserForm()
    if form.validate_on_submit():
        return redirect(f"/id/{form.serch_user_id.data}")
    html = f.render_template(r"friends.html", 
                            form=form,
                            ClientId = f'/id/{current_user.id}', 
                            friends=2,
                            friend_id=[2, 3],
                            friend_avatar=["../static/img/post_test_3.jpg", "../static/img/post_test_2.jpg"],
                            friend_name=['кто-то', 'НеЮля'],
                            friend_surname=['Кто-тович', 'НеИванова'],
                            chat_id=['1', '2'],
                            is_block = [True, False],
                            cntRequests=2,
                            friend_request_id=[2, 3],
                            friend_request_avatar=['../static/img/post_test_2.jpg', '../static/img/logo.png'],
                            friend_request_name=['rrrrr', 'hhhhhh'],
                            friend_request_surname=['ggggg', 'jjjjj'],
                            seeFilter = False)
    return html

@app.route("/", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect("/main")
    form = LoginForm()
    print(current_user)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=True)
            return redirect(f"/id/{user.id}")
        return render_template(
            "logo_form.html", message="Неправильный логин или пароль", form=form
        )
    return render_template("logo_form.html", form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")

@app.route("/id/<Clientid>", methods=["POST", "GET"])
def id(Clientid):
    if not current_user.is_authenticated:
        return redirect("/")
    Clientid=int(Clientid)
    form = SerchUserForm()
    createPostForm = CreatePostForm()
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == Clientid).first()
    if not user:
        f.abort(404)
    name = user.name

    if form.validate_on_submit() and form.serch_user_id.data:
        return redirect(f"/id/{form.serch_user_id.data}")
    if createPostForm.validate_on_submit():
        print("OK")
        print(current_user.id)
        return redirect(f"/id/{current_user.id}")
    print(f"/id/{current_user.id}")
    ClientId = f"/id/{current_user.id}"
    html = f.render_template(
        r"post_block.html",
        createPostForm = createPostForm,
        ClientId=ClientId,
        
        UserName=name,
        cntBlocks=3,
        post_id=[1, 2, 3],
        imgs=[
            [
                "../static/img/post_test_1.jpg",
                "../static/img/post_test_2.jpg",
                "../static/img/post_test_3.jpg",
                "../static/img/avatar.jpg",
            ],
            [
                "../static/img/post_test_1.jpg",
                "../static/img/post_test_2.jpg",
                "../static/img/post_test_3.jpg",
                "../static/img/avatar.jpg",
            ],
            [
                "../static/img/post_test_1.jpg",
                "../static/img/post_test_2.jpg",
                "../static/img/post_test_3.jpg",
                "../static/img/avatar.jpg",
            ],
        ],
        likesBool=[0, 0, 0],
        id=["#aa", "#bb", "#cc"],
        caption=["Описание 1", "Описание 2", "Описание 3"],
        serch_user=Clientid,
        form=form,
        cntRequests=0,
        friend_request_id=[],
        friend_request_avatar=[],
        friend_request_name=[],
        friend_request_surname=[],
        seeFilter = True,
        chat_id = ['1', '2', '3'],
        postCntLikes = [25, 60, 5],
        postCntComments = [3, 40, 1],
        postCreators = [user.id, user.id, user.id],
        # userBackground = '../static/img/post_test_2.jpg',
        # userAvatar = '../static/img/post_test_3.jpg',
        # CurrentUserAvatar = '../static/img/post_test_2.jpg',
        # serch_user_in_friends = False,
        # requests = [1, 3],
        # user_chat_id = 8,
    )
    return html


# @app.route('/id/<Clientid>', methods=['POST', 'GET'])
# def id(Clientid):
#     form = SerchUserForm()

#     # Проверка существования исходного пользователя
#     db_sess = db_session.create_session()
#     current_user_profile = db_sess.query(User).filter(User.id == Clientid).first()

#     if not current_user_profile:
#         f.abort(404)

#     serch_user = Clientid
#     if form.validate_on_submit():
#         serch_user = form.serch_user_id.data
#         return redirect(url_for(f'/id/{serch_user}'))

#     name = current_user_profile.name

#     html = f.render_template(
#         "post_block.html",
#         ClientId=f'/id/{Clientid}',
#         UserName=name,
#         cntBlocks=3,
#         imgs=[
#             ['../static/img/post_test_1.jpg', '../static/img/post_test_2.jpg', '../static/img/post_test_3.jpg', '../static/img/avatar.jpg'],
#             ['../static/img/post_test_1.jpg', '../static/img/post_test_2.jpg', '../static/img/post_test_3.jpg', '../static/img/avatar.jpg'],
#             ['../static/img/post_test_1.jpg', '../static/img/post_test_2.jpg', '../static/img/post_test_3.jpg', '../static/img/avatar.jpg']
#         ],
#         likesBool=[0, 0, 0],
#         id=['#aa', '#bb', '#cc'],
#         caption=["Описание 1", "Описание 2", "Описание 3"],
#         serch_user=serch_user,
#         form=form
#     )
#     return html



@app.route("/create_chat", methods=["GET", "POST"])
def create_chat():
    if not current_user.is_authenticated:
        return redirect("/")
    form = SerchUserForm()
    if form.validate_on_submit():
        return redirect(f"/id/{form.serch_user_id.data}")
    html = f.render_template(r"create_chat.html", 
                            friends=15,
                            friend_id = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15], 
                            friend_avatar=["../static/img/post_test_3.jpg", "../static/img/post_test_2.jpg", "../static/img/post_test_1.jpg", "../static/img/post_test_2.jpg", "../static/img/post_test_3.jpg", "../static/img/post_test_3.jpg", "../static/img/post_test_2.jpg", "../static/img/post_test_1.jpg", "../static/img/post_test_2.jpg", "../static/img/post_test_3.jpg", "../static/img/post_test_3.jpg", "../static/img/post_test_2.jpg", "../static/img/post_test_1.jpg", "../static/img/post_test_2.jpg", "../static/img/post_test_3.jpg"],
                            friend_name=['ddddd', 'jjjjjjj', 'mmmmmm', 'lllllll', 'ppppppp', 'ddddd', 'jjjjjjj', 'mmmmmm', 'lllllll', 'ppppppp', 'ddddd', 'jjjjjjj', 'mmmmmm', 'lllllll', 'ppppppp'],
                            friend_surname=['ddddd', 'jjjjjjj', 'mmmmmm', 'lllllll', 'ppppppp', 'ddddd', 'jjjjjjj', 'mmmmmm', 'lllllll', 'ppppppp', 'ddddd', 'jjjjjjj', 'mmmmmm', 'lllllll', 'ppppppp'],
                            )
    return html


@app.route("/private_chat/<id>", methods=["GET", "POST"])
def private_chat(id):
    #--------TEST-----------------------#
    class TestChat_participants:
        def __init__(self, name, surname, avatar):
            self.name = name
            self.surname = surname
            self.avatar = avatar

    class TestMessage:
        def __init__(self, text, author, time, is_mine, avatar):
            self.text = text
            self.author = author
            self.time = time
            self.is_mine = is_mine
            self.avatar = avatar
    #--------TEST-----------------------#

    if not current_user.is_authenticated:
        return redirect("/")
    form = SerchUserForm()
    if form.validate_on_submit():
        return redirect(f"/id/{form.serch_user_id.data}")
    html = f.render_template("private_chat.html",
                            chat_avatar='../static/img/post_test_3.jpg',
                            chat_name='Durka',
                            chat_participants = [TestChat_participants("some", "someone", "../static/img/post_test_2.jpg"), TestChat_participants("NotJulia", "NotIvanova", "../static/img/post_test_3.jpg"), TestChat_participants("Julia", "Ivanova", "../static/img/post_test_1.jpg")],
                            messages = [TestMessage("dfhdhfhhfhe", "Julia", "00:02", True, "../static/img/post_test_2.jpg"), TestMessage("dfhdhfhhfhe", "NotJulia", "00:02", False, "../static/img/post_test_1.jpg"), TestMessage("dfhdhfhhfhe", "Julia", "00:02", True, "../static/img/post_test_2.jpg"), TestMessage("dfhdhfhhfhehh\nhhhhhhhhhhhhhh\nhhhhhhhh hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh", "some", "00:02", False, "../static/img/post_test_3.jpg")],
                            form = form,
                            ClientId = f'/id/{current_user.id}',
                            cntRequests=2,
                            friend_request_id=[2, 3],
                            friend_request_avatar=['../static/img/post_test_2.jpg', '../static/img/logo.png'],
                            friend_request_name=['rrrrr', 'hhhhhh'],
                            friend_request_surname=['ggggg', 'jjjjj'],
                            seeFilter = False)
    return html




@app.route("/chat/<id>", methods=["GET", "POST"])
def chat(id):
    #--------TEST-----------------------#
    class TestChat_participants:
        def __init__(self, name, surname, avatar):
            self.name = name
            self.surname = surname
            self.avatar = avatar

    class TestMessage:
        def __init__(self, text, author, time, is_mine, avatar):
            self.text = text
            self.author = author
            self.time = time
            self.is_mine = is_mine
            self.avatar = avatar
    #--------TEST-----------------------#

    if not current_user.is_authenticated:
        return redirect("/")
    form = SerchUserForm()
    if form.validate_on_submit():
        return redirect(f"/id/{form.serch_user_id.data}")
    html = f.render_template("chat.html",
                            messages = [TestMessage("dfhdhfhhfhe", "Julia", "00:02", True, "../static/img/post_test_2.jpg"), TestMessage("dfhdhfhhfhe", "NotJulia", "00:02", False, "../static/img/post_test_1.jpg"), TestMessage("dfhdhfhhfhe", "Julia", "00:02", True, "../static/img/post_test_2.jpg"), TestMessage("dfhdhfhhfhehh\nhhhhhhhhhhhhhh\nhhhhhhhh hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh", "some", "00:02", False, "../static/img/post_test_3.jpg")],
                            form = form,
                            ClientId = f'/id/{current_user.id}',
                            cntRequests=2,
                            friend_request_id=[2, 3],
                            friend_request_avatar=['../static/img/post_test_2.jpg', '../static/img/logo.png'],
                            friend_request_name=['rrrrr', 'hhhhhh'],
                            friend_request_surname=['ggggg', 'jjjjj'],
                            seeFilter = False)
    return html



@app.route("/chats", methods=["GET", "POST"])
def chats():
    if not current_user.is_authenticated:
        return redirect("/")
    form = SerchUserForm()
    if form.validate_on_submit():
        return redirect(f"/id/{form.serch_user_id.data}")
    html = f.render_template(r"chats.html", 
                            form=form,
                            ClientId = f'/id/{current_user.id}', 
                            chats=2,
                            chat_avatar=["../static/img/post_test_3.jpg", "../static/img/post_test_2.jpg"],
                            chat_name = ['tttt', 'nnnnnn'],
                            chat_id=['1', '2'],
                            is_block = [True, False],
                            cntRequests=2,
                            friend_request_id=[2, 3],
                            friend_request_avatar=['../static/img/post_test_2.jpg', '../static/img/logo.png'],
                            friend_request_name=['rrrrr', 'hhhhhh'],
                            friend_request_surname=['ggggg', 'jjjjj'],
                            seeFilter = False)
    return html

@app.route("/settings", methods=["GET", "POST"])
def settings():
    if not current_user.is_authenticated:
        return redirect("/")
    form2 = SettingsForm()
    form = SerchUserForm()
    if form.validate_on_submit() and form.serch_user_id.data:
        return redirect(f"/id/{form.serch_user_id.data}")
    name = "Юля"
    surname = "Иванова"
    age = 15
    if request.method == "GET":
        # Получаем данные пользователя из базы данных
        # user = get_user_from_db(current_user.id)
        form2.name.data = name
        form2.surname.data = surname
        form2.age.data = age
        form2.client_id.data = current_user.id

        return render_template(
            "setings.html",
            form=form,
            ClientId=f"/id/{current_user.id}",
            form2=form2,
            cntRequests=0,
            friend_request_id=[],
            friend_request_avatar=[],
            friend_request_name=[],
            friend_request_surname=[],
            seeFilter = False
        )

    if form2.validate_on_submit():
        try:
            # Обработка файлов
            if form2.avatar.data:
                filename = save_file(form2.avatar.data, "avatars")
                # user.avatar = filename

            if form2.background.data:
                filename = save_file(form2.background.data, "backgrounds")
                # user.background = filename

            # Обновление данных пользователя в базе
            # update_user_in_db(
            #     user_id=current_user.id,
            #     name=form.name.data,
            #     surname=form.surname.data,
            #     age=form.age.data,
            #     avatar=filename if form.avatar.data else user.avatar,
            #     background=filename if form.background.data else user.background
            # )

            flash("Настройки успешно сохранены", "success")
            return redirect(url_for("profile"))

        except Exception as e:
            print(e)
            flash(f"Ошибка при сохранении: {str(e)}", "danger")
            return redirect(url_for("settings"))
    print("k")
    return render_template(
        "setings.html",
        form=form,
        ClientId=f"/id/{current_user.id}",
        serch_user=None,
        form2=form2,
        cntRequests=0,
        friend_request_id=[],
        friend_request_avatar=[],
        friend_request_name=[],
        friend_request_surname=[],
        seeFilter = False
    )


def save_file(file, folder):
    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config["UPLOAD_FOLDER"], folder, filename)
        file.save(file_path)
        return filename
    return None


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html", ClientId=current_user.id), 404


if __name__ == "__main__":
    app.run(port=8080, host="127.0.0.1")
