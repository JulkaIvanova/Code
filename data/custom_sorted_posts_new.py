import datetime
from typing import List, Optional

from .posts import Posts


def custom_sorted_posts(
        posts: List[Posts],
        category_filter: Optional[str] = None
) -> List[Posts]:
    def sort_key(post: Posts):
        return post.create_date or datetime.min

    if category_filter is None:
        return sorted(posts, key=sort_key, reverse=True)

    matching = [p for p in posts if p.category == category_filter]
    non_matching = [p for p in posts if p.category != category_filter]

    sorted_matching = sorted(matching, key=sort_key, reverse=True)
    sorted_non_matching = sorted(non_matching, key=sort_key, reverse=True)
    return sorted_matching + sorted_non_matching
