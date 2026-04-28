from fastapi import HTTPException, status

from .content import extract_abstract, extract_title, new_article_id
from .database import get_connection


def list_articles(begin_offset: int, end_offset: int, include_hidden: bool = False) -> tuple[int, list[dict]]:
    limit = max(end_offset - begin_offset, 0)
    where_clause = "" if include_hidden else "WHERE hidden = 0"
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(f"SELECT COUNT(*) AS total FROM articles {where_clause}")
            total = cursor.fetchone()["total"]
            cursor.execute(
                f"""
                SELECT article_id, title, abstract,
                       UNIX_TIMESTAMP(created_at) AS created,
                       UNIX_TIMESTAMP(modified_at) AS modified,
                       hidden
                FROM articles
                {where_clause}
                ORDER BY created_at DESC
                LIMIT %s OFFSET %s
                """,
                (limit, begin_offset),
            )
            return total, cursor.fetchall()


def get_article(article_id: str) -> dict:
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT title, content,
                       UNIX_TIMESTAMP(created_at) AS created,
                       UNIX_TIMESTAMP(modified_at) AS modified,
                       hidden
                FROM articles
                WHERE article_id = %s
                """,
                (article_id,),
            )
            article = cursor.fetchone()
            if article is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Article not found")
            return article


def upsert_article(article_id: str | None, content: str, hidden: bool) -> str:
    title = extract_title(content)
    abstract = extract_abstract(content)

    with get_connection() as connection:
        with connection.cursor() as cursor:
            if article_id:
                cursor.execute("SELECT article_id FROM articles WHERE article_id = %s", (article_id,))
                existing = cursor.fetchone()
                if existing is None:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail="Article not found for update",
                    )
                cursor.execute(
                    """
                    UPDATE articles
                    SET title = %s,
                        abstract = %s,
                        content = %s,
                        hidden = %s,
                        modified_at = CURRENT_TIMESTAMP
                    WHERE article_id = %s
                    """,
                    (title, abstract, content, hidden, article_id),
                )
                return article_id

            new_id = new_article_id()
            cursor.execute(
                """
                INSERT INTO articles (article_id, title, abstract, content, hidden)
                VALUES (%s, %s, %s, %s, %s)
                """,
                (new_id, title, abstract, content, hidden),
            )
            return new_id
