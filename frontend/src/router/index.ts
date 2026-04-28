import { createRouter, createWebHashHistory } from "vue-router";
import HomeView from "../views/HomeView.vue";
import ArticleView from "../views/ArticleView.vue";
import ManageView from "../views/ManageView.vue";

const router = createRouter({
  history: createWebHashHistory(),
  routes: [
    { path: "/", name: "home", component: HomeView },
    { path: "/article/:articleId", name: "article", component: ArticleView, props: true },
    { path: "/manage", name: "manage", component: ManageView },
  ],
  scrollBehavior() {
    return { top: 0 };
  },
});

export default router;
