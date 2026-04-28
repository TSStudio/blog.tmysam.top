# blog.tmysam.top

## 本地开发

### 配置后端

```bash
cd backend
cp .env.example .env
```

把 `.env` 里的 `ADMIN_PASSWORD`、`JWT_SECRET` 和 MySQL 连接信息改成你的值。

### 启动后端

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 启动前端

```bash
cd frontend
npm install
npm run dev
```

前端默认请求 `http://localhost:8000/api/v1`。如果你要切换地址，可以在前端运行前设置：

```bash
VITE_API_BASE=http://localhost:8000/api/v1 npm run dev
```

## 部署

`npm run build` 将 `dist` 中的文件放在你的网站路径

后端 `uvicorn app.main:app --host 0.0.0.0 --port 8000`

请使用 systemctl 之类的守护程序进行自启动和自重启，并进行反向代理配置。

## GitHub 自动化

仓库包含以下自动化配置：

- Dependabot 每周一检查 npm、pip 和 GitHub Actions 依赖
- `Build Test` 会在 PR 和 main/master push 时构建前端并检查后端 Python 语法
- Dependabot PR 在 `Build Test` 成功后会自动 approve 并 merge
- 每月 1 日执行依赖滚动更新；如果 npm 或 pip 依赖有变化，会 bump 版本、构建测试、打 tag 并创建 GitHub Release

版本号格式为 `年.构建次数`，例如 `2026.1`。构建次数按当年已有 `v年.*` tag 递增。

为了让自动 approve 和 merge 生效，需要在 GitHub 仓库设置中确认：

- `Settings -> Actions -> General -> Workflow permissions` 选择 `Read and write permissions`
- 允许 GitHub Actions 创建和批准 pull request
- 如果启用了分支保护，确保 `Build Test` 是必需检查项
