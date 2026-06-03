(function () {
    function escapeHtml(text) {
        return String(text)
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;');
    }

    function getSlug() {
        var params = new URLSearchParams(window.location.search);
        return (params.get('slug') || '').trim();
    }

    function dayMeta(day) {
        var parts = [];
        if (day.drive) parts.push(day.drive);
        if (day.stay) parts.push(day.stay);
        return parts.join(' · ');
    }

    function renderRoute(route) {
        var hero = route.images.hero;
        var tags = route.tags.map(function (t) {
            return '<span class="route-tag">' + escapeHtml(t) + '</span>';
        }).join('');

        var overview = (route.overview || []).map(function (p) {
            return '<p class="detail-overview-p">' + escapeHtml(p) + '</p>';
        }).join('');

        var days = (route.days || []).map(function (d) {
            return (
                '<article class="detail-day">' +
                '<div class="detail-day-head">' +
                '<span class="detail-day-num">' + escapeHtml(d.day) + '</span>' +
                '<h3 class="detail-day-title">' + escapeHtml(d.title) + '</h3>' +
                '</div>' +
                '<p class="detail-day-meta">' + escapeHtml(dayMeta(d)) + '</p>' +
                '<p class="detail-day-text">' + escapeHtml(d.text) + '</p>' +
                '</article>'
            );
        }).join('');

        var gallery = (route.images.gallery || []).map(function (g) {
            return (
                '<figure class="detail-gallery-item">' +
                '<img src="' + escapeHtml(g.src) + '" alt="' + escapeHtml(g.caption) + '" loading="lazy">' +
                '<figcaption>' + escapeHtml(g.caption) + '</figcaption>' +
                '</figure>'
            );
        }).join('');

        var spots = (route.spots || []).map(function (s) {
            return (
                '<div class="detail-spot">' +
                '<h3 class="detail-spot-name">' + escapeHtml(s.name) + '</h3>' +
                '<p class="detail-spot-text">' + escapeHtml(s.text) + '</p>' +
                '</div>'
            );
        }).join('');

        var stops = (route.stops || []).map(function (s, i) {
            var detail = s.detail
                ? '<p class="route-stop-detail">' + escapeHtml(s.detail) + '</p>'
                : '';
            return (
                '<div class="route-stop">' +
                '<span class="route-stop-num">' + (i + 1) + '</span>' +
                '<div>' +
                '<strong>' + escapeHtml(s.name) + '</strong>' +
                '<span class="route-stop-km">' + escapeHtml(s.km) + '</span>' +
                '<p>' + escapeHtml(s.note) + '</p>' +
                detail +
                '</div></div>'
            );
        }).join('');

        var practical = (route.practical || []).map(function (t) {
            return '<li>' + escapeHtml(t) + '</li>';
        }).join('');

        var evTips = (route.ev_tips || []).map(function (t) {
            return '<li>' + escapeHtml(t) + '</li>';
        }).join('');

        return (
            '<section class="detail-hero">' +
            '<div class="detail-hero-bg" style="background-image:url(\'' + escapeHtml(hero) + '\')"></div>' +
            '<div class="hero-overlay"></div>' +
            '<div class="detail-hero-content">' +
            '<a href="travel.html" class="detail-back">← 返回路线列表</a>' +
            '<span class="hero-eyebrow">' + escapeHtml(route.tagline) + '</span>' +
            '<h1 class="hero-title">' + escapeHtml(route.name) + '</h1>' +
            '<p class="hero-subtitle">' + escapeHtml(route.summary) + '</p>' +
            '<div class="detail-stats">' +
            '<div><span class="detail-stat-val">' + escapeHtml(route.distance) + '</span><span class="detail-stat-lbl">总里程</span></div>' +
            '<div><span class="detail-stat-val">' + escapeHtml(route.duration) + '</span><span class="detail-stat-lbl">建议天数</span></div>' +
            '<div><span class="detail-stat-val">' + escapeHtml(route.season) + '</span><span class="detail-stat-lbl">最佳季节</span></div>' +
            '</div></div></section>' +
            '<article class="detail-body"><div class="detail-inner">' +
            '<div class="detail-lead">' +
            '<p class="detail-lead-text">' + escapeHtml(route.intro) + '</p>' +
            '<div class="detail-overview">' + overview + '</div>' +
            '<div class="route-highlights detail-tags">' + tags + '</div></div>' +
            '<section class="detail-section"><p class="section-eyebrow">Itinerary</p>' +
            '<h2 class="section-title">分日行程</h2><div class="detail-days">' + days + '</div></section>' +
            '<section class="detail-section"><p class="section-eyebrow">Photo Essay</p>' +
            '<h2 class="section-title">沿途影像</h2><div class="detail-gallery detail-gallery-wide">' + gallery + '</div></section>' +
            '<section class="detail-section"><p class="section-eyebrow">Highlights</p>' +
            '<h2 class="section-title">核心景点</h2><div class="detail-spots">' + spots + '</div></section>' +
            '<section class="detail-section"><p class="section-eyebrow">Route</p>' +
            '<h2 class="section-title">途经站点</h2><div class="route-stops route-stops-full">' + stops + '</div></section>' +
            '<section class="detail-section"><p class="section-eyebrow">Practical</p>' +
            '<h2 class="section-title">实用信息</h2><ul class="detail-list">' + practical + '</ul></section>' +
            '<section class="detail-section detail-ev"><p class="section-eyebrow">EV Tips</p>' +
            '<h2 class="section-title">新能源出行提示</h2>' +
            '<p class="section-desc">驾驶腾势 N7 等纯电 SUV 出发前，请特别注意以下事项：</p>' +
            '<ul class="detail-list detail-ev-list">' + evTips + '</ul></section>' +
            '</div></article>'
        );
    }

    function renderNotFound(slug) {
        return (
            '<section class="section" style="padding-top:120px;min-height:50vh">' +
            '<div class="section-inner">' +
            '<h1 class="section-title">未找到路线</h1>' +
            '<p class="section-desc">没有名为「' + escapeHtml(slug) + '」的攻略，请返回列表选择。</p>' +
            '<p style="margin-top:24px"><a href="travel.html" class="btn btn-primary">返回自驾游路线</a></p>' +
            '</div></section>'
        );
    }

    function setMeta(route) {
        document.title = route.name + ' — 车行天下';
        var desc = document.querySelector('meta[name="description"]');
        if (desc) desc.setAttribute('content', route.summary);
    }

    async function loadRoutes() {
        if (window.ROUTES_DATA && Array.isArray(window.ROUTES_DATA)) {
            return window.ROUTES_DATA;
        }
        var res = await fetch('data/routes.json');
        if (!res.ok) throw new Error('无法加载路线数据');
        return res.json();
    }

    async function init() {
        var slug = getSlug();
        var app = document.getElementById('routeApp');
        var navBottom = document.getElementById('routeNavBottom');
        if (!app) return;

        try {
            var routes = await loadRoutes();
            var route = routes.find(function (r) { return r.slug === slug; });

            if (!slug || !route) {
                app.innerHTML = renderNotFound(slug);
                document.title = '未找到路线 — 车行天下';
                if (navBottom) navBottom.hidden = true;
                return;
            }

            app.innerHTML = renderRoute(route);
            setMeta(route);
            if (navBottom) navBottom.hidden = false;
            window.scrollTo(0, 0);
        } catch (err) {
            app.innerHTML =
                '<section class="section" style="padding-top:120px">' +
                '<div class="section-inner"><p class="section-desc">加载失败，请刷新重试。</p></div></section>';
            if (navBottom) navBottom.hidden = true;
            console.error(err);
        }
    }

    init();
})();
