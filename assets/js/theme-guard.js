/* Lock dark-theme colors when browser eye-care / filter modes override them. */
(function () {
    var rules = [
        ['.detail-hero .hero-title, .detail-hero .hero-eyebrow, .detail-stat-val', '#ffffff'],
        ['.detail-hero .hero-subtitle', 'rgba(255,255,255,0.9)'],
        ['.detail-stat-lbl, .detail-back', 'rgba(255,255,255,0.85)'],
        ['.detail-lead-text', '#f5f5f7'],
        ['.hero .hero-title, section.hero .hero-title', '#ffffff'],
        ['.hero .hero-subtitle, section.hero .hero-subtitle', 'rgba(255,255,255,0.9)']
    ];

    function lockTheme() {
        var root = document.documentElement;
        var body = document.body;
        root.style.setProperty('color-scheme', 'only dark', 'important');
        root.style.setProperty('background-color', '#0a0a0a', 'important');
        root.style.setProperty('color', '#f5f5f7', 'important');
        if (body) {
            body.style.setProperty('background-color', '#0a0a0a', 'important');
            body.style.setProperty('color', '#f5f5f7', 'important');
        }
        rules.forEach(function (rule) {
            document.querySelectorAll(rule[0]).forEach(function (el) {
                el.style.setProperty('color', rule[1], 'important');
                el.style.setProperty('-webkit-text-fill-color', rule[1], 'important');
            });
        });
    }

    lockTheme();
    new MutationObserver(lockTheme).observe(document.documentElement, {
        subtree: true,
        attributes: true,
        attributeFilter: ['style', 'class'],
        childList: true
    });
    document.addEventListener('DOMContentLoaded', lockTheme);
    window.addEventListener('load', lockTheme);
    [0, 50, 150, 400, 800, 1500, 3000, 5000].forEach(function (ms) {
        setTimeout(lockTheme, ms);
    });
})();
