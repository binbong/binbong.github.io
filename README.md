# binbong.github.io

个人站点「车行天下」— 静态 HTML + GitHub Pages（tahoo.me）。

## 仓库结构（整理后）

```
binbong.github.io/
├── README.md              ← 本说明（进 Git，不是网站页面）
├── docs/                  ← 整站唯一发布目录（进 Git → 上线）
│   ├── index.html
│   ├── travel.html
│   ├── route.html
│   ├── CNAME
│   ├── .nojekyll
│   ├── assets/
│   ├── data/
│   └── images/
├── scripts/               ← 构建脚本 + 路线文案（进 Git，不是网站页面）
└── tools/                 ← 本地预览（不进 Git）
```

根目录**不再**散落 `index.html`、CSS、图片，避免和构建工具混在一起。

## GitHub Pages 必须这样设

**Settings → Pages → Build and deployment**

| 项 | 值 |
|----|-----|
| Source | Deploy from a branch |
| Branch | `main` |
| **Folder** | **`/docs`** ← 必选，不是 `/ (root)` |

设成 `/docs` 后，访客地址仍是：

- https://tahoo.me/
- https://tahoo.me/travel.html  

（不会出现 `/docs/travel.html` 这种路径。）

若 Folder 仍是 **root**，而文件只在 `docs/` 里，就会 **404**——这是上次线上挂掉的原因，不是代码坏了。

## 改内容

```bash
python3 scripts/build_site.py
git add docs/ scripts/
git commit -m "更新路线"
git push
```

## 本地预览

```bash
./serve.sh
```

在 `docs/` 目录起服务，和线上一致。
