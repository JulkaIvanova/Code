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
from sqlalchemy import and_, func, or_ 


def allowed_file(filename, allowed_extensions={'png', 'jpg', 'jpeg', 'gif', 'webp'}):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions


def extract_numbers(text):
    numbers = re.findall(r'"(\d+)"', text)
    return ','.join(numbers)


like_parser = reqparse.RequestParser()
like_parser.add_argument('postId', required=True)
like_parser.add_argument('userId', required=True)
like_parser.add_argument('likesCount', required=True)

message_parser = reqparse.RequestParser()
message_parser.add_argument('text', required=True)
message_parser.add_argument('type', required=True)
message_parser.add_argument('chatID', required=True)


class LikeResource(Resource):
    def post(self):
        if not current_user.is_authenticated:
            return {"error": "Требуется авторизация"}, 401
        args = like_parser.parse_args()
        db_sess = db_session.create_session()
        try:
            post_id = args['postId'][5:]
            user_id = args['userId']
            post_category = db_sess.query(Posts).get(post_id).category
            user = db_sess.query(User).get(user_id)
            post_likes = db_sess.query(Posts).get(post_id).likes_user_id
            user_likes = user.post_like_ids
            post_likes_count = db_sess.query(Posts).get(post_id).likes

            if user_likes is not None or user_likes == "":
                user_likes = user_likes.split(',')

                if post_id not in user_likes:
                    user_likes.append(post_id)
                user_likes = ','.join(user_likes)
            else:
                user_likes = post_id

            if post_category == 'all':
                user_likes_common = user.post_like_common_category_ids
                if user_likes_common:
                    user_likes_common = user_likes_common.split(',')
                    user_likes_common.append(post_id)
                    user_likes_common = ','.join(user_likes_common)
                else:
                    user_likes_common = post_id
                user.post_like_common_category_ids = user_likes_common


            elif post_category == 'guide':
                user_likes_guide = user.post_like_guide_category_ids
                if user_likes_guide:
                    user_likes_guide = user_likes_guide.split(',')
                    user_likes_guide.append(post_id)
                    user_likes_guide = ','.join(user_likes_guide)
                else:
                    user_likes_guide = post_id
                user.post_like_guide_category_ids = user_likes_guide

            elif post_category == 'ideas':
                user_likes_ideas = user.post_like_ideas_category_ids
                if user_likes_ideas:
                    user_likes_ideas = user_likes_ideas.split(',')
                    user_likes_ideas.append(post_id)
                    user_likes_ideas = ','.join(user_likes_ideas)
                else:
                    user_likes_ideas = post_id
                user.post_like_ideas_category_ids = user_likes_ideas

            elif post_category == 'mems':
                user_likes_mems = user.post_like_mems_category_ids
                if user_likes_mems:
                    user_likes_mems = user_likes_mems.split(',')
                    user_likes_mems.append(post_id)
                    user_likes_mems = ','.join(user_likes_mems)
                else:
                    user_likes_mems = post_id
                user.post_like_mems_category_ids = user_likes_mems

            if post_likes:
                post_likes = post_likes.split(',')
                if user_id not in post_likes:
                    post_likes.append(user_id)
                    post_likes_count = str(int(post_likes_count) + 1)
                    db_sess.query(Posts).get(post_id).likes = post_likes_count
                post_likes = ','.join(post_likes)
            else:
                post_likes = user_id
                post_likes_count = str(int(post_likes_count) + 1)
                db_sess.query(Posts).get(post_id).likes = post_likes_count
            db_sess.query(Posts).get(post_id).likes_user_id = post_likes
            user.post_like_ids = user_likes

            db_sess.commit()
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
        self.max_size = 2 * 1024 * 1024

    def post(self):
        if not current_user.is_authenticated:
            return {"error": "Требуется авторизация"}, 401
        try:
            db_sess = db_session.create_session()

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

            chat_name = request.form.get('chatName')
            friends = request.form.get('friends')

            if not chat_name or not friends:
                abort(400, message="Не хватает данных")

            chat = PrivateChat(
                members=f"{extract_numbers(friends)},{current_user.id}",
                chat_name=chat_name,
                chat_avatar=avatar_filename,
            )

            db_sess.add(chat)
            db_sess.commit()

            for i in chat.members.split(","):
                user = db_sess.query(User).get(int(i))
                user.private_chat_ids = f"{user.private_chat_ids},{chat.id}" if user.private_chat_ids else str(chat.id)
                db_sess.add(user)
                db_sess.commit()

            return jsonify({'status': 'success'})

        except Exception as e:
            print(f"Ошибка: {str(e)}")
            abort(500, message="Внутренняя ошибка сервера")

    def put(self, chat_id):
        if not current_user.is_authenticated:
            return {"error": "Требуется авторизация"}, 401
        try:
            db_sess = db_session.create_session()
            chat = db_sess.query(PrivateChat).get(chat_id)

            if not chat:
                abort(404, message="Чат не найден")

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

            chat_name = request.form.get('chatName')
            friends = request.form.get('friends')
            members = f"{extract_numbers(friends)},{current_user.id}"
            members = members.split(",")
            old_members = chat.members.split(",") if chat.members else []
            if set(old_members) != set(members):
                if len(old_members) > len(members):
                    delete_members = list(set(old_members) - set(members))
                    for i in delete_members:
                        user = db_sess.query(User).get(int(i))
                        if user.private_chat_ids:
                            chats = user.private_chat_ids.split(",")
                            chats.remove(str(chat_id))
                            user.private_chat_ids = ",".join(chats)
                elif len(members) > len(old_members):
                    add_friends = list(set(members) - set(old_members))
                    for i in add_friends:
                        user = db_sess.query(User).get(int(i))
                        user.private_chat_ids = f"{user.private_chat_ids},{chat_id}" if user.private_chat_ids else str(chat_id)
                        
            if chat_name:
                chat.chat_name = chat_name
            if friends:
                chat.members = ",".join(members)
            if avatar_filename:
                chat.chat_avatar = avatar_filename

            db_sess.commit()
            return jsonify({'status': 'success'})

        except Exception as e:
            print(f"Ошибка: {str(e)}")
            abort(500, message="Внутренняя ошибка сервера")

    def delete(self, chat_id):
        if not current_user.is_authenticated:
            return {"error": "Требуется авторизация"}, 401
        try:
            session = db_session.create_session()
            chat = session.query(PrivateChat).get(chat_id)
            if not chat or chat.private_chat_with_friend:
                return {'status': 'error', 'message': 'Чат не найден'}, 404
            members = chat.members.split(",")
            if str(current_user.id) not in members:
                return {'status': 'error', 'message': 'Чат не найден'}, 404
            if members:
                members.remove(str(current_user.id))
            if len(members) < 2:
                session.delete(chat)
                session.commit()
                members.append(str(current_user.id))
                for i in members:
                    user = session.query(User).get(int(i))
                    if user.private_chat_ids:
                        chats = user.private_chat_ids.split(",")
                        chats.remove(str(chat_id))
                        user.private_chat_ids = ",".join(chats)
                session.commit()
                return jsonify({'status': 'success'})
            user = session.query(User).get(int(current_user.id))
            if user.private_chat_ids:
                chats = user.private_chat_ids.split(",")
                chats.remove(str(chat_id))
                user.private_chat_ids = ",".join(chats)
            chat.members = ",".join(members)
            session.commit()
            return jsonify({'status': 'success'})
        except Exception as e:
            print(f"Ошибка: {str(e)}")
            abort(500, message="Внутренняя ошибка сервера")


class MessageResource(Resource):
    def post(self):
        if not current_user.is_authenticated:
            return {"error": "Требуется авторизация"}, 401
        args = message_parser.parse_args()
        try:
            db_sess = db_session.create_session()

            comment = Comments(
                chat_id=args['chatID'],
                text=args['text'],
                sender=current_user.id,
                type=args['type'],
            )
            db_sess.add(comment)
            db_sess.commit()

            chat = db_sess.query(PrivateChat).get(args['chatID']) if comment.type == "private" else db_sess.query(
                Chat).get(args['chatID'])
            if chat:
                chat.comments = f"{chat.comments},{comment.id}" if chat.comments else str(comment.id)
                db_sess.commit()

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


class AddFriendResource(Resource):
    def post(self, serch_user_id):
        if not current_user.is_authenticated:
            return {"error": "Требуется авторизация"}, 401
        db_sess = db_session.create_session()
        try:
            current_user_db = db_sess.query(User).get(current_user.id)
            target_user = db_sess.query(User).get(serch_user_id)

            if not target_user:
                return {'error': 'Пользователь не найден'}, 404

            if current_user.id == target_user.id:
                return {'error': 'Нельзя добавить самого себя'}, 400

            if current_user_db.own_requests:
                if str(serch_user_id) not in current_user_db.own_requests.split(','):
                    current_user_db.own_requests = f"{current_user_db.own_requests},{serch_user_id}"
            else:
                current_user_db.own_requests = str(serch_user_id)

            if target_user.friends_requests:
                if str(current_user.id) not in target_user.friends_requests.split(','):
                    target_user.friends_requests = f"{target_user.friends_requests},{current_user.id}"
            else:
                target_user.friends_requests = str(current_user.id)

            db_sess.commit()
            return {'status': 'success', 'message': 'Запрос на дружбу отправлен'}

        except Exception as e:
            db_sess.rollback()
            return {'error': str(e)}, 500
        finally:
            db_sess.close()


class RejectFriendRequestResource(Resource):
    def post(self, user_id):
        if not current_user.is_authenticated:
            return {"error": "Требуется авторизация"}, 401

        db_sess = db_session.create_session()

        try:
            current_user_db = db_sess.query(User).get(current_user.id)
            request_user = db_sess.query(User).get(int(user_id))

            if not request_user:
                return {'error': 'Пользователь не найден'}, 404

            request_user_requests = request_user.own_requests.split(",") if request_user.own_requests else []
            own_friends_requests = current_user_db.friends_requests.split(
                ",") if current_user_db.friends_requests else []

            if str(current_user.id) in request_user_requests:
                request_user_requests.remove(str(current_user.id))
            if str(request_user.id) in own_friends_requests:
                own_friends_requests.remove(str(request_user.id))

            request_user.own_requests = ",".join(request_user_requests) if request_user_requests else None
            current_user_db.friends_requests = ",".join(own_friends_requests) if own_friends_requests else None

            db_sess.commit()
            return {'status': 'success', 'message': 'Запрос в друзья отклонен'}

        except Exception as e:
            db_sess.rollback()
            return {'error': str(e)}, 500
        finally:
            db_sess.close()


class AcceptFriendRequestResource(Resource):
    def post(self, user_id):
        if not current_user.is_authenticated:
            return {"error": "Требуется авторизация"}, 401

        db_sess = db_session.create_session()

        try:
            current_user_db = db_sess.query(User).get(current_user.id)
            request_user = db_sess.query(User).get(int(user_id))

            if not request_user:
                return {'error': 'Пользователь не найден'}, 404

            request_user_requests = request_user.own_requests.split(",") if request_user.own_requests else []
            own_friends_requests = current_user_db.friends_requests.split(
                ",") if current_user_db.friends_requests else []
            own_user_requests = current_user_db.own_requests.split(",") if current_user_db.own_requests else []
            request_friends_requests = request_user.friends_requests.split(",") if request_user.friends_requests else []

            if str(current_user.id) in request_friends_requests:
                request_friends_requests.remove(str(current_user.id))
            if str(current_user.id) in request_user_requests:
                request_user_requests.remove(str(current_user.id))
            if str(request_user.id) in own_friends_requests:
                own_friends_requests.remove(str(request_user.id))
            if str(request_user.id) in own_user_requests:
                own_user_requests.remove(str(request_user.id))

            requests_friends = request_user.friends_ids.split(",") if request_user.friends_ids else []
            own_friends = current_user_db.friends_ids.split(",") if current_user_db.friends_ids else []

            if str(current_user.id) not in requests_friends:
                requests_friends.append(str(current_user.id))
            if str(request_user.id) not in own_friends:
                own_friends.append(str(request_user.id))

            chat = PrivateChat(
                members=f"{request_user.id},{current_user.id}",
                chat_name="Личный чат",
                chat_avatar=rf"..\static\img\chat.png",
                private_chat_with_friend=True,
            )
            db_sess.add(chat)
            db_sess.commit()

            if request_user.private_chat_ids:
                request_user.private_chat_ids = f"{request_user.private_chat_ids},{chat.id}"
            else:
                request_user.private_chat_ids = str(chat.id)
            if current_user_db.private_chat_ids:
                current_user_db.private_chat_ids = f"{current_user_db.private_chat_ids},{chat.id}"
            else:
                current_user_db.private_chat_ids = str(chat.id)

            request_user.friends_ids = ",".join(requests_friends)
            current_user_db.friends_ids = ",".join(own_friends)
            request_user.private_chat_ids
            current_user_db.private_chat_ids

            request_user.own_requests = ",".join(request_user_requests) if request_user_requests else None
            request_user.friends_requests = ",".join(request_friends_requests) if request_friends_requests else None

            current_user_db.own_requests = ",".join(own_user_requests) if own_user_requests else None
            current_user_db.friends_requests = ",".join(own_friends_requests) if own_friends_requests else None

            db_sess.commit()
            return {'status': 'success', 'message': 'Запрос в друзья принят'}

        except Exception as e:
            return {'error': str(e)}, 500
        finally:
            db_sess.close()


class RemoveFriendResource(Resource):
    def delete(self, friend_id):
        if not current_user.is_authenticated:
            return {"error": "Требуется авторизация"}, 401

        db_sess = db_session.create_session()
        try:
            current_user_db = db_sess.query(User).get(current_user.id)
            friend_to_delete = db_sess.query(User).get(int(friend_id))

            if not friend_to_delete:
                return {'error': 'Пользователь не найден'}, 404

            if not current_user_db.friends_ids or str(friend_id) not in current_user_db.friends_ids.split(','):
                return {'error': 'Пользователь не найден'}, 404

            own_friends = current_user_db.friends_ids.split(",") if current_user_db.friends_ids else []
            friend_friends = friend_to_delete.friends_ids.split(",") if friend_to_delete.friends_ids else []

            if str(friend_id) in own_friends:
                own_friends.remove(str(friend_id))
                current_user_db.friends_ids = ",".join(own_friends) if own_friends else None

            if str(current_user.id) in friend_friends:
                friend_friends.remove(str(current_user.id))
                friend_to_delete.friends_ids = ",".join(friend_friends) if friend_friends else None

            if current_user_db.private_chat_ids and friend_to_delete.private_chat_ids:
                cur_chat_ids = current_user_db.private_chat_ids.split(",")
                user_chat_ids = friend_to_delete.private_chat_ids.split(",")
                chat = db_sess.query(PrivateChat).filter(
                    and_(
                        PrivateChat.private_chat_with_friend == True,
                        PrivateChat.id.in_(cur_chat_ids),
                        PrivateChat.id.in_(user_chat_ids)
                    )
                ).first()
                if chat:
                    members = chat.members.split(",")
                    for member_id in members:
                        user = db_sess.query(User).get(int(member_id))
                        if user and user.private_chat_ids:
                            chats = user.private_chat_ids.split(",")
                            if str(chat.id) in chats:
                                chats.remove(str(chat.id))
                                user.private_chat_ids = ",".join(chats) if chats else None

                    db_sess.delete(chat)

            db_sess.commit()
            return {'status': 'success', 'message': 'Пользователь удален из друзей'}

        except Exception as e:
            db_sess.rollback()
            return {'error': str(e)}, 500
        finally:
            db_sess.close()


class DeletePostResource(Resource):
    def delete(self, post_id):

        if not current_user.is_authenticated:
            return {"error": "Требуется авторизация"}, 401

        db_sess = db_session.create_session()
        post = db_sess.query(Posts).get(post_id)
        author_id = post.creater
        if author_id != current_user.id:
            return {"error": "Отсутствуют права"}, 403

        users = db_sess.query(User).all()
        for user in users:
            if user.post_ids is not None:
                user_posts = user.post_ids.split(",")
                if post_id in user_posts:
                    user_posts.remove(post_id)
                    user.post_ids = ','.join(user_posts)
            if user.post_like_ids is not None:
                user_posts_like = user.post_like_ids.split(",")
                if post_id in user_posts_like:
                    user_posts_like.remove(post_id)
                    user.post_like_ids = ','.join(user_posts_like)
            if user.post_like_guide_category_ids is not None:
                user_posts_post_like_guide_category_ids = user.post_like_guide_category_ids.split(",")
                if post_id in user_posts_post_like_guide_category_ids:
                    user_posts_post_like_guide_category_ids.remove(post_id)
                    user.post_like_guide_category_ids = ','.join(user_posts_post_like_guide_category_ids)
            if user.post_like_ideas_category_ids is not None:
                user_posts_post_like_ideas_category_ids = user.post_like_ideas_category_ids.split(",")
                if post_id in user_posts_post_like_ideas_category_ids:
                    user_posts_post_like_ideas_category_ids.remove(post_id)
                    user.post_like_ideas_category_ids = ','.join(user_posts_post_like_ideas_category_ids)
            if user.post_like_mems_category_ids is not None:
                user_posts_post_like_mems_category_ids = user.post_like_mems_category_ids.split(",")
                if post_id in user_posts_post_like_mems_category_ids:
                    user_posts_post_like_mems_category_ids.remove(post_id)
                    user.post_like_mems_category_ids = ','.join(user_posts_post_like_mems_category_ids)
            if user.post_like_common_category_ids is not None:
                user_posts_post_like_common_category_ids = user.post_like_common_category_ids.split(",")
                if post_id in user_posts_post_like_common_category_ids:
                    user_posts_post_like_common_category_ids.remove(post_id)
                    user.post_like_common_category_ids = ','.join(user_posts_post_like_common_category_ids)
        chat = db_sess.query(Chat).get(int(post.comments_ids))
        if chat:
            db_sess.delete(chat)
            db_sess.commit()
        db_sess.delete(post)
        db_sess.commit()

class GetAllUsers(Resource):
    def get(self):
        query = request.args.get('q', '').lower()
        db_sess = db_session.create_session()
        users = []
        for i in db_sess.query(User).all():
            query = query.lower().strip()
            if query.replace(" ", "") in str(i.name.lower()) + str(i.surname.lower()):
                users.append(i)
        return jsonify([{
            'id': user.id,
            'name': user.name,
            'surname': user.surname,
            'img_avatar': user.img_avatar or '../static/img/avatar.jpg'  
        } for user in users])
        
def init_api(api):
    api.add_resource(GetAllUsers, '/api/search_users')
    api.add_resource(LikeResource, '/api/like')
    api.add_resource(ChatResource, '/api/chats/create', '/api/chats/edit/<int:chat_id>',
                     "/delete_private_chat/<chat_id>")
    api.add_resource(MessageResource, '/api/send-message')
    api.add_resource(AddFriendResource, '/add_friend/<int:serch_user_id>')
    api.add_resource(AcceptFriendRequestResource, '/accept_request/<user_id>')
    api.add_resource(RejectFriendRequestResource, '/reject_request/<user_id>')
    api.add_resource(RemoveFriendResource, '/delete_friend/<friend_id>')
    api.add_resource(DeletePostResource, '/del_post/<post_id>')
