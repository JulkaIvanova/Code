from datetime import datetime

ID = 0
CR_D = 4
CTG = 6


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
        sorted_data = sorted(data, key=lambda x: parse_date(x[CR_D]), reverse=True)
    else:
        matching = [post for post in data if post[CTG] == filter_posts]
        non_matching = [post for post in data if post[CTG] != filter_posts]
        sorted_matching = sorted(matching, key=lambda x: parse_date(x[CR_D]), reverse=True)
        sorted_non_matching = sorted(non_matching, key=lambda x: parse_date(x[CR_D]), reverse=True)
        sorted_data = sorted_matching + sorted_non_matching
    if not full:
        return [post[ID] for post in sorted_data]
    return sorted_data
