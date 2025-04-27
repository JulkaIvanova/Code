import datetime
from dataclasses import dataclass
from typing import List
from .posts import Posts
from .users import User


def parse_ids(s: str) -> List[int]:
    if not s:
        return []
    return [int(x) for x in s.split(',') if x.strip().isdigit()]


def sort_posts_by_user_likes(user: User, posts: List[Posts]) -> List[Posts]:
    liked_ids = parse_ids(user.post_like_ids)
    if len(liked_ids) < 10:
        return sorted(posts, key=lambda p: p.create_date, reverse=True)

    category_fields = {
        'guide': user.post_like_guide_category_ids,
        'ideas': user.post_like_ideas_category_ids,
        'mems': user.post_like_mems_category_ids,
        'all': user.post_like_common_category_ids,
    }
    counts = {cat: len(parse_ids(ids)) for cat, ids in category_fields.items()}
    sorted_cats = [cat for cat, _ in sorted(counts.items(), key=lambda x: x[1], reverse=True)]

    result = []
    for cat in sorted_cats:
        cat_posts = [p for p in posts if p.category == cat]
        cat_posts.sort(key=lambda p: p.create_date, reverse=True)
        result.extend(cat_posts)
    return result
