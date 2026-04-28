from pydantic import BaseModel, Field


class StatusPayload(BaseModel):
    code: str
    message: str


class ListRequest(BaseModel):
    begin_offset: int = Field(0, ge=0)
    end_offset: int = Field(20, gt=0)


class ArticleRequest(BaseModel):
    article_id: str


class LoginRequest(BaseModel):
    password: str


class ModifyRequest(BaseModel):
    article_id: str | None = None
    content: str = Field(min_length=1)
    hidden: bool = False


class ArticlePreview(BaseModel):
    title: str
    abstract: str
    created: int
    modified: int
    article_id: str
    hidden: bool


class ListResponse(BaseModel):
    total_results: int
    results: list[ArticlePreview]
    status: StatusPayload


class ArticleResponse(BaseModel):
    title: str
    content: str
    created: int
    modified: int
    hidden: bool


class LoginResponse(BaseModel):
    status: StatusPayload
    token: str


class ModifyResponse(BaseModel):
    status: StatusPayload
    article_id: str
