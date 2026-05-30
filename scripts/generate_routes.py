#!/usr/bin/env python3
"""Generate route detail pages and update travel.html from routes data."""

import json
import re
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ROUTES_DIR = ROOT / "routes"
IMAGES_DIR = ROOT / "images" / "routes"
UA = "CheXingTianXia/1.0 (personal travel site; contact@tahoo.me)"

ROUTES = [
    {
        "slug": "chuanzang",
        "name": "川藏线",
        "region": "西南",
        "tagline": "西南 · 国道 G318",
        "distance": "约 2,150 km",
        "duration": "7–12 天",
        "season": "5–10 月",
        "tags": ["稻城亚丁", "然乌湖", "林芝桃花"],
        "images": {
            "hero": "https://upload.wikimedia.org/wikipedia/commons/4/47/Panorama_of_Lhasa_in_1942%2C_with_the_Potala_Palace_at_the_upper_left.jpg",
            "gallery": [
                "https://upload.wikimedia.org/wikipedia/commons/thumb/a/aa/Banji_Feng_2014.jpg/1280px-Banji_Feng_2014.jpg",
                "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d7/The_Grand_Canyon_of_the_Nujiang_River%2C_Yunnan%2C_China_-_2019_May.jpg/1280px-The_Grand_Canyon_of_the_Nujiang_River%2C_Yunnan%2C_China_-_2019_May.jpg",
            ],
        },
        "map_bbox": "91.0,29.5,104.5,31.5",
        "map_marker": "29.65,91.12",
        "summary": "成都至拉萨，中国最经典的进藏公路。雪山、草原、冰川与藏式村镇在 G318 上依次展开。",
        "intro": "川藏南线（G318）是无数自驾者心中的「终极公路」。从成都平原出发，翻越折多山、海子山，经稻城亚丁、然乌湖、林芝，最终抵达圣城拉萨。全程海拔落差大，景观类型在一天之内可数次切换——这是任何其他国内线路难以复制的体验。",
        "highlights": [
            "折多山与海子山垭口，高原风光第一次冲击",
            "稻城亚丁三神山，蓝色星球上的最后香格里拉",
            "然乌湖晨雾，318 上最上镜的高原湖泊",
            "林芝桃花沟（3–4 月），藏地江南限定春色",
        ],
        "stops": [
            {"name": "成都", "km": "0", "note": "出发点，补给充足"},
            {"name": "新都桥", "km": "330", "note": "摄影天堂，光影极美"},
            {"name": "稻城亚丁", "km": "760", "note": "停留 1–2 天徒步"},
            {"name": "然乌湖", "km": "1,280", "note": "最佳拍摄清晨"},
            {"name": "林芝", "km": "1,850", "note": "低海拔休整"},
            {"name": "拉萨", "km": "2,150", "note": "终点，布达拉宫"},
        ],
        "ev_tips": [
            "高原段快充站间距较大，理塘、林芝、拉萨前务必补满电",
            "低温会明显影响续航，预留 30% 以上电量裕度",
            "部分垭口无信号，提前下载离线地图",
        ],
    },
    {
        "slug": "chuanxi",
        "name": "川西环线",
        "region": "西南",
        "tagline": "西南 · 四川",
        "distance": "约 1,800 km",
        "duration": "6–8 天",
        "season": "9–11 月",
        "tags": ["新都桥", "色达", "海子山"],
        "images": {
            "hero": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/aa/Banji_Feng_2014.jpg/1280px-Banji_Feng_2014.jpg",
            "gallery": [
                "https://upload.wikimedia.org/wikipedia/commons/thumb/c/cc/Zhangye_Danxia.JPG/1280px-Zhangye_Danxia.JPG",
                "https://upload.wikimedia.org/wikipedia/commons/f/fb/Meili_Snow_Mountains_-_R0010879.jpg",
            ],
        },
        "map_bbox": "100.0,29.0,102.5,32.0",
        "map_marker": "30.05,101.96",
        "summary": "不进藏也能看尽川西精华：四姑娘山、丹巴藏寨、新都桥、稻城亚丁。",
        "intro": "川西环线是时间有限者的最优解——把四川西部最极致的高原风光压缩进一条可循环的线路。秋季的新都桥层林尽染，色达佛学院的红房子在谷地铺展，海子山的荒原像火星表面。全程可在成都起止，无需办理边防证。",
        "highlights": ["四姑娘山双桥沟", "丹巴甲居藏寨", "新都桥光影", "稻城亚丁三神山"],
        "stops": [
            {"name": "成都", "km": "0", "note": "出发"},
            {"name": "四姑娘山", "km": "205", "note": "双桥沟游览"},
            {"name": "丹巴", "km": "360", "note": "藏寨住宿"},
            {"name": "新都桥", "km": "430", "note": "摄影核心段"},
            {"name": "稻城亚丁", "km": "780", "note": "核心景区"},
            {"name": "成都", "km": "1,800", "note": "环线返回"},
        ],
        "ev_tips": ["康定、新都桥、稻城均有快充", "折多山爬坡耗电大，上山前充满", "秋季早晚温差大，注意电池保温"],
    },
    {
        "slug": "dianzang",
        "name": "滇藏线",
        "region": "西南",
        "tagline": "西南 · 国道 G214",
        "distance": "约 1,900 km",
        "duration": "8–10 天",
        "season": "4–6、9–10 月",
        "tags": ["梅里雪山", "盐井", "香格里拉"],
        "images": {
            "hero": "https://upload.wikimedia.org/wikipedia/commons/f/fb/Meili_Snow_Mountains_-_R0010879.jpg",
            "gallery": [
                "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d7/The_Grand_Canyon_of_the_Nujiang_River%2C_Yunnan%2C_China_-_2019_May.jpg/1280px-The_Grand_Canyon_of_the_Nujiang_River%2C_Yunnan%2C_China_-_2019_May.jpg",
                "https://upload.wikimedia.org/wikipedia/commons/thumb/9/92/1_li_jiang_guilin_yangshuo_2011.jpg/1280px-1_li_jiang_guilin_yangshuo_2011.jpg",
            ],
        },
        "map_bbox": "98.0,25.0,99.5,29.0",
        "map_marker": "28.43,98.87",
        "summary": "云南大理/香格里拉入藏，梅里雪山与盐井古盐田沿途相伴。",
        "intro": "滇藏线融合了云南的多元民族文化与西藏的宗教氛围。飞来寺看梅里雪山日照金山，盐井千年古盐田仍在晒盐，香格里拉普达措的森林与湖泊是进入高原前的缓冲。相比川藏线，海拔爬升更和缓，适合首次进藏。",
        "highlights": ["梅里雪山日照金山", "千年盐井古盐田", "香格里拉普达措", "纳帕海湿地"],
        "stops": [
            {"name": "大理/丽江", "km": "0", "note": "云南段起点"},
            {"name": "香格里拉", "km": "320", "note": "高原适应"},
            {"name": "飞来寺", "km": "480", "note": "观梅里雪山"},
            {"name": "盐井", "km": "620", "note": "古盐田"},
            {"name": "芒康", "km": "780", "note": "入藏第一县"},
            {"name": "拉萨", "km": "1,900", "note": "终点"},
        ],
        "ev_tips": ["香格里拉、德钦有快充站", "梅里雪山段海拔高，注意续航", "盐井至芒康路况复杂，谨慎驾驶"],
    },
    {
        "slug": "bingchacha",
        "name": "丙察察",
        "region": "西南",
        "tagline": "西南 · 极限越野",
        "distance": "约 300 km",
        "duration": "3–5 天",
        "season": "5–10 月",
        "tags": ["怒江大峡谷", "原始森林", "高难度"],
        "images": {
            "hero": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d7/The_Grand_Canyon_of_the_Nujiang_River%2C_Yunnan%2C_China_-_2019_May.jpg/1280px-The_Grand_Canyon_of_the_Nujiang_River%2C_Yunnan%2C_China_-_2019_May.jpg",
            "gallery": [
                "https://upload.wikimedia.org/wikipedia/commons/f/fb/Meili_Snow_Mountains_-_R0010879.jpg",
                "https://upload.wikimedia.org/wikipedia/commons/thumb/a/aa/Banji_Feng_2014.jpg/1280px-Banji_Feng_2014.jpg",
            ],
        },
        "map_bbox": "97.5,27.5,98.8,28.5",
        "map_marker": "28.02,98.27",
        "summary": "丙中洛至察隅，中国最险峻的进藏短线之一，原始到令人屏息。",
        "intro": "丙察察（丙中洛—察瓦龙—察隅）是硬核越野者的朝圣路。怒江大峡谷在两侧挤压天空，原始森林与悬崖路段交替出现。300 公里可能需要 3 天以上——这不是「赶路」的线路，而是「探路」。雨季严禁通行。",
        "highlights": ["怒江第一湾", "石门关", "察瓦龙悬崖路", "察隅原始森林"],
        "stops": [
            {"name": "丙中洛", "km": "0", "note": "云南起点"},
            {"name": "石门关", "km": "45", "note": "怒江峡谷核心"},
            {"name": "察瓦龙", "km": "120", "note": "最险路段"},
            {"name": "察隅", "km": "300", "note": "西藏段终点"},
        ],
        "ev_tips": ["全程几乎无快充，不建议纯电单车挑战", "如需尝试，建议组队并携带应急充电方案", "优先选择非雨季、非夜间通行"],
    },
    {
        "slug": "qinggan",
        "name": "青甘大环线",
        "region": "西北",
        "tagline": "西北 · 青海甘肃",
        "distance": "约 2,700 km",
        "duration": "7–9 天",
        "season": "6–9 月",
        "tags": ["青海湖", "茶卡盐湖", "莫高窟"],
        "images": {
            "hero": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/cc/Zhangye_Danxia.JPG/1280px-Zhangye_Danxia.JPG",
            "gallery": [
                "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d9/Qinghai_Lake_sunset_2018-07-30.jpg/1280px-Qinghai_Lake_sunset_2018-07-30.jpg",
                "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1a/%E8%8C%B6%E5%8D%A1%E7%9B%90%E6%B9%96%E6%B9%96%E9%9D%A210.jpg/1280px-%E8%8C%B6%E5%8D%A1%E7%9B%90%E6%B9%96%E6%B9%96%E9%9D%A210.jpg",
                "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a1/Mogao_Caves.jpg/1280px-Mogao_Caves.jpg",
            ],
        },
        "map_bbox": "94.0,36.0,102.0,38.5",
        "map_marker": "36.62,100.75",
        "summary": "西宁起止的经典环线：湖、盐、沙漠、丹霞、石窟，西北精华一次看尽。",
        "intro": "青甘大环线是国内最「出片」的自驾线路之一。青海湖的蓝、茶卡盐湖的天空之镜、张掖七彩丹霞的地质奇观、敦煌莫高窟的千年文明——每天驾驶 300–400 公里，但每站都值得停留。6–8 月是最佳窗口，油菜花海与湖水同框。",
        "highlights": ["青海湖环湖", "茶卡盐湖天空之镜", "张掖七彩丹霞", "敦煌莫高窟"],
        "stops": [
            {"name": "西宁", "km": "0", "note": "环线起点"},
            {"name": "青海湖", "km": "150", "note": "环湖 1 天"},
            {"name": "茶卡盐湖", "km": "300", "note": "最佳下午光线"},
            {"name": "敦煌", "km": "1,100", "note": "莫高窟预约"},
            {"name": "张掖", "km": "1,600", "note": "丹霞日落"},
            {"name": "西宁", "km": "2,700", "note": "环线闭合"},
        ],
        "ev_tips": ["西宁、青海湖、敦煌、张掖均有超充", "柴达木盆地段间距拉大，提前规划", "夏季紫外线强，注意车内降温"],
    },
    {
        "slug": "beijiang",
        "name": "北疆环线",
        "region": "西北",
        "tagline": "西北 · 新疆",
        "distance": "约 2,500 km",
        "duration": "8–12 天",
        "season": "6–9 月",
        "tags": ["喀纳斯", "禾木村", "赛里木湖"],
        "images": {
            "hero": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d3/Outlet_from_Kanas_Lake_at_the_Xinjiang_Kanas_National_Geopark.jpg/1280px-Outlet_from_Kanas_Lake_at_the_Xinjiang_Kanas_National_Geopark.jpg",
            "gallery": [
                "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a0/Lake_Kanas.jpg/1280px-Lake_Kanas.jpg",
                "https://upload.wikimedia.org/wikipedia/commons/thumb/7/70/Karakul.jpg/1280px-Karakul.jpg",
            ],
        },
        "map_bbox": "84.0,44.0,88.5,48.5",
        "map_marker": "48.71,87.04",
        "summary": "乌鲁木齐—喀纳斯—禾木—赛里木湖，北疆秋色与湖泊森林的极致组合。",
        "intro": "北疆拥有中国最像瑞士的 landscape：喀纳斯湖的晨雾、禾木村的小木屋与白桦林、赛里木湖的高原蓝宝石。9 月秋景达到巅峰，层林尽染。线路较长，建议预留 10 天以上，慢下来才能感受北疆的安静。",
        "highlights": ["喀纳斯湖三湾", "禾木村晨雾", "赛里木湖环湖", "魔鬼城雅丹"],
        "stops": [
            {"name": "乌鲁木齐", "km": "0", "note": "新疆起点"},
            {"name": "布尔津", "km": "500", "note": "前往喀纳斯中转"},
            {"name": "喀纳斯", "km": "680", "note": "停留 2 天"},
            {"name": "禾木", "km": "720", "note": "摄影核心"},
            {"name": "赛里木湖", "km": "1,200", "note": "高原湖泊"},
            {"name": "乌鲁木齐", "km": "2,500", "note": "环线返回"},
        ],
        "ev_tips": ["乌鲁木齐、克拉玛依、伊宁充电设施较好", "喀纳斯景区内充电有限，进景区前补满", "北疆昼夜温差大，注意电池性能"],
    },
    {
        "slug": "nanjiang",
        "name": "南疆环线",
        "region": "西北",
        "tagline": "西北 · 新疆",
        "distance": "约 2,000 km",
        "duration": "8–10 天",
        "season": "4–10 月",
        "tags": ["慕士塔格峰", "盘龙古道", "喀什古城"],
        "images": {
            "hero": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/62/Kashgar%2C_China_Bebop_Drone_2015-09-13T194555%2B0000_18F943.jpg/1280px-Kashgar%2C_China_Bebop_Drone_2015-09-13T194555%2B0000_18F943.jpg",
            "gallery": [
                "https://upload.wikimedia.org/wikipedia/commons/c/c5/Mt_Kongur_Lake_Karakul_Xinjiang_China.jpg",
                "https://upload.wikimedia.org/wikipedia/commons/thumb/7/70/Karakul.jpg/1280px-Karakul.jpg",
            ],
        },
        "map_bbox": "75.0,37.0,78.0,39.5",
        "map_marker": "39.47,75.99",
        "summary": "喀什—塔县—盘龙古道，帕米尔高原与丝路南道的异域风情。",
        "intro": "南疆是另一种新疆：喀什古城的艾提尕尔清真寺、塔什库尔干的帕米尔高原、盘龙古道的 600 多个 S 弯。慕士塔格峰倒映在喀拉库勒湖面，像一幅静止的油画。这里是古丝绸之路的要冲，也是体验维吾尔与塔吉克文化的窗口。",
        "highlights": ["喀什古城", "白沙湖", "慕士塔格峰", "盘龙古道"],
        "stops": [
            {"name": "喀什", "km": "0", "note": "南疆枢纽"},
            {"name": "白沙湖", "km": "180", "note": "帕米尔门户"},
            {"name": "塔县", "km": "290", "note": "高原县城"},
            {"name": "盘龙古道", "km": "320", "note": "网红公路"},
            {"name": "和田", "km": "800", "note": "玉石之乡"},
            {"name": "喀什", "km": "2,000", "note": "环线返回"},
        ],
        "ev_tips": ["喀什、阿克苏有较好充电网络", "塔县海拔 3100m+，注意续航与高原反应", "盘龙古道弯多坡陡，控制车速"],
    },
    {
        "slug": "duku",
        "name": "独库公路",
        "region": "西北",
        "tagline": "西北 · 新疆 · G217",
        "distance": "约 561 km",
        "duration": "2–3 天",
        "season": "6–9 月",
        "tags": ["天山", "巴音布鲁克", "限定开放"],
        "images": {
            "hero": "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f0/G217_Duku.jpg/1280px-G217_Duku.jpg",
            "gallery": [
                "https://upload.wikimedia.org/wikipedia/commons/thumb/9/96/Xinjiang_Tianshan_%2854573044960%29.jpg/1280px-Xinjiang_Tianshan_%2854573044960%29.jpg",
            ],
        },
        "map_bbox": "82.5,42.0,84.5,44.5",
        "map_marker": "43.58,83.25",
        "summary": "纵贯天山的景观大道，一日穿越四季，中国公路旅行天花板之一。",
        "intro": "独库公路（G217 独山子—库车段）连接新疆南北，翻越达坂、穿过隧道，从荒漠到草原、从雪山到峡谷。铁力买提达坂、巴音布鲁克九曲十八弯、天山大峡谷——561 公里浓缩了新疆最壮丽的地貌。每年仅开放约 4 个月，通车时间与天气强相关。",
        "highlights": ["铁力买提达坂", "巴音布鲁克草原", "大小龙池", "天山大峡谷"],
        "stops": [
            {"name": "独山子", "km": "0", "note": "北线起点"},
            {"name": "乔尔玛", "km": "120", "note": "烈士陵园"},
            {"name": "巴音布鲁克", "km": "350", "note": "九曲十八弯日落"},
            {"name": "大小龙池", "km": "480", "note": "高山湖泊"},
            {"name": "库车", "km": "561", "note": "南线终点"},
        ],
        "ev_tips": ["独库公路中途充电站稀少，独山子/库车出发前务必满电", "翻越达坂续航波动大，预留充足余量", "关注官方通车公告，严禁违规穿越"],
    },
    {
        "slug": "silkroad",
        "name": "丝绸之路",
        "region": "西北",
        "tagline": "西北 · 丝路",
        "distance": "约 1,700 km",
        "duration": "6–8 天",
        "season": "5–10 月",
        "tags": ["敦煌", "嘉峪关", "张掖丹霞"],
        "images": {
            "hero": "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f4/National_cultural_heritage_stele_at_Jiayuguan_Great_Wall_%2820230919143944%29.jpg/1280px-National_cultural_heritage_stele_at_Jiayuguan_Great_Wall_%2820230919143944%29.jpg",
            "gallery": [
                "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a1/Mogao_Caves.jpg/1280px-Mogao_Caves.jpg",
                "https://upload.wikimedia.org/wikipedia/commons/thumb/c/cc/Zhangye_Danxia.JPG/1280px-Zhangye_Danxia.JPG",
            ],
        },
        "map_bbox": "94.0,36.0,109.0,40.5",
        "map_marker": "40.14,94.66",
        "summary": "西安至敦煌，沿古丝路西行，历史与荒漠风光并存。",
        "intro": "丝绸之路自驾是「读万卷书，行万里路」的具象化。嘉峪关「天下第一雄关」、敦煌莫高窟的壁画、张掖丹霞的地质奇迹——每一站都有千年故事。河西走廊相对平坦，驾驶强度低于青藏或新疆线路，更适合文化深度游。",
        "highlights": ["嘉峪关关城", "敦煌莫高窟", "鸣沙山月牙泉", "张掖七彩丹霞"],
        "stops": [
            {"name": "西安", "km": "0", "note": "丝路东起点"},
            {"name": "兰州", "km": "650", "note": "黄河铁桥"},
            {"name": "嘉峪关", "km": "1,050", "note": "天下第一雄关"},
            {"name": "敦煌", "km": "1,400", "note": "莫高窟核心"},
            {"name": "张掖", "km": "1,700", "note": "丹霞终点"},
        ],
        "ev_tips": ["西安、兰州、嘉峪关、敦煌均有超充", "河西走廊风大，注意横风与能耗", "莫高窟需提前预约，合理规划停留"],
    },
    {
        "slug": "qingzang",
        "name": "青藏线",
        "region": "西北",
        "tagline": "西北 · 国道 G109",
        "distance": "约 1,900 km",
        "duration": "5–7 天",
        "season": "5–10 月",
        "tags": ["可可西里", "纳木错", "高原公路"],
        "images": {
            "hero": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d9/Qinghai_Lake_sunset_2018-07-30.jpg/1280px-Qinghai_Lake_sunset_2018-07-30.jpg",
            "gallery": [
                "https://upload.wikimedia.org/wikipedia/commons/6/6f/Qinghai_lake.jpg",
                "https://upload.wikimedia.org/wikipedia/commons/4/47/Panorama_of_Lhasa_in_1942%2C_with_the_Potala_Palace_at_the_upper_left.jpg",
            ],
        },
        "map_bbox": "91.0,31.5,95.0,36.5",
        "map_marker": "36.62,100.75",
        "summary": "西宁至拉萨，路况最好的进藏公路，适合首次高原自驾。",
        "intro": "青藏线（G109）沿青海湖、穿越可可西里、翻越唐古拉山口，最终抵达拉萨。相比川藏线，坡度更缓、路况更好，是不少新手进藏的首选。沿途可看到藏羚羊、野牦牛——记得在可可西里保持安静，不要惊扰野生动物。",
        "highlights": ["青海湖", "可可西里", "唐古拉山口", "纳木错"],
        "stops": [
            {"name": "西宁", "km": "0", "note": "青海起点"},
            {"name": "青海湖", "km": "150", "note": "高原湖泊"},
            {"name": "格尔木", "km": "830", "note": "进藏前最后大城市"},
            {"name": "唐古拉山口", "km": "1,200", "note": "海拔 5231m"},
            {"name": "拉萨", "km": "1,900", "note": "终点"},
        ],
        "ev_tips": ["格尔木是进藏前关键补能点，务必满电", "可可西里段无快充，规划保守", "唐古拉山口海拔高，低温影响续航明显"],
    },
    {
        "slug": "xinzang",
        "name": "新藏线",
        "region": "西北",
        "tagline": "西北 · 国道 G219",
        "distance": "约 2,340 km",
        "duration": "7–10 天",
        "season": "6–9 月",
        "tags": ["界山达坂", "无人区", "极限挑战"],
        "images": {
            "hero": "https://upload.wikimedia.org/wikipedia/commons/c/c5/Mt_Kongur_Lake_Karakul_Xinjiang_China.jpg",
            "gallery": [
                "https://upload.wikimedia.org/wikipedia/commons/thumb/7/70/Karakul.jpg/1280px-Karakul.jpg",
                "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f0/G217_Duku.jpg/1280px-G217_Duku.jpg",
            ],
        },
        "map_bbox": "77.0,32.0,81.0,37.0",
        "map_marker": "35.72,77.85",
        "summary": "叶城至狮泉河，穿越昆仑山与羌塘无人区，中国海拔最高的公路之一。",
        "intro": "新藏线（G219 新疆叶城—西藏狮泉河段）是硬核中的硬核。界山达坂海拔 5248 米，长时间在 5000 米以上行驶，穿越羌塘无人区。补给点极少，路况复杂——这是给有充分准备的老司机准备的线路，而非普通旅行。",
        "highlights": ["零公里界碑", "界山达坂", "羌塘无人区", "狮泉河"],
        "stops": [
            {"name": "叶城", "km": "0", "note": "新疆起点"},
            {"name": "麻扎", "km": "120", "note": "进入山区"},
            {"name": "界山达坂", "km": "900", "note": "全程最高点"},
            {"name": "多玛", "km": "1,400", "note": "无人区中段"},
            {"name": "狮泉河", "km": "2,340", "note": "西藏终点"},
        ],
        "ev_tips": ["纯电车辆强烈不建议单独挑战新藏线", "若必须通行，需详细规划每一个补能点", "携带备用能源与卫星通讯设备"],
    },
    {
        "slug": "caoyuan",
        "name": "草原天路",
        "region": "华北",
        "tagline": "华北 · 河北",
        "distance": "约 130 km",
        "duration": "1–2 天",
        "season": "6–8 月",
        "tags": ["风车草原", "周末游", "充电便利"],
        "images": {
            "hero": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/cb/Fengning_Jing_Bei_meadow.jpg/1280px-Fengning_Jing_Bei_meadow.jpg",
            "gallery": [
                "https://upload.wikimedia.org/wikipedia/commons/thumb/0/01/Morin_Dawa%2C_Hulun_Buir%2C_Inner_Mongolia%2C_China_-_panoramio_%281%29.jpg/1280px-Morin_Dawa%2C_Hulun_Buir%2C_Inner_Mongolia%2C_China_-_panoramio_%281%29.jpg",
            ],
        },
        "map_bbox": "114.5,41.0,115.8,41.8",
        "map_marker": "41.35,115.15",
        "summary": "张北草原天路，北京周边最热门的短途自驾，风车与草原同框。",
        "intro": "草原天路位于河北张家口张北县，蜿蜒于坝上高原。夏季油菜花海、风车阵列、蒙古包点缀其间，是北京车主周末「出逃」的首选。线路不长，可结合张北音乐节或崇礼滑雪（冬季）组合游玩。充电设施完善，纯电友好。",
        "highlights": ["桦皮岭入口", "风车阵列", "油菜花海", "草原日落"],
        "stops": [
            {"name": "野狐岭", "km": "0", "note": "西线入口"},
            {"name": "桦皮岭", "km": "65", "note": "制高点"},
            {"name": "张北", "km": "130", "note": "东线终点"},
        ],
        "ev_tips": ["北京至张北全程高速，充电便利", "周末车流大，建议错峰出行", "夏季防晒，草原无遮阴"],
    },
    {
        "slug": "ejina",
        "name": "额济纳胡杨林",
        "region": "华北",
        "tagline": "华北 · 内蒙古",
        "distance": "视起点而定",
        "duration": "3–5 天",
        "season": "9 月下旬–10 月",
        "tags": ["胡杨林", "居延海", "秋季限定"],
        "images": {
            "hero": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7d/%E5%86%85%E8%92%99_%E9%A2%9D%E6%B5%8E%E7%BA%B3_%E6%80%AA%E6%A0%91%E6%9E%97-%E3%80%90%E8%83%A1%E6%9D%A8%E6%A0%91%E2%80%9C%E6%AD%BB%E8%80%8C%E5%8D%83%E5%B9%B4%E4%B8%8D%E5%80%92%E3%80%81%E5%80%92%E8%80%8C%E5%8D%83%E5%B9%B4%E4%B8%8D%E6%9C%BD%E2%80%9D%E3%80%91_-_panoramio.jpg/1280px-%E5%86%85%E8%92%99_%E9%A2%9D%E6%B5%8E%E7%BA%B3_%E6%80%AA%E6%A0%91%E6%9E%97-%E3%80%90%E8%83%A1%E6%9D%A8%E6%A0%91%E2%80%9C%E6%AD%BB%E8%80%8C%E5%8D%83%E5%B9%B4%E4%B8%8D%E5%80%92%E3%80%81%E5%80%92%E8%80%8C%E5%8D%83%E5%B9%B4%E4%B8%8D%E6%9C%BD%E2%80%9D%E3%80%91_-_panoramio.jpg",
            "gallery": [
                "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f4/National_cultural_heritage_stele_at_Jiayuguan_Great_Wall_%2820230919143944%29.jpg/1280px-National_cultural_heritage_stele_at_Jiayuguan_Great_Wall_%2820230919143944%29.jpg",
            ],
        },
        "map_bbox": "99.0,40.5,101.5,42.5",
        "map_marker": "41.95,101.07",
        "summary": "内蒙古额济纳旗，中国最美胡杨林之一，一年仅约 20 天黄金期。",
        "intro": "额济纳胡杨林是中国秋景的「天花板」之一。九月底至十月中旬，二道桥、四道桥、八道桥的胡杨变成一片金黄，与沙漠、倒影、牧群构成极致画面。怪树林的枯死胡杨「千年不倒」，又是另一种苍凉美学。可与嘉峪关、张掖串联成丝路秋游线。",
        "highlights": ["二道桥倒影", "四道桥英雄林", "八道桥沙漠", "怪树林"],
        "stops": [
            {"name": "达来呼布", "km": "0", "note": "旗府驻地"},
            {"name": "二道桥", "km": "25", "note": "晨拍倒影"},
            {"name": "四道桥", "km": "35", "note": "核心林区"},
            {"name": "八道桥", "km": "50", "note": "沙漠日落"},
            {"name": "怪树林", "km": "60", "note": "枯胡杨"},
        ],
        "ev_tips": ["旺季住宿紧张，提前预订", "酒泉、嘉峪关可作为补能中转", "沙漠段注意沙尘对充电口的影响"],
    },
    {
        "slug": "hulunbeier",
        "name": "呼伦贝尔大草原",
        "region": "东北",
        "tagline": "东北 · 内蒙古",
        "distance": "约 1,000 km",
        "duration": "5–7 天",
        "season": "6–8 月",
        "tags": ["莫日格勒河", "满洲里", "边境风光"],
        "images": {
            "hero": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/01/Morin_Dawa%2C_Hulun_Buir%2C_Inner_Mongolia%2C_China_-_panoramio_%281%29.jpg/1280px-Morin_Dawa%2C_Hulun_Buir%2C_Inner_Mongolia%2C_China_-_panoramio_%281%29.jpg",
            "gallery": [
                "https://upload.wikimedia.org/wikipedia/commons/thumb/9/91/Hulun_Lake.jpg/1280px-Hulun_Lake.jpg",
                "https://upload.wikimedia.org/wikipedia/commons/thumb/c/cb/Fengning_Jing_Bei_meadow.jpg/1280px-Fengning_Jing_Bei_meadow.jpg",
            ],
        },
        "map_bbox": "116.0,48.0,120.5,50.5",
        "map_marker": "49.21,119.75",
        "summary": "海拉尔—额尔古纳—满洲里，中国最美草原之一，夏季绿草如茵。",
        "intro": "呼伦贝尔是中国保存最完好的草原之一。莫日格勒河的九曲蜿蜒、额尔古纳湿地的中俄边境、满洲里的俄式风情——这里的天际线低而辽阔，适合把节奏放慢，在蒙古包里看一次草原日出。6–8 月是最佳季节，冬季则可体验那达慕与冰雪那达慕。",
        "highlights": ["莫日格勒河", "额尔古纳湿地", "白桦林", "满洲里国门"],
        "stops": [
            {"name": "海拉尔", "km": "0", "note": "呼伦贝尔门户"},
            {"name": "额尔古纳", "km": "200", "note": "湿地与白桦林"},
            {"name": "室韦", "km": "350", "note": "中俄边境小镇"},
            {"name": "满洲里", "km": "500", "note": "俄式风情"},
            {"name": "海拉尔", "km": "1,000", "note": "环线返回"},
        ],
        "ev_tips": ["海拉尔、满洲里有快充", "草原深处充电站少，出发前满电", "夏季蚊虫多，注意车内通风"],
    },
    {
        "slug": "dongbei",
        "name": "东北边境线",
        "region": "东北",
        "tagline": "东北 · 边境",
        "distance": "约 1,200 km",
        "duration": "6–8 天",
        "season": "9–10 月",
        "tags": ["长白山", "延吉美食", "图们江"],
        "images": {
            "hero": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/64/Changbai_Shan_2008-06-14_IMG_1526a.jpg/1280px-Changbai_Shan_2008-06-14_IMG_1526a.jpg",
            "gallery": [
                "https://upload.wikimedia.org/wikipedia/commons/7/72/Fenghuang_Ancient_Town.jpg",
            ],
        },
        "map_bbox": "124.0,41.5,130.5,43.5",
        "map_marker": "42.05,128.05",
        "summary": "丹东—长白山—延吉—珲春，鸭绿江与天池构成的东北边境走廊。",
        "intro": "东北边境线串联了鸭绿江断桥、长白山天池、图们江口岸与延吉朝鲜族美食。9–10 月秋色斑斓，长白山天池在晴朗天气下蓝得令人心醉。延吉的冷面、烤肉、米肠是自驾途中最好的慰藉——这座「小首尔」值得专门停留一天。",
        "highlights": ["鸭绿江断桥", "长白山天池", "图们口岸", "延吉美食"],
        "stops": [
            {"name": "丹东", "km": "0", "note": "鸭绿江起点"},
            {"name": "长白山", "km": "400", "note": "北坡/西坡"},
            {"name": "延吉", "km": "650", "note": "美食之都"},
            {"name": "珲春", "km": "900", "note": "三国交界"},
            {"name": "丹东", "km": "1,200", "note": "环线返回"},
        ],
        "ev_tips": ["沈阳、长春、延吉充电网络完善", "长白山景区内充电有限", "冬季极寒，非冬季出行更推荐"],
    },
    {
        "slug": "wannan",
        "name": "皖南川藏线",
        "region": "华东",
        "tagline": "华东 · 安徽",
        "distance": "约 120 km",
        "duration": "2–3 天",
        "season": "3–5、9–11 月",
        "tags": ["青龙湾", "水墨汀溪", "周末首选"],
        "images": {
            "hero": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/16/Gate_of_Hongcun_Scenario_Area%2C_Anhui%2C_China.jpg/1280px-Gate_of_Hongcun_Scenario_Area%2C_Anhui%2C_China.jpg",
            "gallery": [
                "https://upload.wikimedia.org/wikipedia/commons/thumb/6/66/Mt_Banner_and_Thousand_Island_Lake.jpg/1280px-Mt_Banner_and_Thousand_Island_Lake.jpg",
            ],
        },
        "map_bbox": "118.0,30.0,119.2,30.8",
        "map_marker": "30.35,118.55",
        "summary": "宁国至泾县，江南版川藏线，竹海、梯田与古村落。",
        "intro": "皖南川藏线（又称「江南天路」）位于安徽宁国至泾县之间，全程约 120 公里，弯道密集、风景秀丽。青龙湾的碧水、水墨汀溪的竹林、查济与桃花潭的古村——这是长三角车主最方便的「小川藏」，周末即可往返。",
        "highlights": ["青龙湾", "储家滩", "水墨汀溪", "查济古村"],
        "stops": [
            {"name": "宁国", "km": "0", "note": "东入口"},
            {"name": "青龙湾", "km": "20", "note": "湖光山色"},
            {"name": "水墨汀溪", "km": "60", "note": "竹林核心"},
            {"name": "泾县", "km": "120", "note": "西终点"},
        ],
        "ev_tips": ["上海/杭州/南京出发均可一日到达", "全程充电便利，纯电友好", "弯多路窄，注意会车"],
    },
    {
        "slug": "qiandaohu",
        "name": "千岛湖环湖",
        "region": "华东",
        "tagline": "华东 · 浙江",
        "distance": "约 150 km",
        "duration": "2–3 天",
        "season": "4–6、9–11 月",
        "tags": ["湖光山色", "骑行徒步", "充电方便"],
        "images": {
            "hero": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/66/Mt_Banner_and_Thousand_Island_Lake.jpg/1280px-Mt_Banner_and_Thousand_Island_Lake.jpg",
            "gallery": [
                "https://upload.wikimedia.org/wikipedia/commons/thumb/1/16/Gate_of_Hongcun_Scenario_Area%2C_Anhui%2C_China.jpg/1280px-Gate_of_Hongcun_Scenario_Area%2C_Anhui%2C_China.jpg",
            ],
        },
        "map_bbox": "118.5,29.3,119.5,29.8",
        "map_marker": "29.60,119.03",
        "summary": "杭州周边最成熟的环湖自驾，碧水千岛，适合休闲慢游。",
        "intro": "千岛湖因新安江水库而成，1078 个岛屿散落湖面。环湖公路路况极佳，隧道与桥梁串联各景点，适合「不赶路」的休闲自驾。可搭配骑行、皮划艇、森林氧吧，是长三角纯电出行的标杆线路——充电站密度高，焦虑为零。",
        "highlights": ["中心湖区", "东南湖区", "森林氧吧", "环湖骑行道"],
        "stops": [
            {"name": "千岛湖镇", "km": "0", "note": "主镇"},
            {"name": "梅峰观岛", "km": "25", "note": "俯瞰全湖"},
            {"name": "龙山岛", "km": "40", "note": "海瑞祠"},
            {"name": "千岛湖镇", "km": "150", "note": "环湖完成"},
        ],
        "ev_tips": ["环湖充电站密集，纯电首选线路", "可与杭州组合，西湖+千岛湖 3 日游", "旺季住宿提前预订"],
    },
    {
        "slug": "hainan",
        "name": "海南环岛",
        "region": "华南",
        "tagline": "华南 · 海南",
        "distance": "约 800 km",
        "duration": "5–7 天",
        "season": "11 月–次年 3 月",
        "tags": ["三亚", "万宁", "环岛旅游公路"],
        "images": {
            "hero": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/29/Beaches_in_Sanya%2C_Hainan%2C_China2.jpg/1280px-Beaches_in_Sanya%2C_Hainan%2C_China2.jpg",
            "gallery": [
                "https://upload.wikimedia.org/wikipedia/commons/thumb/2/29/Beaches_in_Sanya%2C_Hainan%2C_China2.jpg/1280px-Beaches_in_Sanya%2C_Hainan%2C_China2.jpg",
            ],
        },
        "map_bbox": "108.5,18.0,111.0,20.5",
        "map_marker": "18.25,109.51",
        "summary": "椰风海韵的环岛之旅，冬季避寒自驾首选。",
        "intro": "海南环岛旅游公路于 2023 年全线贯通，串联海口、文昌、万宁、三亚、儋州。冬季北方寒冷时，海南仍是温暖如春——三亚的亚龙湾、万宁的日月湾冲浪、海口的骑楼老街，构成一条「反季节」的完美环线。纯电环岛的充电焦虑在海南几乎不存在。",
        "highlights": ["三亚亚龙湾", "万宁日月湾", "文昌东郊椰林", "海口骑楼老街"],
        "stops": [
            {"name": "海口", "km": "0", "note": "环岛起点"},
            {"name": "文昌", "km": "80", "note": "东郊椰林"},
            {"name": "万宁", "km": "200", "note": "日月湾"},
            {"name": "三亚", "km": "350", "note": "核心停留"},
            {"name": "海口", "km": "800", "note": "环岛闭合"},
        ],
        "ev_tips": ["海南充电网络全国领先，纯电友好", "冬季为旺季，机票与酒店需提前订", "注意防晒与台风季（7–9 月）"],
    },
    {
        "slug": "guilin",
        "name": "桂林山水线",
        "region": "华南",
        "tagline": "华南 · 广西",
        "distance": "约 300 km",
        "duration": "3–5 天",
        "season": "4–10 月",
        "tags": ["漓江", "阳朔", "龙脊梯田"],
        "images": {
            "hero": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/92/1_li_jiang_guilin_yangshuo_2011.jpg/1280px-1_li_jiang_guilin_yangshuo_2011.jpg",
            "gallery": [
                "https://upload.wikimedia.org/wikipedia/commons/thumb/6/66/Mt_Banner_and_Thousand_Island_Lake.jpg/1280px-Mt_Banner_and_Thousand_Island_Lake.jpg",
            ],
        },
        "map_bbox": "109.5,24.5,110.8,26.0",
        "map_marker": "25.27,110.29",
        "summary": "桂林—阳朔—龙脊，中国山水美学的代表线路。",
        "intro": "「桂林山水甲天下，阳朔山水甲桂林」。漓江的喀斯特峰林、阳朔西街的夜晚、龙脊梯田的层层曲线——这条线路是中国风景审美的原点。适合慢游：竹筏漂流、骑行十里画廊、在梯田旁住一晚，感受晨雾中的壮族村寨。",
        "highlights": ["漓江竹筏", "阳朔西街", "十里画廊", "龙脊梯田"],
        "stops": [
            {"name": "桂林", "km": "0", "note": "起点"},
            {"name": "阳朔", "km": "65", "note": "核心停留"},
            {"name": "龙脊梯田", "km": "120", "note": "平安寨/金坑"},
            {"name": "桂林", "km": "300", "note": "返回"},
        ],
        "ev_tips": ["桂林、阳朔均有超充", "龙脊山路弯陡，注意电量与驾驶", "4–5 月灌水季梯田最美"],
    },
    {
        "slug": "zhangjiajie",
        "name": "张家界—凤凰古城",
        "region": "华中",
        "tagline": "华中 · 湖南",
        "distance": "约 230 km",
        "duration": "4–6 天",
        "season": "4–5、9–10 月",
        "tags": ["天门山", "凤凰古城", "武陵源"],
        "images": {
            "hero": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/62/1_zhangjiajie_huangshizhai_wulingyuan_panorama_2012.jpg/1280px-1_zhangjiajie_huangshizhai_wulingyuan_panorama_2012.jpg",
            "gallery": [
                "https://upload.wikimedia.org/wikipedia/commons/7/72/Fenghuang_Ancient_Town.jpg",
                "https://upload.wikimedia.org/wikipedia/commons/thumb/4/47/Zhangjiajie_National_Forest_Park.jpg/1280px-Zhangjiajie_National_Forest_Park.jpg",
            ],
        },
        "map_bbox": "109.5,27.8,110.8,29.5",
        "map_marker": "29.13,110.48",
        "summary": "奇峰怪石与沱江夜景，湘西最经典的自然+人文组合。",
        "intro": "张家界武陵源是《阿凡达》哈利路亚山的原型，三千奇峰拔地而起；天门山的玻璃栈道与 99 弯盘山公路考验胆量。驱车 230 公里至凤凰古城，沱江边的吊脚楼在夜晚亮起灯光——这是湘西最经典的组合线路。",
        "highlights": ["武陵源", "天门山", "玻璃栈道", "凤凰古城夜景"],
        "stops": [
            {"name": "张家界", "km": "0", "note": "武陵源 2 天"},
            {"name": "天门山", "km": "15", "note": "索道/盘山公路"},
            {"name": "凤凰古城", "km": "230", "note": "沱江夜景"},
        ],
        "ev_tips": ["张家界市区充电便利", "山区气温低于平原，注意续航", "凤凰古城步行为主，车停城外"],
    },
    {
        "slug": "enshi",
        "name": "恩施大峡谷",
        "region": "华中",
        "tagline": "华中 · 湖北",
        "distance": "视路线而定",
        "duration": "3–5 天",
        "season": "4–10 月",
        "tags": ["屏山峡谷", "土司城", "小众秘境"],
        "images": {
            "hero": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/bf/Enshi_Grand_Canyon_20240725.jpg/1280px-Enshi_Grand_Canyon_20240725.jpg",
            "gallery": [
                "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d7/The_Grand_Canyon_of_the_Nujiang_River%2C_Yunnan%2C_China_-_2019_May.jpg/1280px-The_Grand_Canyon_of_the_Nujiang_River%2C_Yunnan%2C_China_-_2019_May.jpg",
            ],
        },
        "map_bbox": "108.5,29.5,110.5,31.0",
        "map_marker": "30.28,109.48",
        "summary": "湖北恩施，地缝、绝壁与浮桥，被称为「中国仙本那」。",
        "intro": "恩施大峡谷集天坑、地缝、绝壁、峰丛于一体，屏山峡谷的「悬浮船」照片火遍全网。这里是湖北的隐藏秘境，游客密度远低于张家界。土司城展示土家族文化，女儿城的夜市适合品尝合渣与腊肉。",
        "highlights": ["恩施大峡谷", "屏山峡谷", "土司城", "女儿城"],
        "stops": [
            {"name": "恩施市区", "km": "0", "note": "枢纽"},
            {"name": "恩施大峡谷", "km": "45", "note": "核心景区"},
            {"name": "屏山峡谷", "km": "120", "note": "鹤峰县"},
            {"name": "土司城", "km": "5", "note": "市区内"},
        ],
        "ev_tips": ["恩施市区有快充", "屏山峡谷需预约，限流", "山路多雾，谨慎驾驶"],
    },
    {
        "slug": "qiandongnan",
        "name": "黔东南苗寨线",
        "region": "华中",
        "tagline": "华中 · 贵州",
        "distance": "约 600 km",
        "duration": "5–7 天",
        "season": "4–10 月",
        "tags": ["西江苗寨", "荔波", "镇远古镇"],
        "images": {
            "hero": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/19/Xijiang_Miao_Village.jpg/1280px-Xijiang_Miao_Village.jpg",
            "gallery": [
                "https://upload.wikimedia.org/wikipedia/commons/thumb/b/bf/Enshi_Grand_Canyon_20240725.jpg/1280px-Enshi_Grand_Canyon_20240725.jpg",
                "https://upload.wikimedia.org/wikipedia/commons/7/72/Fenghuang_Ancient_Town.jpg",
            ],
        },
        "map_bbox": "107.0,25.5,109.5,27.0",
        "map_marker": "26.58,108.18",
        "summary": "贵阳—凯里—西江—荔波，苗寨灯火与喀斯特山水。",
        "intro": "黔东南是贵州民族文化的核心。西江千户苗寨的万家灯火、荔波小七孔的碧水森林、镇远古镇的舞阳河——这条线路把人文与自然编织在一起。酸汤鱼、长桌宴、芦笙舞，是路上最好的文化体验。",
        "highlights": ["西江千户苗寨", "荔波小七孔", "镇远古镇", "肇兴侗寨"],
        "stops": [
            {"name": "贵阳", "km": "0", "note": "贵州起点"},
            {"name": "凯里", "km": "180", "note": "苗侗门户"},
            {"name": "西江苗寨", "km": "220", "note": "夜景必看"},
            {"name": "荔波", "km": "400", "note": "小七孔"},
            {"name": "镇远", "km": "550", "note": "古镇停留"},
        ],
        "ev_tips": ["贵阳、凯里、荔波充电较完善", "苗寨内停车有限，建议停外围", "贵州山路多，注意能耗"],
    },
]


def download(url: str, dest: Path) -> str:
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists() and dest.stat().st_size > 5000:
        return str(dest.relative_to(ROOT)).replace("\\", "/")
    last_err = None
    for attempt in range(5):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=90) as resp:
                data = resp.read()
            if len(data) < 1000:
                raise ValueError("image too small")
            dest.write_bytes(data)
            return str(dest.relative_to(ROOT)).replace("\\", "/")
        except Exception as e:
            last_err = e
            import time
            time.sleep(2 * (attempt + 1))
    raise last_err


def esc(s: str) -> str:
    return (
        s.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def render_detail(route: dict, paths: dict) -> str:
    hero = paths["hero"]
    gallery_html = "".join(
        f'<figure class="detail-gallery-item"><img src="../{p}" alt="{esc(route["name"])}"><figcaption>{esc(route["name"])}</figcaption></figure>'
        for p in paths["gallery"]
    )
    highlights_html = "".join(f"<li>{esc(h)}</li>" for h in route["highlights"])
    stops_html = "".join(
        f'<div class="route-stop"><span class="route-stop-num">{i+1}</span><div><strong>{esc(s["name"])}</strong><span class="route-stop-km">{esc(s["km"])}</span><p>{esc(s["note"])}</p></div></div>'
        for i, s in enumerate(route["stops"])
    )
    ev_html = "".join(f"<li>{esc(t)}</li>" for t in route["ev_tips"])
    tags_html = "".join(f'<span class="route-tag">{esc(t)}</span>' for t in route["tags"])
    lat, lon = route["map_marker"].split(",")
    bbox = route["map_bbox"]
    map_src = f"https://www.openstreetmap.org/export/embed.html?bbox={bbox}&layer=mapnik&marker={lat}%2C{lon}"

    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="darkreader-lock">
    <style id="theme-lock">
      html {{ color-scheme: only dark; background: #0a0a0a; color: #f5f5f7; }}
      body {{ background: #0a0a0a; color: #f5f5f7; }}
      .hero-title, .detail-hero .hero-title {{ color: #fff !important; -webkit-text-fill-color: #fff !important; }}
      .hero-subtitle, .detail-hero .hero-subtitle {{ color: rgba(255,255,255,.9) !important; -webkit-text-fill-color: rgba(255,255,255,.9) !important; }}
      .detail-stat-val, .detail-stat-lbl {{ color: #fff !important; -webkit-text-fill-color: #fff !important; }}
      .detail-lead-text {{ color: #f5f5f7 !important; -webkit-text-fill-color: #f5f5f7 !important; }}
    </style>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="color-scheme" content="dark">
    <title>{esc(route["name"])} — 车行天下</title>
    <meta name="description" content="{esc(route["summary"])}">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;700&family=Playfair+Display:ital,wght@0,400;0,700;1,400&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="../styles.css?v=3">
    <link rel="stylesheet" href="../route-detail.css?v=3">
</head>
<body>

<nav class="nav" id="nav">
    <a href="../index.html" class="nav-logo">车行<span>天下</span></a>
    <ul class="nav-links" id="navLinks">
        <li><a href="../index.html">首页</a></li>
        <li><a href="../travel.html" class="active">自驾游</a></li>
        <li><a href="../index.html#vehicle">我的座驾</a></li>
        <li><a href="../index.html#care">养护指南</a></li>
        <li><a href="../index.html#about">关于</a></li>
    </ul>
    <button class="nav-toggle" id="navToggle" aria-label="菜单">
        <svg width="24" height="24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 6h16M4 12h16M4 18h16"/></svg>
    </button>
</nav>

<section class="detail-hero">
    <div class="detail-hero-bg" style="background-image:url('../{hero}')"></div>
    <div class="hero-overlay"></div>
    <div class="detail-hero-content">
        <a href="../travel.html" class="detail-back">← 返回路线列表</a>
        <span class="hero-eyebrow">{esc(route["tagline"])}</span>
        <h1 class="hero-title">{esc(route["name"])}</h1>
        <p class="hero-subtitle">{esc(route["summary"])}</p>
        <div class="detail-stats">
            <div><span class="detail-stat-val">{esc(route["distance"])}</span><span class="detail-stat-lbl">总里程</span></div>
            <div><span class="detail-stat-val">{esc(route["duration"])}</span><span class="detail-stat-lbl">建议天数</span></div>
            <div><span class="detail-stat-val">{esc(route["season"])}</span><span class="detail-stat-lbl">最佳季节</span></div>
        </div>
    </div>
</section>

<article class="detail-body">
    <div class="detail-inner">
        <div class="detail-lead">
            <p class="detail-lead-text">{esc(route["intro"])}</p>
            <div class="route-highlights detail-tags">{tags_html}</div>
        </div>

        <section class="detail-section">
            <p class="section-eyebrow">Photo Essay</p>
            <h2 class="section-title">沿途影像</h2>
            <div class="detail-gallery">{gallery_html}</div>
        </section>

        <section class="detail-section">
            <p class="section-eyebrow">Highlights</p>
            <h2 class="section-title">不可错过</h2>
            <ul class="detail-list">{highlights_html}</ul>
        </section>

        <section class="detail-section detail-split">
            <div>
                <p class="section-eyebrow">Itinerary</p>
                <h2 class="section-title">途经站点</h2>
                <div class="route-stops">{stops_html}</div>
            </div>
            <div>
                <p class="section-eyebrow">Map Guide</p>
                <h2 class="section-title">路线地图</h2>
                <div class="detail-map-wrap">
                    <iframe class="detail-map" title="{esc(route["name"])}地图" src="{map_src}" loading="lazy"></iframe>
                </div>
                <p class="detail-map-note">基于 OpenStreetMap。出发前请结合最新导航与路况信息。</p>
                <a class="detail-map-link" href="https://www.openstreetmap.org/?bbox={bbox}" target="_blank" rel="noopener">在 OpenStreetMap 中打开 ↗</a>
            </div>
        </section>

        <section class="detail-section detail-ev">
            <p class="section-eyebrow">EV Tips</p>
            <h2 class="section-title">新能源出行提示</h2>
            <p class="section-desc">驾驶腾势 N7 等纯电 SUV 出发前，请特别注意以下事项：</p>
            <ul class="detail-list detail-ev-list">{ev_html}</ul>
        </section>
    </div>
</article>

<section class="detail-nav-bottom">
    <div class="detail-inner detail-nav-inner">
        <a href="../travel.html" class="btn btn-ghost">← 全部路线</a>
    </div>
</section>

<footer class="footer">
    <div class="footer-inner">
        <div>
            <div class="footer-brand">车行<span>天下</span></div>
            <p class="footer-desc">新能源自驾与用车笔记。驾驶腾势 N7，探索中国之美。</p>
        </div>
        <div class="footer-links">
            <div class="footer-col">
                <h4>栏目</h4>
                <ul>
                    <li><a href="../travel.html">自驾游</a></li>
                    <li><a href="../index.html#vehicle">我的座驾</a></li>
                    <li><a href="../index.html#care">养护指南</a></li>
                </ul>
            </div>
        </div>
    </div>
    <div class="footer-bottom"><p>© 2026 车行天下 · tahoo.me</p></div>
</footer>

<script src="../theme-guard.js"></script>
<script>
    const nav = document.getElementById('nav');
    window.addEventListener('scroll', () => nav.classList.toggle('scrolled', window.scrollY > 50));
    document.getElementById('navToggle').addEventListener('click', () => document.getElementById('navLinks').classList.toggle('open'));
</script>
</body>
</html>"""


def render_travel_card(route: dict, thumb: str) -> str:
    tags = "".join(f'<span class="route-tag">{esc(t)}</span>' for t in route["tags"])
    return f"""
            <a href="routes/{route["slug"]}.html" class="route-card route-card-link" data-region="{esc(route["region"])}">
                <div class="route-card-image">
                    <img src="{thumb}" alt="{esc(route["name"])}">
                </div>
                <div class="route-card-body">
                    <p class="route-card-region">{esc(route["tagline"])}</p>
                    <h3 class="route-card-title">{esc(route["name"])}</h3>
                    <p class="route-card-desc">{esc(route["summary"])}</p>
                    <div class="route-meta">
                        <span class="route-meta-item"><strong>里程</strong> {esc(route["distance"])}</span>
                        <span class="route-meta-item"><strong>建议</strong> {esc(route["duration"])}</span>
                        <span class="route-meta-item"><strong>最佳</strong> {esc(route["season"])}</span>
                    </div>
                    <div class="route-highlights">{tags}</div>
                    <span class="route-card-cta">查看详情 →</span>
                </div>
            </a>"""


def main():
    ROUTES_DIR.mkdir(exist_ok=True)
    IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    card_html = []

    for route in ROUTES:
        slug = route["slug"]
        slug_dir = IMAGES_DIR / slug
        hero_path = download(route["images"]["hero"], slug_dir / "hero.jpg")
        gallery_paths = []
        for i, url in enumerate(route["images"]["gallery"]):
            gallery_paths.append(download(url, slug_dir / f"gallery-{i+1}.jpg"))

        paths = {"hero": hero_path, "gallery": gallery_paths}
        detail_path = ROUTES_DIR / f"{slug}.html"
        detail_path.write_text(render_detail(route, paths), encoding="utf-8")
        card_html.append(render_travel_card(route, hero_path))
        print(f"OK {slug}")

    travel_path = ROOT / "travel.html"
    content = travel_path.read_text(encoding="utf-8")
    new_grid = "\n".join(card_html) + "\n"
    content = re.sub(
        r'(<div class="route-grid" id="routeGrid">).*?(</div>\s*</div>\s*</section>)',
        rf'\1{new_grid}        \2',
        content,
        count=1,
        flags=re.DOTALL,
    )
    content = content.replace(
        "background-image: url('https://images.unsplash.com/photo-1469854523086-cc02fe5d8800?w=1920&q=80');",
        f"background-image: url('{ROUTES[7]['slug'] and 'images/routes/duku/hero.jpg'}');",
    )
    # fix hero - use duku or qinggan hero for travel page
    content = re.sub(
        r"(class=\"page-hero\">[\s\S]*?background-image: url\(')[^']+('\);)",
        r"\1images/routes/qinggan/hero.jpg\2",
        content,
        count=1,
    )
    content = re.sub(
        r"(class=\"quote-banner-bg\" style=\"background-image: url\(')[^']+('\);)",
        r"\1images/routes/chuanzang/hero.jpg\2",
        content,
        count=1,
    )
    travel_path.write_text(content, encoding="utf-8")
    print("Updated travel.html")


if __name__ == "__main__":
    main()
