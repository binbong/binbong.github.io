# binbong.github.io

个人站点「车行天下」— 静态站，托管于 GitHub Pages（tahoo.me）。

## 什么会推送、什么不会

「推送」= 执行 `git push` 后进 GitHub 仓库。  
「上网站」= 访客打开 tahoo.me 能看到的页面（仅 `docs/` 内文件）。

| 目录/文件 | 会 `git push` | 会上 tahoo.me |
|-----------|:-------------:|:-------------:|
| **`docs/`** | ✅ | ✅ 整站 |
| **`scripts/`** | ✅ | ❌ 仅构建用 |
| **`README.md`**（本文件） | ✅ | ❌ 只在 GitHub 仓库页显示 |
| **`scripts/README.md`** | ✅ | ❌ |
| **`tools/`** | ❌ 已 `.gitignore` | ❌ |
| **`serve.sh`、`本地预览.command`** | ❌ 已 `.gitignore` | ❌ |

`README.md` **应该推送**，用来在 GitHub 上说明项目；它不在 `docs/` 里，所以不会变成网站里的一个页面。

### `docs/` — 发布目录（推送 = 上线）

```
docs/
├── index.html
├── travel.html
├── route.html
├── CNAME
├── assets/css、assets/js
├── data/routes.json
└── images/
```

### 仓库根 — 开发与说明

```
scripts/          # 改 routes_data.py 后运行 build_site.py
tools/serve.sh    # 本地预览（不提交，可复制 tools/serve.sh 使用）
```

## GitHub Pages 设置

仓库 **Settings → Pages → Build and deployment**：

- **Source**: Deploy from a branch  
- **Branch**: `main`  
- **Folder**: **`/docs`**

若仍选根目录 `/`，上线会缺页面；请改为 **`/docs`**。

## 改内容

```bash
python3 scripts/build_site.py
git add docs/ scripts/ README.md
git commit -m "更新路线内容"
git push
```

## 本地预览

```bash
./serve.sh
# 或：bash tools/serve.sh
```

在 `docs/` 目录起静态服务，与线上一致。
