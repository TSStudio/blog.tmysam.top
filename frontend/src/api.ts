import type {
  ArticleResponse,
  ListResponse,
  LoginResponse,
  ModifyResponse,
} from "./types/api";

function resolveApiBase(): string {
  const envBase = import.meta.env.VITE_API_BASE as string | undefined;
  if (envBase) {
    return envBase;
  }

  if (import.meta.env.DEV) {
    return "http://localhost:8000/api/v1";
  }

  return `${window.location.origin}/api/v1`;
}

const API_BASE = resolveApiBase();

function withNoCacheQuery(input: string): string {
  const url = new URL(input, window.location.origin);
  url.searchParams.set("_t", `${Date.now()}_${Math.random().toString(36).slice(2, 10)}`);
  return url.toString();
}

async function requestJson<T>(input: string, init?: RequestInit): Promise<T> {
  const headers = new Headers(init?.headers);
  if (!headers.has("Content-Type")) {
    headers.set("Content-Type", "application/json");
  }
  headers.set("Cache-Control", "no-cache, no-store, max-age=0");
  headers.set("Pragma", "no-cache");
  headers.set("Expires", "0");

  const response = await fetch(withNoCacheQuery(input), {
    ...init,
    headers,
  });

  if (!response.ok) {
    const text = await response.text();
    throw new Error(text || `Request failed with status ${response.status}`);
  }

  return response.json() as Promise<T>;
}

export function fetchArticles(beginOffset = 0, endOffset = 20, token?: string): Promise<ListResponse> {
  const url = new URL(`${API_BASE}/list/`);
  url.searchParams.set("begin_offset", String(beginOffset));
  url.searchParams.set("end_offset", String(endOffset));
  return requestJson<ListResponse>(url.toString(), {
    headers: token
      ? {
          Authorization: `Bearer ${token}`,
        }
      : undefined,
  });
}

export function fetchArticle(articleId: string): Promise<ArticleResponse> {
  const url = new URL(`${API_BASE}/article/`);
  url.searchParams.set("article_id", articleId);
  return requestJson<ArticleResponse>(url.toString());
}

export function login(password: string): Promise<LoginResponse> {
  return requestJson<LoginResponse>(`${API_BASE}/login/`, {
    method: "POST",
    body: JSON.stringify({
      password,
    }),
  });
}

export function saveArticle(
  content: string,
  token: string,
  articleId?: string,
  hidden = false,
): Promise<ModifyResponse> {
  return requestJson<ModifyResponse>(`${API_BASE}/modify/`, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify({
      article_id: articleId,
      content,
      hidden,
    }),
  });
}
