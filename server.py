import flask as f
from flask import render_template, request, redirect, flash, url_for, jsonify
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
from data.private_chats import PrivateChat
from forms.create_post_form import CreatePostForm
from forms.registr_form import *
from forms.serch_user import SerchUserForm
from forms.edit_post_form import EditPostForm

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
    if form.validate_on_submit() and form.serch_user_id.data:
        return redirect(f"/id/{form.serch_user_id.data}")
    html = f.render_template(r"create_chat.html", 
                            friends=15,
                            friend_id = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15], 
                            friend_avatar=["../static/img/post_test_3.jpg", "../static/img/post_test_2.jpg", "../static/img/post_test_1.jpg", "../static/img/post_test_2.jpg", "../static/img/post_test_3.jpg", "../static/img/post_test_3.jpg", "../static/img/post_test_2.jpg", "../static/img/post_test_1.jpg", "../static/img/post_test_2.jpg", "../static/img/post_test_3.jpg", "../static/img/post_test_3.jpg", "../static/img/post_test_2.jpg", "../static/img/post_test_1.jpg", "../static/img/post_test_2.jpg", "../static/img/post_test_3.jpg"],
                            friend_name=['ddddd', 'jjjjjjj', 'mmmmmm', 'lllllll', 'ppppppp', 'ddddd', 'jjjjjjj', 'mmmmmm', 'lllllll', 'ppppppp', 'ddddd', 'jjjjjjj', 'mmmmmm', 'lllllll', 'ppppppp'],
                            friend_surname=['ddddd', 'jjjjjjj', 'mmmmmm', 'lllllll', 'ppppppp', 'ddddd', 'jjjjjjj', 'mmmmmm', 'lllllll', 'ppppppp', 'ddddd', 'jjjjjjj', 'mmmmmm', 'lllllll', 'ppppppp'],
                            )
    return html


@app.route("/edit_private_chat/<chat_id>", methods=["GET", "POST"])
def edit_chat(chat_id):
    if not current_user.is_authenticated:
        return redirect("/")
    form = SerchUserForm()
    if form.validate_on_submit() and form.serch_user_id.data:
        return redirect(f"/id/{form.serch_user_id.data}")
    html = f.render_template(r"create_chat.html", 
                            friends=15,
                            friend_id = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15], 
                            friend_avatar=["../static/img/post_test_3.jpg", "../static/img/post_test_2.jpg", "../static/img/post_test_1.jpg", "../static/img/post_test_2.jpg", "../static/img/post_test_3.jpg", "../static/img/post_test_3.jpg", "../static/img/post_test_2.jpg", "../static/img/post_test_1.jpg", "../static/img/post_test_2.jpg", "../static/img/post_test_3.jpg", "../static/img/post_test_3.jpg", "../static/img/post_test_2.jpg", "../static/img/post_test_1.jpg", "../static/img/post_test_2.jpg", "../static/img/post_test_3.jpg"],
                            friend_name=['ddddd', 'jjjjjjj', 'mmmmmm', 'lllllll', 'ppppppp', 'ddddd', 'jjjjjjj', 'mmmmmm', 'lllllll', 'ppppppp', 'ddddd', 'jjjjjjj', 'mmmmmm', 'lllllll', 'ppppppp'],
                            friend_surname=['ddddd', 'jjjjjjj', 'mmmmmm', 'lllllll', 'ppppppp', 'ddddd', 'jjjjjjj', 'mmmmmm', 'lllllll', 'ppppppp', 'ddddd', 'jjjjjjj', 'mmmmmm', 'lllllll', 'ppppppp'],
                            members = 5,
                            selectedFriendAvatar = ["../static/img/post_test_3.jpg", "../static/img/post_test_2.jpg", "../static/img/post_test_1.jpg", "../static/img/post_test_2.jpg", "../static/img/post_test_3.jpg"],
                            selectedFriendName = ['ddddd', 'jjjjjjj', 'mmmmmm', 'lllllll', 'ppppppp'],
                            selected_friend_id = [1, 2, 3, 4, 5],
                            chat_avatar = "../static/img/post_test_3.jpg",
                            chat_name = "Durka"
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
                             chat_id = int(id),
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


@app.route('/edit_post/<post_id>', methods=['POST', 'GET'])
def edit_post(post_id):
    if not current_user.is_authenticated:
        return redirect("/")
    form = SerchUserForm()
    if form.validate_on_submit() and form.serch_user_id.data:
        return redirect(f"/id/{form.serch_user_id.data}")
    form1 = EditPostForm()
    if request.method == "GET":
        # Здесь нужно описать то как данные о посте достаются из бд
        post_id = int(post_id)
        caption = "Описание 1"
        form1.caption.data = caption

        return render_template("edit_post.html", createPostForm=form1, post_id=post_id, form=form,
                            ClientId = f'/id/{current_user.id}',
                             cntRequests=2,
                            friend_request_id=[2, 3],
                            friend_request_avatar=['../static/img/post_test_2.jpg', '../static/img/logo.png'],
                            friend_request_name=['rrrrr', 'hhhhhh'],
                            friend_request_surname=['ggggg', 'jjjjj'],
                            seeFilter = False )
    elif request.method == "POST":
        if form1.validate_on_submit():
            #нужно внести изменения в БД
            print(form1.caption.data)
            return redirect("/main")

#!!!ВАЖНЫЙ КОМЕНТ: все с блоки с пометкой TEST написаны лишь для проверки и не являются полноценными, однако могут помочь в разработке в дальнейшем
#--------------TEST---------------------------
from flask import request, jsonify

@app.route('/api/like', methods=['POST'])
def test1():
    try:
        data = request.get_json()
        
        # Проверяем наличие всех необходимых полей
        required_fields = ['postId', 'userId', 'likesCount']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing required fields'}), 400

        # Получаем данные
        post_id = data['postId']
        user_id = data['userId']
        likes_count = data['likesCount']

        # Здесь вы можете обработать данные (сохранить в БД и т.д.)
        print(f"Получен лайк: Пост {post_id}, Пользователь {user_id}, Лайков: {likes_count}")

        # Возвращаем успешный ответ
        return jsonify({
            'status': 'success',
            'message': 'Like processed',
            'postId': post_id,
            'newLikesCount': likes_count
        }), 200

    except Exception as e:
        print(f"Ошибка при обработке лайка: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

#ВНИМАНИЕ!!!: данная функция пока работает некоректно (однако моей задачей в данный момент было имено отправить данные) картинка отправляется, чтобы её прочитать используйте read()
import os
from werkzeug.utils import secure_filename
from flask import request, jsonify
import time
import uuid
import re
# Конфигурация
UPLOAD_FOLDER = 'static\chat_avatars'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_numbers(text):
    numbers = re.findall(r'"(\d+)"', text)
    return ','.join(numbers)

@app.route('/api/chats/create', methods=['POST'])
def test2():
    try:
        avatar_filename = None
        if 'avatar_file' in request.files:
            file = request.files['avatar_file']

            
            if file.content_length > 2 * 1024 * 1024: 
                return jsonify({'error': 'Файл слишком большой (макс. 2MB)'}), 400

           
            if not allowed_file(file.filename):
                return jsonify({'error': 'Недопустимый тип файла'}), 400
            

            filename = secure_filename(file.filename)
            avatar_filename = f"avatar_{str(uuid.uuid4())}_{filename}"
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], avatar_filename))
     
        chat_name = request.form.get('chatName')
        friends = request.form.get('friends')
        print(extract_numbers(friends))
        if not chat_name or not friends:
            return jsonify({'error': 'Не хватает данных'}), 400

        db_sess = db_session.create_session()
        chat = PrivateChat(
            members=extract_numbers(friends),
            chat_name=chat_name,
            chat_avatar=avatar_filename,
        )
        
        db_sess.add(chat)
        db_sess.commit()
        
        return jsonify({
            'status': 'success',
        })

    except Exception as e:
        print(f"\n!!! Ошибка: {str(e)}")
        return jsonify({'error': 'Внутренняя ошибка сервера'}), 500
    

@app.route('/api/chats/edit/<id>', methods=['POST'])
def test3(id):
    try:
        file = None
        if 'avatar_file' in request.files:
            file = request.files['avatar_file']
            print(file.read(100))
        chat_name = request.form.get('chatName')
        friends = request.form.get('friends')
        print(file, chat_name, friends)
        return jsonify({
                'status': 'success',
                'chatId': 123,
        })
    except Exception as e:
        print(f"\n!!! Ошибка: {str(e)}")
        return jsonify({'error': 'Внутренняя ошибка сервера'}), 500
    # try:
    #     file = None
    #     if 'avatar_file' in request.files:
    #         file = request.files['avatar_file']
    #         print(file.read(100))
    #         # Проверяем размер файла
    #         if file.content_length > 2 * 1024 * 1024:  # 2MB
    #             return jsonify({'error': 'Файл слишком большой (макс. 2MB)'}), 400

    #         # Проверяем расширение
    #         if not allowed_file(file.filename):
    #             return jsonify({'error': 'Недопустимый тип файла'}), 400
    #         # Типо дальше сохранение но пусть это кто-нибудь сделает (ну или я но потом)

    #     # Получаем остальные данные
    #     chat_name = request.form.get('chatName')
    #     friends = request.form.get('friends')
        
    #     if not chat_name or not friends:
    #         return jsonify({'error': 'Не хватает данных'}), 400

    #     # Здесь должна быть ваша логика создания чата в БД
    #     # ...
        
    #     return jsonify({
    #         'status': 'success',
    #         'chatId': 123,
    #     })

    # except Exception as e:
    #     print(f"\n!!! Ошибка: {str(e)}")
    #     return jsonify({'error': 'Внутренняя ошибка сервера'}), 500



@app.route('/api/send-message', methods=['POST'])
def test4():
    try:
        print(request)
        data = request.get_json()
        print(data)
        text = data['text']
        type = data['type']
        chatID = data['chatID']
        print(text, type, chatID)
        db_sess = db_session.create_session()
        coment = Comments(
            chat_id=chatID,
            text=text,
            sender = current_user.id,
            type=type,
        )
        
        db_sess.add(coment)
        db_sess.commit()
        return jsonify({
                'status': 'success',
        })
    except Exception as e:
        print(f"\n!!! Ошибка: {str(e)}")
        return jsonify({'error': 'Внутренняя ошибка сервера'}), 500
    
#--------------TEST---------------------------



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
