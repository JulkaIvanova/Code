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
from data.api import*
from flask_restful import Api



app = f.Flask(__name__)
db_session.global_init("db/Code.db")
app.config["SECRET_KEY"] = "code_secret_key"
app.config["UPLOAD_FOLDER"] = os.path.join(app.root_path, "static/uploads")
app.config["ALLOWED_EXTENSIONS"] = {"png", "jpg", "jpeg", "gif"}
api = Api(app)
init_api(api)

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
    db_sess = db_session.create_session()
    friends = []
    print(current_user.friends_ids)
    if current_user.friends_ids:
        for i in str(current_user.friends_ids).split(","):
            friends.append(db_sess.query(User).filter(User.id == int(i)).first())
    html = f.render_template(r"create_chat.html", friends=friends)
    return html
    


@app.route("/edit_private_chat/<chat_id>", methods=["GET", "POST"])
def edit_chat(chat_id):
    if not current_user.is_authenticated:
        return redirect("/")
    form = SerchUserForm()
    if form.validate_on_submit() and form.serch_user_id.data:
        return redirect(f"/id/{form.serch_user_id.data}")
    db_sess = db_session.create_session()
    private_chat = db_sess.query(PrivateChat).filter(PrivateChat.id == chat_id).first()
    if not private_chat:
        return f.abort(404)
    members = private_chat.members.split(",")
    if str(current_user.id) not in members:
        return f.abort(404)
    friends = []
    print(current_user.friends_ids)
    if current_user.friends_ids:
        for i in str(current_user.friends_ids).split(","):
            friends.append(db_sess.query(User).filter(User.id == int(i)).first())
    chat = db_sess.query(PrivateChat).filter(PrivateChat.id == int(chat_id)).first()
    members_id = str(chat.members).split(",")
    members = []
    for i in members_id:
        if int(i) == current_user.id:
            continue
        members.append(db_sess.query(User).filter(User.id == int(i)).first())
    chat_avatar = rf"..\static\img\chat.png"
    if private_chat.chat_avatar:
        chat_avatar = private_chat.chat_avatar
    html = f.render_template(r"create_chat.html", 
                            friends = friends,
                            members = members,
                            chat_avatar = chat_avatar,
                            chat_name = chat.chat_name
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
    #--------TEST-----------------------#

    class Message:
        def __init__(self, text, author, time, is_mine, avatar):
            self.text = text
            self.author = author
            self.time = time
            self.is_mine = is_mine
            self.avatar = avatar

    db_sess = db_session.create_session()
    private_chat = db_sess.query(PrivateChat).filter(PrivateChat.id == id).first()
    if not private_chat:
        return f.abort(404)
    if not current_user.is_authenticated:
        return redirect("/")
    form = SerchUserForm()
    if form.validate_on_submit():
        return redirect(f"/id/{form.serch_user_id.data}")
    members = private_chat.members.split(",")
    if str(current_user.id) not in members:
        return f.abort(404)
    users = []
    for i in members:
        users.append(db_sess.query(User).filter(User.id == int(i)).first())
    print(users)
    messages = []
    if private_chat.comments:
        message_id = private_chat.comments.split(",")
        for i in message_id:
            message = db_sess.query(Comments).filter(Comments.id == int(i)).first()
            user = db_sess.query(User).filter(User.id == message.sender).first()
            messages.append(Message(message.text, user.name, str(message.send_date).split(".")[0], message.sender == current_user.id, user.img_avatar))
    chat_avatar = rf"..\static\img\chat.png"
    if private_chat.chat_avatar:
        chat_avatar = private_chat.chat_avatar
    html = f.render_template("private_chat.html",
                             chat_id = int(id),
                            chat_avatar=chat_avatar,
                            chat_name=private_chat.chat_name,
                            chat_participants = users,
                            messages = messages,
                            form = form,
                            ClientId = f'/id/{current_user.id}',
                            cntRequests=2,
                            friend_request_id=[2, 3],
                            friend_request_avatar=['../static/img/post_test_2.jpg', '../static/img/logo.png'],
                            friend_request_name=['rrrrr', 'hhhhhh'],
                            friend_request_surname=['ggggg', 'jjjjj'],
                            seeFilter = False)
    
    # html = f.render_template("private_chat.html",
    #                          chat_id = int(id),
    #                         chat_avatar='../static/img/post_test_3.jpg',
    #                         chat_name='Durka',
    #                         chat_participants = [TestChat_participants("some", "someone", "../static/img/post_test_2.jpg"), TestChat_participants("NotJulia", "NotIvanova", "../static/img/post_test_3.jpg"), TestChat_participants("Julia", "Ivanova", "../static/img/post_test_1.jpg")],
    #                         messages = [Message("dfhdhfhhfhe", "Julia", "00:02", True, "../static/img/post_test_2.jpg"), Message("dfhdhfhhfhe", "NotJulia", "00:02", False, "../static/img/post_test_1.jpg"), Message("dfhdhfhhfhe", "Julia", "00:02", True, "../static/img/post_test_2.jpg"), Message("dfhdhfhhfhehh\nhhhhhhhhhhhhhh\nhhhhhhhh hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh", "some", "00:02", False, "../static/img/post_test_3.jpg")],
    #                         form = form,
    #                         ClientId = f'/id/{current_user.id}',
    #                         cntRequests=2,
    #                         friend_request_id=[2, 3],
    #                         friend_request_avatar=['../static/img/post_test_2.jpg', '../static/img/logo.png'],
    #                         friend_request_name=['rrrrr', 'hhhhhh'],
    #                         friend_request_surname=['ggggg', 'jjjjj'],
    #                         seeFilter = False)
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
# from flask import request, jsonify

# @app.route('/api/like', methods=['POST'])
# def test1():
#     try:
#         data = request.get_json()
        
#         # Проверяем наличие всех необходимых полей
#         required_fields = ['postId', 'userId', 'likesCount']
#         if not all(field in data for field in required_fields):
#             return jsonify({'error': 'Missing required fields'}), 400

#         # Получаем данные
#         post_id = data['postId']
#         user_id = data['userId']
#         likes_count = data['likesCount']

#         # Здесь вы можете обработать данные (сохранить в БД и т.д.)
#         print(f"Получен лайк: Пост {post_id}, Пользователь {user_id}, Лайков: {likes_count}")

#         # Возвращаем успешный ответ
#         return jsonify({
#             'status': 'success',
#             'message': 'Like processed',
#             'postId': post_id,
#             'newLikesCount': likes_count
#         }), 200

#     except Exception as e:
#         print(f"Ошибка при обработке лайка: {str(e)}")
#         return jsonify({'error': 'Internal server error'}), 500

# #ВНИМАНИЕ!!!: данная функция пока работает некоректно (однако моей задачей в данный момент было имено отправить данные) картинка отправляется, чтобы её прочитать используйте read()
# import os
# from werkzeug.utils import secure_filename
# from flask import request, jsonify
# import time
# import uuid
# import re
# # Конфигурация
# UPLOAD_FOLDER = 'static\chat_avatars'
# ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# def allowed_file(filename):
#     return '.' in filename and \
#            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# def extract_numbers(text):
#     numbers = re.findall(r'"(\d+)"', text)
#     return ','.join(numbers)

# @app.route('/api/chats/create', methods=['POST'])
# def test2():
#     try:
#         avatar_filename = None
#         if 'avatar_file' in request.files:
#             file = request.files['avatar_file']

            
#             if file.content_length > 2 * 1024 * 1024: 
#                 return jsonify({'error': 'Файл слишком большой (макс. 2MB)'}), 400

           
#             if not allowed_file(file.filename):
#                 return jsonify({'error': 'Недопустимый тип файла'}), 400
            

#             filename = secure_filename(file.filename)
#             avatar_filename = f"avatar_{str(uuid.uuid4())}_{filename}"
#             file.save(os.path.join(app.config['UPLOAD_FOLDER'], avatar_filename))
#             avatar_filename = rf"..\{UPLOAD_FOLDER}\{avatar_filename}"

#         chat_name = request.form.get('chatName')
#         friends = request.form.get('friends')
#         print(extract_numbers(friends))
#         if not chat_name or not friends:
#             return jsonify({'error': 'Не хватает данных'}), 400

#         db_sess = db_session.create_session()
#         chat = PrivateChat(
#             members=extract_numbers(friends)+f",{current_user.id}",
#             chat_name=chat_name,
#             chat_avatar=avatar_filename,
#         )
        
#         db_sess.add(chat)
#         db_sess.commit()
        
#         return jsonify({
#             'status': 'success',
#         })

#     except Exception as e:
#         print(f"\n!!! Ошибка: {str(e)}")
#         return jsonify({'error': 'Внутренняя ошибка сервера'}), 500
    

# @app.route('/api/chats/edit/<id>', methods=['POST'])
# def test3(id):
#     try:
#         avatar_filename = None
#         if 'avatar_file' in request.files:
#             file = request.files['avatar_file']

            
#             if file.content_length > 2 * 1024 * 1024: 
#                 return jsonify({'error': 'Файл слишком большой (макс. 2MB)'}), 400

           
#             if not allowed_file(file.filename):
#                 return jsonify({'error': 'Недопустимый тип файла'}), 400
            

#             filename = secure_filename(file.filename)
#             avatar_filename = f"avatar_{str(uuid.uuid4())}_{filename}"
#             file.save(os.path.join(app.config['UPLOAD_FOLDER'], avatar_filename))
#             avatar_filename = rf"..\{UPLOAD_FOLDER}\{avatar_filename}"
#             print(avatar_filename)

#         chat_name = request.form.get('chatName')
#         friends = request.form.get('friends')
#         # print(file, chat_name, friends)

#         db_sess = db_session.create_session()
#         chat = db_sess.query(PrivateChat).filter(PrivateChat.id == int(id)).first()
#         chat.members=extract_numbers(friends)+f",{current_user.id}"
#         chat.chat_name=chat_name
#         if avatar_filename:
#             chat.chat_avatar=avatar_filename
        
        
#         db_sess.add(chat)
#         db_sess.commit()

#         return jsonify({
#             'status': 'success',
#         })
    
#     except Exception as e:
#         print(f"\n!!! Ошибка: {str(e)}")
#         return jsonify({'error': 'Внутренняя ошибка сервера'}), 500

# @app.route('/api/send-message', methods=['POST'])
# def test4():
#     try:
#         data = request.get_json()
#         text = data['text']
#         type = data['type']
#         chatID = data['chatID']
        
#         db_sess = db_session.create_session()
        
#         # Создаем и добавляем комментарий
#         coment = Comments(
#             chat_id=chatID,
#             text=text,
#             sender=current_user.id,
#             type=type,
#         )
#         db_sess.add(coment)
#         db_sess.commit()  # Фиксируем, чтобы получить ID комментария
        
#         # Обновляем чат, добавляя ID комментария
#         chat = db_sess.query(PrivateChat).filter(PrivateChat.id == chatID).first()
#         if chat:
#             if chat.comments is None:
#                 chat.comments = str(coment.id)
#             else:
#                 comments_list = chat.comments.split(",")
#                 comments_list.append(str(coment.id))
#                 chat.comments = ",".join(comments_list)
            
#             db_sess.commit()
#         user = db_sess.query(User).filter(User.id == current_user.id).first()
#         if user:
#             if user.comment_ids is None:
#                 user.comment_ids = str(coment.id)
#             else:
#                 user_comments_list = user.comment_ids.split(",")
#                 user_comments_list.append(str(coment.id))
#                 user.comment_ids = ",".join(user_comments_list)
#             db_sess.commit()
#         avatar = "../static/img/avatar.jpg"
#         if current_user.img_avatar:
#             avatar = current_user.img_avatar
#         return jsonify({
#             'time': str(coment.send_date).split(".")[0],
#             'messageText': coment.text,
#             'name': current_user.name,
#             'avatar': avatar 
#         })
#     except Exception as e:
#         print(f"\n!!! Ошибка: {str(e)}")
#         return jsonify({'error': 'Внутренняя ошибка сервера'}), 500
#     finally:
#         db_sess.close()
    
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
