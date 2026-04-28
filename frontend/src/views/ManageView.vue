<template>
  <section class="stack">
    <div v-if="!isLoggedIn" class="panel stack manage-login-panel">
      <div>
        <h1 class="section-title">文章管理</h1>
        <p class="section-subtitle">先登录，再进入 Markdown 编辑器。</p>
      </div>

      <div class="field-row">
        <label class="field">
          <span>管理密码</span>
          <input
            v-model="password"
            type="password"
            placeholder="输入后端配置的密码"
            @keyup.enter="handleLogin"
          />
        </label>
        <button class="primary-button" type="button" @click="handleLogin" :disabled="loginLoading">
          {{ loginLoading ? "登录中..." : "登录" }}
        </button>
      </div>

      <p v-if="saveMessage" class="feedback" :class="{ error: saveMessageIsError }">{{ saveMessage }}</p>
    </div>

    <div v-else class="manage-layout">
      <div class="panel stack">
        <div class="toolbar">
          <div>
            <h1 class="section-title">文章管理</h1>
            <p class="section-subtitle">登录后可新建文章，或加载已有文章继续编辑。</p>
          </div>
        </div>

        <div class="field-row">
          <label class="field field-grow">
            <span>文章 ID</span>
            <input v-model="articleId" type="text" placeholder="留空表示新建文章" />
          </label>
          <button class="ghost-button" type="button" @click="loadExistingArticle" :disabled="loadLoading">
            {{ loadLoading ? "加载中..." : "加载文章" }}
          </button>
        </div>

        <label class="toggle-row">
          <input v-model="hidden" type="checkbox" />
          <span>隐藏文章（不出现在文章列表中）</span>
        </label>

        <div class="field">
          <span>Markdown 内容</span>
          <MarkdownEditor
            v-model="content"
            placeholder="# 标题&#10;&#10;在这里开始写作..."
          />
        </div>

        <div class="toolbar">
          <p class="feedback" :class="{ error: saveMessageIsError }">{{ saveMessage || helperText }}</p>
          <button class="primary-button" type="button" @click="saveCurrentArticle" :disabled="saveLoading">
            {{ saveLoading ? "保存中..." : "保存文章" }}
          </button>
        </div>
      </div>

      <div class="panel stack">
        <div>
          <h2 class="section-title">实时预览</h2>
          <p class="section-subtitle">标题和摘要由后端从 Markdown 自动提取。</p>
        </div>
        <div class="markdown-body preview-body" v-html="previewHtml"></div>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { computed, ref, watch } from "vue";
import { useRoute } from "vue-router";
import { fetchArticle, login, saveArticle } from "../api";
import { renderMarkdown } from "../utils";
import MarkdownEditor from "../components/MarkdownEditor.vue";

const route = useRoute();
const password = ref("");
const token = ref(localStorage.getItem("blog_admin_token") ?? "");
const articleId = ref("");
const content = ref("# 新文章\n\n开始写点什么吧。");
const hidden = ref(false);
const helperText = "支持 Markdown 工具栏、Tab 缩进和实时预览。若填写文章 ID，将覆盖原文章并更新修改时间。";
const saveMessage = ref("");
const saveMessageIsError = ref(false);
const loginLoading = ref(false);
const loadLoading = ref(false);
const saveLoading = ref(false);

const previewHtml = computed(() => renderMarkdown(content.value));
const isLoggedIn = computed(() => Boolean(token.value));

async function maybeLoadArticleFromRoute() {
  const routeArticleId = route.query.articleId;
  if (!isLoggedIn.value || typeof routeArticleId !== "string" || !routeArticleId.trim()) {
    return;
  }
  if (articleId.value === routeArticleId && content.value.trim()) {
    return;
  }
  articleId.value = routeArticleId;
  await loadExistingArticle();
}

async function handleLogin() {
  loginLoading.value = true;
  saveMessage.value = "";
  try {
    const response = await login(password.value);
    token.value = response.token;
    localStorage.setItem("blog_admin_token", response.token);
    saveMessage.value = "登录成功，已经可以保存文章。";
    saveMessageIsError.value = false;
    await maybeLoadArticleFromRoute();
  } catch (error) {
    saveMessage.value = error instanceof Error ? error.message : "登录失败";
    saveMessageIsError.value = true;
  } finally {
    loginLoading.value = false;
  }
}

async function loadExistingArticle() {
  if (!articleId.value.trim()) {
    saveMessage.value = "请输入要加载的文章 ID。";
    saveMessageIsError.value = true;
    return;
  }

  loadLoading.value = true;
  saveMessage.value = "";
  try {
    const response = await fetchArticle(articleId.value.trim());
    content.value = response.content;
    hidden.value = response.hidden;
    saveMessage.value = "文章已加载。";
    saveMessageIsError.value = false;
  } catch (error) {
    saveMessage.value = error instanceof Error ? error.message : "加载失败";
    saveMessageIsError.value = true;
  } finally {
    loadLoading.value = false;
  }
}

async function saveCurrentArticle() {
  if (!token.value) {
    saveMessage.value = "请先登录。";
    saveMessageIsError.value = true;
    return;
  }

  saveLoading.value = true;
  saveMessage.value = "";
  try {
    const response = await saveArticle(
      content.value,
      token.value,
      articleId.value.trim() || undefined,
      hidden.value,
    );
    articleId.value = response.article_id;
    saveMessage.value = `保存成功，文章 ID：${response.article_id}`;
    saveMessageIsError.value = false;
  } catch (error) {
    saveMessage.value = error instanceof Error ? error.message : "保存失败";
    saveMessageIsError.value = true;
  } finally {
    saveLoading.value = false;
  }
}

watch(
  () => route.query.articleId,
  () => {
    void maybeLoadArticleFromRoute();
  },
  { immediate: true },
);
</script>
