from typing import Annotated

from fastapi import Body, Depends, FastAPI, Header, HTTPException, Query, status
from fastapi.middleware.cors import CORSMiddleware

from .auth import create_token, decode_token, verify_password
from .config import settings
from .database import ensure_schema
from .models import (
    ArticleResponse,
    ListResponse,
    LoginRequest,
    LoginResponse,
    ModifyRequest,
    ModifyResponse,
    StatusPayload,
)
from .repository import get_article, list_articles, upsert_article

app = FastAPI(title=settings.app_name)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_origin_regex=r"https?://(localhost|127\.0\.0\.1)(:\d+)?$",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup_event() -> None:
    ensure_schema()


def require_token(authorization: Annotated[str | None, Header()] = None) -> None:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing bearer token")
    token = authorization.split(" ", 1)[1].strip()
    decode_token(token)


def is_admin_request(authorization: Annotated[str | None, Header()] = None) -> bool:
    if not authorization or not authorization.startswith("Bearer "):
        return False
    token = authorization.split(" ", 1)[1].strip()
    try:
        decode_token(token)
    except HTTPException:
        return False
    return True


@app.get("/")
def root() -> dict[str, str]:
    return {"message": "tmysam blog api is running"}


@app.get(f"{settings.api_prefix}/list/", response_model=ListResponse)
def api_list_articles(
    begin_offset: int = Query(default=0, ge=0),
    end_offset: int = Query(default=20, gt=0),
    is_admin: bool = Depends(is_admin_request),
):
    total, results = list_articles(begin_offset, end_offset, include_hidden=is_admin)
    return ListResponse(
        total_results=total,
        results=results,
        status=StatusPayload(code="success", message="ok"),
    )


@app.get(f"{settings.api_prefix}/article/", response_model=ArticleResponse)
def api_get_article(article_id: str = Query(...)):
    return ArticleResponse(**get_article(article_id))


@app.post(f"{settings.api_prefix}/login/", response_model=LoginResponse)
def api_login(payload: Annotated[LoginRequest, Body()]):
    if not verify_password(payload.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid password")
    return LoginResponse(status=StatusPayload(code="success", message="ok"), token=create_token())


@app.post(f"{settings.api_prefix}/modify/", response_model=ModifyResponse, dependencies=[Depends(require_token)])
def api_modify_article(payload: Annotated[ModifyRequest, Body()]):
    article_id = upsert_article(payload.article_id, payload.content, payload.hidden)
    return ModifyResponse(
        status=StatusPayload(code="success", message="ok"),
        article_id=article_id,
    )


@app.get(f"{settings.api_prefix}/modify/", response_model=ModifyResponse, dependencies=[Depends(require_token)])
def api_modify_article_legacy(
    content: str = Query(...),
    article_id: str | None = Query(default=None),
    hidden: bool = Query(default=False),
):
    saved_article_id = upsert_article(article_id, content, hidden)
    return ModifyResponse(
        status=StatusPayload(code="success", message="ok"),
        article_id=saved_article_id,
    )
