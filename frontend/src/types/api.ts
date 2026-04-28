export interface StatusPayload {
  code: "success" | "error";
  message: string;
}

export interface ArticlePreview {
  title: string;
  abstract: string;
  created: number;
  modified: number;
  article_id: string;
  hidden: boolean;
}

export interface ListResponse {
  total_results: number;
  results: ArticlePreview[];
  status: StatusPayload;
}

export interface ArticleResponse {
  title: string;
  content: string;
  created: number;
  modified: number;
  hidden: boolean;
}

export interface LoginResponse {
  status: StatusPayload;
  token: string;
}

export interface ModifyResponse {
  status: StatusPayload;
  article_id: string;
}
