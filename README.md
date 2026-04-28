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