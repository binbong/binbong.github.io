# binbong.github.io

个人站点「车行天下」— 静态 HTML，GitHub Pages（tahoo.me）。

## 目录说明

| 路径 | 会 `git push` | 访客可见（tahoo.me） |
|------|:-------------:|:-------------------:|
| 根目录 `index.html`、`travel.html`、`route.html` | ✅ | ✅ |
| `assets/`、`data/`、`images/`、`CNAME` | ✅ | ✅ |
| `scripts/` | ✅ | ❌ 仅构建 |
| 根目录 `README.md` | ✅ | ❌（GitHub 仓库说明；`.nojekyll` 防止被当成网站首页） |
| `tools/`、`serve.sh`、`本地预览.command` | ❌ `.gitignore` | ❌ |

## 改内容

```bash
python3 scripts/build_site.py
git add index.html travel.html route.html assets/ data/ images/ scripts/ README.md .nojekyll CNAME
git commit -m "更新路线"
git push
```

## GitHub Pages

本仓库为用户站 **binbong.github.io**，请使用：

- **Settings → Pages → Branch: `main` → Folder: `/ (root)`**

不要用 `/docs`，否则域名根路径会 404。根目录的 **`.nojekyll`** 必须保留，否则 GitHub 会用 Jekyll 渲染 README 而不是你的 `index.html`。

## 本地预览

```bash
./serve.sh
```
