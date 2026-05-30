/* Restore light text if a browser extension overrides colors after load. */
(function () {
    var rules = [
        ['.detail-hero .hero-title, .detail-hero .hero-eyebrow, .detail-stat-val', '#ffffff'],
        ['.detail-hero .hero-subtitle', 'rgba(255,255,255,0.9)'],
        ['.detail-stat-lbl, .detail-back', 'rgba(255,255,255,0.85)'],
        ['.detail-lead-text', '#f5f5f7'],
        ['.hero .hero-title, section.hero .hero-title', '#ffffff'],
        ['.hero .hero-subtitle, section.hero .hero-subtitle', 'rgba(255,255,255,0.9)']
    ];

    function isDarkColor(value) {
        var match = value && value.match(/rgba?\(\s*(\d+)/);
        return match ? parseInt(match[1], 10) < 128 : false;
    }

    function fixTextColors() {
        rules.forEach(function (rule) {
            document.querySelectorAll(rule[0]).forEach(function (el) {
                if (isDarkColor(getComputedStyle(el).color)) {
                    el.style.setProperty('color', rule[1], 'important');
                    el.style.setProperty('-webkit-text-fill-color', rule[1], 'important');
                }
            });
        });
    }

    fixTextColors();
    new MutationObserver(fixTextColors).observe(document.documentElement, {
        subtree: true,
        attributes: true,
        attributeFilter: ['style', 'class'],
        childList: true
    });
    document.addEventListener('DOMContentLoaded', fixTextColors);
    window.addEventListener('load', fixTextColors);
    [50, 200, 800, 2000].forEach(function (ms) {
        setTimeout(fixTextColors, ms);
    });
})();
