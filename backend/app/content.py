import re
import uuid


def extract_title(markdown: str) -> str:
    for line in markdown.splitlines():
        stripped = line.strip()
        if stripped.startswith("#"):
            title = stripped.lstrip("#").strip()
            if title:
                return title

    for line in markdown.splitlines():
        stripped = line.strip()
        if stripped:
            return stripped[:120]
    return "Untitled"


def extract_abstract(markdown: str) -> str:
    cleaned = re.sub(r"^#+\s+", "", markdown, flags=re.MULTILINE)
    paragraphs = [segment.strip() for segment in cleaned.split("\n\n") if segment.strip()]
    for paragraph in paragraphs:
        single_line = " ".join(part.strip() for part in paragraph.splitlines())
        if single_line:
            return single_line[:180]
    return "暂无摘要"


def new_article_id() -> str:
    return uuid.uuid4().hex
