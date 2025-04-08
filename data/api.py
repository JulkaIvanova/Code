from flask_restful import Resource, reqparse, abort
from flask import jsonify, request
from . import db_session
from .users import User
from .posts import Posts
from .chats import Chat
from .comments import Comments
from .private_chats import PrivateChat
import os
from werkzeug.utils import secure_filename
import uuid
import re
from flask_login import current_user

class CheckLoginResource(Resource):
    def post(self):
        # Проверка авторизации
        if not current_user.is_authenticated:
            return {"error": "Требуется авторизация"}, 401
        
        # current_user теперь доступен
        print(f"User ID: {current_user.id}, Name: {current_user.name}")
        return {"status": "success"}

# Общие функции
def allowed_file(filename, allowed_extensions={'png', 'jpg', 'jpeg', 'gif'}):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

def extract_numbers(text):
    numbers = re.findall(r'"(\d+)"', text)
    return ','.join(numbers)

# Парсеры для запросов
like_parser = reqparse.RequestParser()
like_parser.add_argument('postId', required=True)
like_parser.add_argument('userId', required=True)
like_parser.add_argument('likesCount', required=True)

message_parser = reqparse.RequestParser()
message_parser.add_argument('text', required=True)
message_parser.add_argument('type', required=True)
message_parser.add_argument('chatID', required=True)

# Ресурсы API
class LikeResource(Resource):
    def post(self):
        print("hhhh")
        args = like_parser.parse_args()
        try:
            print(f"Получен лайк: Пост {args['postId']}, Пользователь {args['userId']}, Лайков: {args['likesCount']}")
            return jsonify({
                'status': 'success',
                'message': 'Like processed',
                'postId': args['postId'],
                'newLikesCount': args['likesCount']
            })
        except Exception as e:
            print(f"Ошибка при обработке лайка: {str(e)}")
            abort(500, message="Internal server error")

class ChatResource(Resource):
    def __init__(self):
        self.upload_folder = 'static\chat_avatars'
        self.max_size = 2 * 1024 * 1024  # 2MB

    def post(self):
        try:
            db_sess = db_session.create_session()
            
            # Обработка файла
            avatar_filename = None
            if 'avatar_file' in request.files:
                file = request.files['avatar_file']
                
                if file.content_length > self.max_size:
                    abort(400, message="Файл слишком большой (макс. 2MB)")
                
                if not allowed_file(file.filename):
                    abort(400, message="Недопустимый тип файла")
                
                filename = secure_filename(file.filename)
                avatar_filename = f"avatar_{uuid.uuid4()}_{filename}"
                file.save(os.path.join(self.upload_folder, avatar_filename))
                avatar_filename = f"..\{self.upload_folder}\{avatar_filename}"

            # Обработка данных формы
            chat_name = request.form.get('chatName')
            friends = request.form.get('friends')
            
            if not chat_name or not friends:
                abort(400, message="Не хватает данных")

            # Создание чата
            chat = PrivateChat(
                members=f"{extract_numbers(friends)},{current_user.id}",
                chat_name=chat_name,
                chat_avatar=avatar_filename,
            )
            
            db_sess.add(chat)
            db_sess.commit()
            
            return jsonify({'status': 'success'})

        except Exception as e:
            print(f"Ошибка: {str(e)}")
            abort(500, message="Внутренняя ошибка сервера")

    def put(self, chat_id):
        try:
            db_sess = db_session.create_session()
            chat = db_sess.query(PrivateChat).get(chat_id)
            
            if not chat:
                abort(404, message="Чат не найден")

            # Обработка файла
            avatar_filename = None
            if 'avatar_file' in request.files:
                file = request.files['avatar_file']
                
                if file.content_length > self.max_size:
                    abort(400, message="Файл слишком большой (макс. 2MB)")
                
                if not allowed_file(file.filename):
                    abort(400, message="Недопустимый тип файла")
                
                filename = secure_filename(file.filename)
                avatar_filename = f"avatar_{uuid.uuid4()}_{filename}"
                file.save(os.path.join(self.upload_folder, avatar_filename))
                avatar_filename = f"..\{self.upload_folder}\{avatar_filename}"

            # Обновление данных чата
            chat_name = request.form.get('chatName')
            friends = request.form.get('friends')
            
            if chat_name:
                chat.chat_name = chat_name
            if friends:
                chat.members = f"{extract_numbers(friends)},{current_user.id}"
            if avatar_filename:
                chat.chat_avatar = avatar_filename
            
            db_sess.commit()
            return jsonify({'status': 'success'})

        except Exception as e:
            print(f"Ошибка: {str(e)}")
            abort(500, message="Внутренняя ошибка сервера")

class MessageResource(Resource):
    def post(self):
        args = message_parser.parse_args()
        try:
            db_sess = db_session.create_session()
            
            # Создание сообщения
            comment = Comments(
                chat_id=args['chatID'],
                text=args['text'],
                sender=current_user.id,
                type=args['type'],
            )
            db_sess.add(comment)
            db_sess.commit()
            
            # Обновление чата
            chat = db_sess.query(PrivateChat).get(args['chatID'])
            if chat:
                chat.comments = f"{chat.comments},{comment.id}" if chat.comments else str(comment.id)
                db_sess.commit()
            
            # Обновление пользователя
            user = db_sess.query(User).get(current_user.id)
            if user:
                user.comment_ids = f"{user.comment_ids},{comment.id}" if user.comment_ids else str(comment.id)
                db_sess.commit()
            
            avatar = rf"..\static\img\avatar.jpg"
            if current_user.img_avatar:
                avatar = current_user.img_avatar
                
            return jsonify({
                'time': str(comment.send_date).split(".")[0],
                'messageText': comment.text,
                'name': current_user.name,
                'avatar': avatar
            })
            
        except Exception as e:
            print(f"Ошибка: {str(e)}")
            abort(500, message="Внутренняя ошибка сервера")
        finally:
            db_sess.close()

# Инициализация API
def init_api(api):
    api.add_resource(LikeResource, '/api/like')
    api.add_resource(ChatResource, '/api/chats/create', '/api/chats/edit/<int:chat_id>')
    api.add_resource(MessageResource, '/api/send-message')