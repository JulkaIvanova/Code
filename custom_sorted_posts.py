from datetime import datetime

# Константы для номеров элементов кортежа
ID = 0
CR_D = 4  # индекс create_date
CTG = 6  # индекс category


def custom_sorted_posts(data, filter_posts=None, full=False):
    """
    Сортирует список постов и возвращает либо их полное содержимое, либо только ID в нужном порядке.

    Если filter задан, то:
      1. Сначала идут посты, у которых post[CTG] == filter, отсортированные по дате (от новых к старым).
      2. Затем идут остальные посты, отсортированные по дате (от новых к старых).

    Если filter равен None, то сортировка производится по дате (от новых к старых) для всех постов.

    Параметры:
      data: список кортежей, где каждый кортеж имеет вид
            ('id', 'likes', 'caption', 'comment', 'create_date', 'imgs', 'category', 'creater')
      filter: строка с нужной категорией для фильтрации (по умолчанию None)
      full: если True, возвращаются полные посты, иначе — только ID постов (по умолчанию False)

    Возвращает:
      Отсортированный список постов либо список ID постов в нужном порядке.
    """

    def parse_date(date_str):
        return datetime.fromisoformat(date_str)

    if filter_posts is None:
        # Сортируем весь список по дате (от новых к старым)
        sorted_data = sorted(data, key=lambda x: parse_date(x[CR_D]), reverse=True)
    else:
        # Делим посты на две группы: подходящие по категории и остальные
        matching = [post for post in data if post[CTG] == filter_posts]
        non_matching = [post for post in data if post[CTG] != filter_posts]
        sorted_matching = sorted(matching, key=lambda x: parse_date(x[CR_D]), reverse=True)
        sorted_non_matching = sorted(non_matching, key=lambda x: parse_date(x[CR_D]), reverse=True)
        sorted_data = sorted_matching + sorted_non_matching

    # Если full=False, возвращаем только ID постов
    if not full:
        return [post[ID] for post in sorted_data]
    # Иначе возвращаем полный пост
    return sorted_data


            # # Пример списка с 15 постами для проверки
            # example_data = [
            #     (1, 100, "Caption1", "Comment1", "2025-03-14 10:30:00.000000", "img1.jpg", "tech", "user1"),
            #     (2, 150, "Caption2", "Comment2", "2025-03-15 09:20:00.000000", "img2.jpg", "food", "user2"),
            #     (3, 200, "Caption3", "Comment3", "2025-03-13 12:00:00.000000", "img3.jpg", "tech", "user3"),
            #     (4, 250, "Caption4", "Comment4", "2025-03-12 08:15:00.000000", "img4.jpg", "travel", "user4"),
            #     (5, 300, "Caption5", "Comment5", "2025-03-16 14:45:00.000000", "img5.jpg", "tech", "user5"),
            #     (6, 350, "Caption6", "Comment6", "2025-03-11 16:30:00.000000", "img6.jpg", "food", "user6"),
            #     (7, 400, "Caption7", "Comment7", "2025-03-15 18:20:00.000000", "img7.jpg", "travel", "user7"),
            #     (8, 450, "Caption8", "Comment8", "2025-03-14 21:00:00.000000", "img8.jpg", "tech", "user8"),
            #     (9, 500, "Caption9", "Comment9", "2025-03-10 11:05:00.000000", "img9.jpg", "food", "user9"),
            #     (10, 550, "Caption10", "Comment10", "2025-03-17 07:25:00.000000", "img10.jpg", "travel", "user10"),
            #     (11, 600, "Caption11", "Comment11", "2025-03-18 15:00:00.000000", "img11.jpg", "tech", "user11"),
            #     (12, 650, "Caption12", "Comment12", "2025-03-17 20:30:00.000000", "img12.jpg", "food", "user12"),
            #     (13, 700, "Caption13", "Comment13", "2025-03-16 22:10:00.000000", "img13.jpg", "tech", "user13"),
            #     (14, 750, "Caption14", "Comment14", "2025-03-09 13:45:00.000000", "img14.jpg", "travel", "user14"),
            #     (15, 800, "Caption15", "Comment15", "2025-03-19 09:55:00.000000", "img15.jpg", "food", "user15")
            # ]
            #
            # # Примеры использования:
            # # 1. С фильтром "tech" и только ID
            # sorted_ids_tech = custom_sorted_posts(example_data, filter_posts="tech", full=False)
            # print("Список ID с фильтром 'tech':")
            # print(sorted_ids_tech)
            #
            # # 2. Без фильтра, возвращаются только ID
            # sorted_ids_all = custom_sorted_posts(example_data, full=False)
            # print("\nСписок ID без фильтра:")
            # print(sorted_ids_all)
            #
            # # 3. С фильтром "tech" и полным содержимым постов
            # sorted_posts_full = custom_sorted_posts(example_data, filter_posts="tech", full=True)
            # print("\nПолный список постов с фильтром 'tech':")
            # for post in sorted_posts_full:
            #     print(post)
