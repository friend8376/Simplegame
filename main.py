# -*- coding: utf-8 -*-
"""
เกมทำน้ำหอม (Perfume Maker) - ใช้แค่ tkinter ที่มากับ Python
รัน:  python main.py

วิธีเล่น
  - ลูกค้าแต่ละคนอยากได้น้ำหอมกลิ่นต่างกัน ดูแถบกลิ่นทางขวา
  - คลิกวัตถุดิบ (หรือกดเลข 1-9, 0) เพื่อหยดลงขวด ให้แถบสีไปถึงหัวใจ
  - กด "ส่งมอบ" (Enter) ก่อนลูกค้าหมดความอดทน
  - ได้ 3 ดาวติดกันจะเกิดคอมโบ ได้เงินเพิ่ม
  - มีสูตรลับ 5 สูตรซ่อนอยู่ ลองผสมวัตถุดิบ 3 อย่างที่เข้ากันดู (กด R เปิดสมุดสูตร)
  - ก่อนเริ่มเลือกเจ้าของร้านได้ 4 ตัว แต่ละตัวมีความสามารถพิเศษ
  - จบวันต้องจ่ายค่าเช่าร้าน ถ้าเงินไม่พอร้านจะปิด
"""
import json
import math
import os
import random
import time
import tkinter as tk

SAVE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "perfume_save.json")

W, H = 1000, 680
FONT = "Tahoma"

# ---------------------------------------------------------------- สี
BG = "#fff1f7"
PANEL = "#ffffff"
LINE = "#f7b9d3"
TEXT = "#6b4a6e"
SOFT = "#a98bab"
PINK = "#ff8fb8"
MINT = "#7ed6b8"
GOLD = "#ffc94d"
DARK = "#4a3550"

NOTES = ["ดอกไม้", "ส้ม", "ไม้", "หวาน", "สดชื่น"]
NOTE_COLORS = ["#ff8fb8", "#ffb347", "#b98a5e", "#c9a0f5", "#5fd0c0"]

# ชื่อ, สี, ราคาต่อหยด, กลิ่น [ดอกไม้, ส้ม, ไม้, หวาน, สดชื่น], รูปทรง, ปลดล็อกวันที่
INGREDIENTS = [
    ("กุหลาบ",       "#ff9ebb", 3, [3, 0, 0, 1, 0], "flower6", 1),
    ("มะนาว",        "#f4ec6a", 1, [0, 3, 0, 0, 1], "citrus",  1),
    ("ไม้จันทน์",     "#c99b72", 4, [0, 0, 3, 0, 0], "wood",    1),
    ("วานิลลา",      "#fff0c2", 2, [0, 0, 0, 3, 0], "cream",   1),
    ("มินต์",        "#8fe0a6", 1, [0, 0, 0, 0, 3], "leaf",    1),
    ("ลาเวนเดอร์",   "#b9a0f0", 2, [1, 0, 0, 0, 2], "flower5", 1),
    ("ส้มเขียวหวาน",  "#ffb45c", 1, [0, 2, 0, 1, 0], "citrus",  2),
    ("มะลิ",         "#ffffff", 3, [2, 0, 0, 0, 1], "flower8", 3),
    ("ซีดาร์",       "#dcb48c", 3, [0, 0, 2, 0, 1], "wood",    4),
    ("มัสก์",         "#e6d5ea", 4, [0, 0, 1, 2, 0], "cloud",   5),
]

# ชื่อ, คำขอ, เป้าหมายกลิ่น, สีผม, ทรงผม, สีเสื้อ
CUSTOMERS = [
    ("คุณมาลี",    "อยากได้กลิ่นดอกไม้หวานๆ ไปงานแต่งงานค่ะ", [5, 0, 0, 3, 1], "#7a4b3a", "bun",     "#ffb3cf"),
    ("ลุงสมชาย",   "ขอกลิ่นไม้หอมเข้มๆ แบบสุภาพบุรุษ",        [0, 1, 5, 1, 1], "#9a9a9a", "short",   "#9db8e8"),
    ("น้องฟ้า",     "อยากได้กลิ่นซัมเมอร์ ส้มๆ สดชื่น!",        [0, 4, 0, 1, 3], "#3d3350", "pigtail", "#a8e6f0"),
    ("คุณนภา",     "กลิ่นหวานละมุนไว้ฉีดก่อนนอนค่ะ",          [1, 0, 1, 5, 1], "#5b3a55", "long",    "#d9c2f5"),
    ("พี่ต้น",      "กลิ่นสะอาดๆ ไว้ใช้หลังออกกำลังกาย",        [1, 1, 0, 0, 5], "#2f2a3a", "cap",     "#b5ecc4"),
    ("คุณหญิงแก้ว", "ดอกไม้ผสมไม้ หรูหราลึกลับหน่อยนะ",        [4, 0, 3, 1, 0], "#c9c1d6", "bun",     "#c7a4e0"),
    ("น้องมิว",     "ขอแบบหวานซ่าส้มๆ น่ารักๆ ค่า",            [0, 3, 0, 3, 1], "#e9a15b", "pigtail", "#ffd3a3"),
    ("คุณเอก",     "อยากได้แบบสมดุล มีทุกกลิ่นเลยครับ",        [2, 2, 2, 2, 2], "#3a2c2c", "short",   "#f5e19a"),
    ("ป้าบุญ",      "กลิ่นดอกไม้เย็นๆ ผ่อนคลายจ้ะ",            [3, 0, 0, 1, 4], "#b9b0b0", "bun",     "#b6e3d4"),
    ("คุณเจมส์",    "กลิ่นไม้สดชื่นเหมือนเดินป่าสน",            [0, 1, 4, 0, 3], "#c98a4b", "cap",     "#a9d6a0"),
    ("น้องพลอย",   "ดอกไม้กับส้ม สดใสเหมือนตอนเช้า",          [3, 3, 0, 1, 1], "#4a2f4f", "long",    "#ffc2d6"),
    ("อาจารย์วิทย์", "ไม้หอมอุ่นๆ หวานนิดๆ เวลาอ่านหนังสือ",    [0, 0, 4, 3, 1], "#55504f", "short",   "#d8c3a5"),
]

# สูตรลับ: ถ้าในขวดมีวัตถุดิบครบทั้งสามอย่าง จะได้โบนัส  (ชื่อ, วัตถุดิบ, คำใบ้)
RECIPES = [
    ("รักแรกพบ",        {"กุหลาบ", "วานิลลา", "มัสก์"},       "ดอกไม้สีแดง ของหวาน และความนุ่มเหมือนก้อนเมฆ"),
    ("เช้าวันอาทิตย์",    {"มะนาว", "มินต์", "ลาเวนเดอร์"},     "เปรี้ยวสดชื่น ใบไม้เย็นๆ และดอกไม้สีม่วง"),
    ("ป่าหลังฝน",        {"ซีดาร์", "มินต์", "ไม้จันทน์"},      "ไม้สองชนิดกับใบไม้เขียวสด"),
    ("ขนมยามบ่าย",      {"ส้มเขียวหวาน", "วานิลลา", "มะลิ"},  "ส้มหวาน ครีมนุ่มๆ และดอกไม้สีขาว"),
    ("ฝันดีนะ",          {"ลาเวนเดอร์", "วานิลลา", "ไม้จันทน์"}, "ดอกไม้ช่วยหลับ ของหวาน และไม้หอมอุ่นๆ"),
]
NAME_IDX = {ing[0]: i for i, ing in enumerate(INGREDIENTS)}

# เจ้าของร้าน: ชื่อ, ชนิด, สีขน, สีผ้ากันเปื้อน, ความสามารถ, คำอธิบาย
KEEPERS = [
    ("โมจิ",  "กระต่าย", "#fffafc", "#ffb3cf", "patience",
     "ใจดีชวนคุยเก่ง\nลูกค้าอดทนนานขึ้น 40%"),
    ("เนโกะ", "แมว",    "#ffd59e", "#a8e6f0", "money",
     "หัวการค้า\nเริ่มด้วยเงิน 180฿\nค่าเช่าร้านถูกลง 20%"),
    ("ฮันนี่", "หมี",     "#c99b72", "#ffe08a", "tip",
     "ยิ้มหวานเรียกทิป\nทิปและโบนัสคอมโบ x2"),
    ("คิตสึ",  "จิ้งจอก", "#ffa66b", "#c9b6e8", "recipe",
     "นักปรุงสูตรลับ\nโบนัสสูตรลับ x2\nสมุดสูตรบอกวัตถุดิบ 1 อย่าง"),
]

MAX_DROPS = 12
CUSTOMERS_PER_DAY = 5
RECIPE_BONUS = 25


# ---------------------------------------------------------------- ตัวช่วย
def normalize(vec):
    total = sum(vec)
    return [v / total for v in vec] if total else [0.0] * len(vec)


def similarity(a, b):
    pa, pb = normalize(a), normalize(b)
    diff = sum(abs(x - y) for x, y in zip(pa, pb)) / 2
    return max(0, round((1 - diff) * 100))


def stars_for(score):
    return 3 if score >= 90 else 2 if score >= 75 else 1 if score >= 55 else 0


def shade(color, f):
    r, g, b = (int(color[i:i + 2], 16) for i in (1, 3, 5))
    if f <= 1:
        r, g, b = r * f, g * f, b * f
    else:
        r, g, b = (r + (255 - r) * (f - 1) for r in (r, g, b)) if False else (
            r + (255 - r) * (f - 1), g + (255 - g) * (f - 1), b + (255 - b) * (f - 1))
    return "#%02x%02x%02x" % (int(min(255, r)), int(min(255, g)), int(min(255, b)))


def mix_color(drops):
    if not drops:
        return "#eef6ff"
    r = g = b = 0
    for idx in drops:
        c = INGREDIENTS[idx][1]
        r += int(c[1:3], 16)
        g += int(c[3:5], 16)
        b += int(c[5:7], 16)
    n = len(drops)
    return shade("#%02x%02x%02x" % (r // n, g // n, b // n), 0.93)


def rent_for(day):
    return 40 + 25 * day + 3 * day * day


def load_save():
    try:
        with open(SAVE_PATH, encoding="utf-8") as f:
            data = json.load(f)
        return data if isinstance(data, dict) else {}
    except (OSError, ValueError):
        return {}


# ---------------------------------------------------------------- เกม
class PerfumeGame:
    def __init__(self, root):
        self.root = root
        root.title("ร้านน้ำหอมมหัศจรรย์")
        root.resizable(False, False)
        self.c = tk.Canvas(root, width=W, height=H, bg=BG, highlightthickness=0)
        self.c.pack()
        self.c.bind("<Button-1>", self.on_click)
        self.c.bind("<Motion>", self.on_move)
        root.bind("<Key>", self.on_key)

        self.mouse = (-1, -1)
        self.hot = []            # [(x0, y0, x1, y1, callback)]
        self.particles = []
        self.t = 0.0
        self.last = time.time()
        self.save = load_save()
        self.found = {r[0] for r in RECIPES} & set(self.save.get("found", []))
        self.keeper_idx = 0
        self.state = "title"
        self.book_prev = "play"
        self.reset_game()
        self.loop()

    # ------------------------------------------------------------ บันทึก
    def write_save(self):
        self.save["found"] = sorted(self.found)
        try:
            with open(SAVE_PATH, "w", encoding="utf-8") as f:
                json.dump(self.save, f, ensure_ascii=False, indent=1)
        except OSError:
            pass

    def best(self, idx=None):
        name = KEEPERS[self.keeper_idx if idx is None else idx][0]
        return self.save.get("best", {}).get(name, 0)

    # ------------------------------------------------------------ สถานะ
    def perk(self):
        return KEEPERS[self.keeper_idx][4]

    def rent(self, day):
        r = rent_for(day)
        return int(r * 0.8) if self.perk() == "money" else r

    def reset_game(self):
        self.day = 1
        self.money = 180 if self.perk() == "money" else 100
        self.combo = 0
        self.new_record = False
        self.drops = []
        self.customer = CUSTOMERS[0]
        self.served = 0
        self.day_income = 0
        self.time_max = self.time_left = 45
        self.enter_t = 1.0
        self.msg = ""
        self.msg_t = 0
        self.result = None
        self.dayinfo = None

    def start_game(self):
        self.reset_game()
        self.start_day()

    def start_day(self):
        self.queue = random.sample(CUSTOMERS, CUSTOMERS_PER_DAY)
        self.served = 0
        self.day_income = 0
        self.next_customer()

    def next_customer(self):
        self.customer = self.queue[self.served]
        self.drops = []
        patience = max(22, 48 - 3 * self.day)
        if self.perk() == "patience":
            patience *= 1.4
        self.time_max = self.time_left = patience
        self.enter_t = 0.0
        self.state = "play"

    def unlocked(self, idx):
        return INGREDIENTS[idx][5] <= self.day

    def base_price(self):
        return 60 + 5 * (self.day - 1)

    def drop_cost(self):
        return sum(INGREDIENTS[i][2] for i in self.drops)

    def profile(self):
        vec = [0] * len(NOTES)
        for i in self.drops:
            for k, v in enumerate(INGREDIENTS[i][3]):
                vec[k] += v
        return vec

    def score(self):
        return similarity(self.profile(), self.customer[2]) if self.drops else 0

    def find_recipe(self):
        names = {INGREDIENTS[i][0] for i in self.drops}
        for name, need in RECIPES:
            if need <= names:
                return name
        return None

    # ------------------------------------------------------------ การกระทำ
    def say(self, msg):
        self.msg, self.msg_t = msg, 1.4

    def add_drop(self, idx):
        if self.state != "play" or not self.unlocked(idx):
            return
        if len(self.drops) >= MAX_DROPS:
            self.say("ขวดเต็มแล้วจ้า!")
            return
        self.drops.append(idx)
        color = INGREDIENTS[idx][1]
        self.particles.append(dict(kind="drop", x=500, y=150, vy=520, color=shade(color, 0.9)))
        for _ in range(6):
            self.particles.append(dict(
                kind="bubble", x=500 + random.uniform(-70, 70), y=468,
                vy=-random.uniform(40, 90), r=random.uniform(2, 5), life=3))

    def undo(self):
        if self.state == "play" and self.drops:
            self.drops.pop()

    def clear(self):
        if self.state == "play":
            self.drops = []

    def burst(self, x, y, kind, n, colors):
        for _ in range(n):
            a = random.uniform(0, math.tau)
            sp = random.uniform(60, 220)
            self.particles.append(dict(
                kind=kind, x=x, y=y, vx=math.cos(a) * sp, vy=math.sin(a) * sp - 80,
                life=random.uniform(0.8, 1.6), size=random.uniform(6, 12),
                color=random.choice(colors)))

    def submit(self):
        if self.state != "play":
            return
        if len(self.drops) < 3:
            self.say("ใส่อย่างน้อย 3 หยดนะ")
            return
        score = self.score()
        stars = stars_for(score)
        cost = self.drop_cost()
        lines = []
        price = int(self.base_price() * [0, 0.6, 1.2, 1.8][stars])
        lines.append(("ค่าน้ำหอม", price))
        total = price
        honey = 2 if self.perk() == "tip" else 1
        if stars >= 2:
            tip = int(20 * honey * self.time_left / self.time_max)
            if tip:
                lines.append(("ทิปทำไว", tip))
                total += tip
        if score >= 97:
            lines.append(("เพอร์เฟกต์!", 20))
            total += 20
        if stars == 3:
            self.combo += 1
            if self.combo > 1:
                bonus = int(price * 0.1 * min(self.combo - 1, 5)) * honey
                lines.append((f"คอมโบ x{self.combo}", bonus))
                total += bonus
        else:
            self.combo = 0
        recipe = self.find_recipe() if stars >= 1 else None
        new_recipe = False
        if recipe:
            new_recipe = recipe not in self.found
            self.found.add(recipe)
            if new_recipe:
                self.write_save()
            bonus = RECIPE_BONUS * (2 if self.perk() == "recipe" else 1)
            lines.append((f"สูตรลับ \"{recipe}\"", bonus))
            total += bonus
        lines.append(("ต้นทุนวัตถุดิบ", -cost))
        profit = total - cost
        comment = ["ไม่ใช่กลิ่นที่อยากได้เลย...", "อืม พอใช้ได้อยู่นะ",
                   "หอมจัง ชอบมากเลย!", "ว้าว! ใช่เลย กลิ่นนี้แหละ!"][stars]
        self.finish(dict(score=score, stars=stars, lines=lines, profit=profit,
                         comment=comment, recipe=recipe, new_recipe=new_recipe))

    def timeout(self):
        cost = self.drop_cost()
        self.combo = 0
        self.finish(dict(score=0, stars=0, lines=[("วัตถุดิบที่เสียไป", -cost)],
                         profit=-cost, comment="รอนานไป... ขอตัวก่อนนะ",
                         recipe=None, new_recipe=False, left=True))

    def finish(self, result):
        self.result = result
        self.result_t = 0.0
        self.money += result["profit"]
        self.day_income += result["profit"]
        self.state = "result"
        if result["stars"] >= 2:
            self.burst(840, 140, "heart", 8 * result["stars"], ["#ff8fb8", "#ffb3cf", "#ff6f9f"])
        if result["stars"] == 3:
            self.burst(500, 300, "spark", 30, [GOLD, "#fff2a8", "#ffd9ec", MINT])

    def continue_game(self):
        if self.state == "result":
            self.served += 1
            if self.served >= CUSTOMERS_PER_DAY:
                self.end_day()
            else:
                self.next_customer()
        elif self.state == "dayend":
            self.day += 1
            self.start_day()
        elif self.state == "title":
            self.state = "select"
        elif self.state in ("select", "gameover"):
            self.start_game()

    def pick_keeper(self, idx):
        if self.keeper_idx == idx:
            self.start_game()
        else:
            self.keeper_idx = idx

    def open_book(self):
        if self.state in ("play", "dayend"):
            self.book_prev = self.state
            self.state = "book"

    def close_book(self):
        if self.state == "book":
            self.state = self.book_prev
            self.last = time.time()

    def end_day(self):
        rent = self.rent(self.day)
        self.money -= rent
        new = [ing[0] for ing in INGREDIENTS if ing[5] == self.day + 1]
        self.dayinfo = dict(income=self.day_income, rent=rent, new=new)
        self.drops = []
        name = KEEPERS[self.keeper_idx][0]
        best = self.save.setdefault("best", {})
        self.new_record = self.day > best.get(name, 0)
        best[name] = max(best.get(name, 0), self.day)
        self.write_save()
        if self.money < 0:
            self.state = "gameover"
        else:
            self.state = "dayend"
            self.burst(500, 250, "spark", 25, [GOLD, "#ffd9ec", MINT])

    # ------------------------------------------------------------ อินพุต
    def on_move(self, e):
        self.mouse = (e.x, e.y)

    def on_click(self, e):
        for x0, y0, x1, y1, cb in reversed(self.hot):
            if x0 <= e.x <= x1 and y0 <= e.y <= y1:
                cb()
                return

    def on_key(self, e):
        if self.state == "book":
            if e.keysym in ("Return", "KP_Enter", "space", "Escape") or e.char in ("r", "R"):
                self.close_book()
            return
        if self.state == "select":
            if e.keysym == "Left":
                self.keeper_idx = (self.keeper_idx - 1) % len(KEEPERS)
            elif e.keysym == "Right":
                self.keeper_idx = (self.keeper_idx + 1) % len(KEEPERS)
            elif e.keysym in ("Return", "KP_Enter", "space"):
                self.start_game()
            return
        if e.char in ("r", "R"):
            self.open_book()
        elif e.keysym in ("Return", "KP_Enter", "space"):
            if self.state == "play":
                self.submit()
            else:
                self.continue_game()
        elif e.keysym == "BackSpace":
            self.undo()
        elif e.keysym == "Escape":
            self.clear()
        elif e.char and e.char in "1234567890":
            self.add_drop((int(e.char) - 1) % 10)

    def hovering(self, x0, y0, x1, y1):
        mx, my = self.mouse
        return x0 <= mx <= x1 and y0 <= my <= y1

    # ------------------------------------------------------------ ลูปหลัก
    def loop(self):
        now = time.time()
        dt = min(0.1, now - self.last)
        self.last = now
        self.t += dt
        self.update(dt)
        self.draw()
        self.root.after(30, self.loop)

    def update(self, dt):
        if self.state == "play":
            self.enter_t = min(1.0, self.enter_t + dt * 2.5)
            self.time_left -= dt
            if self.time_left <= 0:
                self.time_left = 0
                self.timeout()
        elif self.state == "result":
            self.result_t += dt
        if self.msg_t > 0:
            self.msg_t -= dt
        level_y = self.liquid_top()
        alive = []
        for p in self.particles:
            k = p["kind"]
            if k == "drop":
                p["y"] += p["vy"] * dt
                if p["y"] < level_y:
                    alive.append(p)
            elif k == "bubble":
                p["y"] += p["vy"] * dt
                p["life"] -= dt
                if p["y"] > level_y + 6 and p["life"] > 0:
                    alive.append(p)
            else:
                p["x"] += p["vx"] * dt
                p["y"] += p["vy"] * dt
                p["vy"] += 160 * dt
                p["life"] -= dt
                if p["life"] > 0:
                    alive.append(p)
        self.particles = alive

    def liquid_top(self):
        n = len(self.drops)
        return 470 - (30 + 170 * n / MAX_DROPS) if n else 470

    # ------------------------------------------------------------ วาดพื้นฐาน
    def rrect(self, x0, y0, x1, y1, r, **kw):
        r = max(0, min(r, (x1 - x0) / 2, (y1 - y0) / 2))
        pts = [x0 + r, y0, x1 - r, y0, x1, y0, x1, y0 + r, x1, y1 - r, x1, y1,
               x1 - r, y1, x0 + r, y1, x0, y1, x0, y1 - r, x0, y0 + r, x0, y0]
        return self.c.create_polygon(pts, smooth=True, **kw)

    def text(self, x, y, s, size=11, bold=False, fill=TEXT, anchor="center", width=None):
        font = (FONT, size, "bold") if bold else (FONT, size)
        kw = dict(text=s, font=font, fill=fill, anchor=anchor)
        if width:
            kw["width"] = width
            kw["justify"] = "center" if anchor == "center" else "left"
        self.c.create_text(x, y, **kw)

    def heart(self, x, y, s, color, outline=""):
        pts = [x, y + s, x - s * 1.1, y - s * 0.1, x - s * 0.95, y - s * 0.8,
               x - s * 0.4, y - s * 0.95, x, y - s * 0.4, x + s * 0.4, y - s * 0.95,
               x + s * 0.95, y - s * 0.8, x + s * 1.1, y - s * 0.1]
        self.c.create_polygon(pts, smooth=True, fill=color, outline=outline)

    def star(self, x, y, r, fill, outline="#e0a400"):
        pts = []
        for i in range(10):
            a = -math.pi / 2 + i * math.pi / 5
            rr = r if i % 2 == 0 else r * 0.48
            pts += [x + math.cos(a) * rr, y + math.sin(a) * rr]
        self.c.create_polygon(pts, fill=fill, outline=outline, width=2, joinstyle="round")

    def sparkle(self, x, y, s, color):
        pts = [x, y - s, x + s * 0.25, y - s * 0.25, x + s, y, x + s * 0.25, y + s * 0.25,
               x, y + s, x - s * 0.25, y + s * 0.25, x - s, y, x - s * 0.25, y - s * 0.25]
        self.c.create_polygon(pts, fill=color, outline="")

    def face(self, x, y, s, mood="smile"):
        """หน้าน่ารัก: mood = smile / happy / neutral / sad / wow"""
        c = self.c
        blink = (self.t + x * 0.013) % 3.7 < 0.13
        ex, er = s * 0.4, s * 0.12
        for sx in (-1, 1):
            px = x + sx * ex
            c.create_oval(px - er * 1.7 + sx * s * 0.14, y + s * 0.12,
                          px + er * 1.7 + sx * s * 0.14, y + s * 0.38,
                          fill="#ffb6c9", outline="")
            if mood == "happy":
                c.create_arc(px - er * 1.4, y - er * 1.2, px + er * 1.4, y + er * 1.8,
                             start=20, extent=140, style="arc", outline=DARK, width=2)
            elif blink:
                c.create_line(px - er * 1.2, y, px + er * 1.2, y, fill=DARK, width=2)
            else:
                c.create_oval(px - er, y - er * 1.35, px + er, y + er * 1.35,
                              fill=DARK, outline="")
                c.create_oval(px - er * 0.3, y - er * 1.0, px + er * 0.5, y - er * 0.2,
                              fill="white", outline="")
        my, mw = y + s * 0.3, s * 0.2
        if mood in ("smile", "happy"):
            c.create_arc(x - mw, my - mw * 1.3, x + mw, my + mw * 0.7,
                         start=200, extent=140, style="arc", outline=DARK, width=2)
        elif mood == "sad":
            c.create_arc(x - mw, my - mw * 0.1, x + mw, my + mw * 1.7,
                         start=20, extent=140, style="arc", outline=DARK, width=2)
        elif mood == "wow":
            c.create_oval(x - mw * 0.5, my - mw * 0.5, x + mw * 0.5, my + mw * 0.7,
                          fill=DARK, outline="")
        else:
            c.create_line(x - mw * 0.7, my + mw * 0.2, x + mw * 0.7, my + mw * 0.2,
                          fill=DARK, width=2, capstyle="round")

    def button(self, x0, y0, x1, y1, label, cb, color=PINK, fg="white", size=11):
        hov = self.hovering(x0, y0, x1, y1)
        dy = -2 if hov else 0
        self.rrect(x0, y0 + 4, x1, y1 + 4, 18, fill=shade(color, 0.8), outline="")
        self.rrect(x0, y0 + dy, x1, y1 + dy, 18,
                   fill=shade(color, 1.12) if hov else color, outline="")
        self.text((x0 + x1) / 2, (y0 + y1) / 2 + dy, label, size, True, fg)
        self.hot.append((x0, y0, x1, y1 + 4, cb))

    # ------------------------------------------------------------ วาดเจ้าของร้าน
    def draw_keeper(self, x, y, s, idx, mood="smile"):
        c = self.c
        name, kind, fur, apron = KEEPERS[idx][:4]
        edge = shade(fur, 0.8) if kind != "กระต่าย" else "#f0c8d8"
        inner = "#ffc4d8"
        # หู
        if kind == "กระต่าย":
            sway = math.sin(self.t * 3 + idx) * s * 0.06
            for sx in (-1, 1):
                ex = x + sx * s * 0.42 + sway
                c.create_oval(ex - s * 0.24, y - s * 1.8, ex + s * 0.24, y - s * 0.45,
                              fill=fur, outline=edge, width=2)
                c.create_oval(ex - s * 0.11, y - s * 1.6, ex + s * 0.11, y - s * 0.7,
                              fill=inner, outline="")
        elif kind in ("แมว", "จิ้งจอก"):
            big = 1.22 if kind == "จิ้งจอก" else 1.0
            ear_in = inner if kind == "แมว" else "#7a4a3a"
            for sx in (-1, 1):
                c.create_polygon(x + sx * s * 0.9, y - s * 0.3, x + sx * s * 0.78 * big,
                                 y - s * 1.2 * big, x + sx * s * 0.18, y - s * 0.78,
                                 fill=fur, outline=edge, width=2, joinstyle="round")
                c.create_polygon(x + sx * s * 0.72, y - s * 0.48, x + sx * s * 0.7 * big,
                                 y - s * 0.98 * big, x + sx * s * 0.38, y - s * 0.74,
                                 fill=ear_in, outline="")
        else:
            for sx in (-1, 1):
                ex, ey = x + sx * s * 0.72, y - s * 0.7
                c.create_oval(ex - s * 0.32, ey - s * 0.32, ex + s * 0.32, ey + s * 0.32,
                              fill=fur, outline=edge, width=2)
                c.create_oval(ex - s * 0.16, ey - s * 0.16, ex + s * 0.16, ey + s * 0.16,
                              fill=inner, outline="")
        # ตัวและผ้ากันเปื้อน
        self.rrect(x - s * 0.85, y + s * 0.7, x + s * 0.85, y + s * 1.9, s * 0.5,
                   fill=fur, outline=edge, width=2)
        self.rrect(x - s * 0.55, y + s * 0.95, x + s * 0.55, y + s * 1.9, s * 0.25,
                   fill=apron, outline=shade(apron, 0.85), width=2)
        self.heart(x, y + s * 1.4, s * 0.14, "white")
        # หัว
        c.create_oval(x - s, y - s * 0.9, x + s, y + s * 0.95, fill=fur, outline=edge, width=2)
        if kind == "จิ้งจอก":
            c.create_polygon(x - s * 0.92, y + s * 0.15, x, y + s * 0.35, x + s * 0.92,
                             y + s * 0.15, x + s * 0.6, y + s * 0.75, x, y + s * 0.93,
                             x - s * 0.6, y + s * 0.75, smooth=True, fill="white", outline="")
        elif kind == "หมี":
            c.create_oval(x - s * 0.34, y + s * 0.12, x + s * 0.34, y + s * 0.62,
                          fill="#f3dcc4", outline="")
        elif kind == "แมว":
            for sx in (-1, 1):
                for dy in (0.18, 0.3):
                    c.create_line(x + sx * s * 0.6, y + s * dy, x + sx * s * 0.95,
                                  y + s * (dy - 0.04 + 0.08 * (dy > 0.2)), fill=edge, width=1.5)
        self.face(x, y + s * 0.05, s * 0.85, mood)
        c.create_oval(x - s * 0.07, y + s * 0.13, x + s * 0.07, y + s * 0.23,
                      fill="#e96a9b" if kind != "หมี" else "#5a3d3d", outline="")

    # ------------------------------------------------------------ วาดวัตถุดิบ
    def icon(self, x, y, r, idx, mood="smile"):
        c = self.c
        name, color, _, _, kind, _ = INGREDIENTS[idx]
        edge = shade(color, 0.78)
        if kind.startswith("flower"):
            n = int(kind[6:])
            for k in range(n):
                a = k * math.tau / n + self.t * 0.25
                px, py = x + math.cos(a) * r * 0.72, y + math.sin(a) * r * 0.72
                pr = r * (0.5 if n <= 6 else 0.4)
                c.create_oval(px - pr, py - pr, px + pr, py + pr, fill=color, outline=edge)
            cr = r * 0.62
            c.create_oval(x - cr, y - cr, x + cr, y + cr, fill="#fff6c9", outline="#f0d77a")
            self.face(x, y - 1, cr * 1.05, mood)
        elif kind == "citrus":
            c.create_oval(x - r * 0.1, y - r * 1.35, x + r * 0.75, y - r * 0.8,
                          fill="#8fd694", outline="#5fb86a")
            c.create_oval(x - r, y - r, x + r, y + r, fill=color, outline=edge, width=2)
            c.create_oval(x - r * 0.65, y - r * 0.75, x - r * 0.2, y - r * 0.4,
                          fill=shade(color, 1.5), outline="")
            self.face(x, y, r * 0.9, mood)
        elif kind == "wood":
            self.rrect(x - r * 1.15, y - r * 0.72, x + r * 1.15, y + r * 0.72, r * 0.6,
                       fill=color, outline=edge, width=2)
            c.create_oval(x + r * 0.55, y - r * 0.6, x + r * 1.1, y + r * 0.6,
                          fill=shade(color, 1.35), outline=edge)
            c.create_oval(x + r * 0.72, y - r * 0.28, x + r * 0.94, y + r * 0.28,
                          fill="", outline=edge)
            self.face(x - r * 0.25, y - r * 0.05, r * 0.72, mood)
        elif kind == "cream":
            c.create_oval(x - r * 0.3, y - r * 1.2, x + r * 0.3, y - r * 0.6,
                          fill=color, outline=edge)
            c.create_oval(x - r * 0.65, y - r * 0.9, x + r * 0.65, y - r * 0.05,
                          fill=color, outline=edge)
            c.create_oval(x - r, y - r * 0.45, x + r, y + r, fill=color, outline=edge, width=2)
            self.face(x, y + r * 0.2, r * 0.8, mood)
        elif kind == "leaf":
            c.create_polygon(x, y - r * 1.35, x + r * 1.15, y - r * 0.1, x, y + r * 1.15,
                             x - r * 1.15, y - r * 0.1, smooth=True, fill=color,
                             outline=edge, width=2)
            c.create_line(x, y - r * 0.95, x, y - r * 0.5, fill=edge, width=2)
            self.face(x, y + r * 0.1, r * 0.8, mood)
        else:  # cloud
            for dx, dy, rr in ((-0.55, 0.15, 0.62), (0.55, 0.15, 0.62), (0, -0.3, 0.75), (0, 0.3, 0.6)):
                c.create_oval(x + (dx - rr) * r, y + (dy - rr) * r,
                              x + (dx + rr) * r, y + (dy + rr) * r, fill=color, outline=edge)
            for dx, dy, rr in ((-0.55, 0.15, 0.55), (0.55, 0.15, 0.55), (0, -0.3, 0.68), (0, 0.3, 0.55)):
                c.create_oval(x + (dx - rr) * r, y + (dy - rr) * r,
                              x + (dx + rr) * r, y + (dy + rr) * r, fill=color, outline="")
            self.face(x, y + r * 0.05, r * 0.8, mood)

    def draw_shelf(self):
        self.rrect(14, 70, 306, 668, 26, fill=PANEL, outline=LINE, width=2)
        self.text(160, 88, "ชั้นวัตถุดิบ", 12, True)
        active = self.state == "play"
        for i, (name, color, cost, notes, kind, day) in enumerate(INGREDIENTS):
            col, row = i % 2, i // 2
            x0, y0 = 22 + col * 142, 106 + row * 111
            x1, y1 = x0 + 134, y0 + 103
            if not self.unlocked(i):
                self.rrect(x0, y0, x1, y1, 18, fill="#f6eef3", outline="#ead9e3", width=2)
                self.text((x0 + x1) / 2, y0 + 38, "?", 24, True, "#d8c3d0")
                self.text((x0 + x1) / 2, y0 + 78, f"ปลดล็อกวันที่ {day}", 9, False, SOFT)
                continue
            hov = active and self.hovering(x0, y0, x1, y1)
            dy = -3 if hov else 0
            self.rrect(x0, y0 + 4, x1, y1 + 4, 18, fill="#f6d5e3", outline="")
            self.rrect(x0, y0 + dy, x1, y1 + dy, 18,
                       fill="#fff8fb" if hov else "#fffdfe",
                       outline=PINK if hov else LINE, width=2)
            wig = math.sin(self.t * 9) * 3 if hov else 0
            self.icon((x0 + x1) / 2 + wig, y0 + 36 + dy, 19, i, "happy" if hov else "smile")
            self.text(x0 + 14, y0 + 13 + dy, str((i + 1) % 10), 8, True, SOFT)
            self.rrect(x1 - 36, y0 + 5 + dy, x1 - 6, y0 + 23 + dy, 9, fill="#fff0c2", outline="")
            self.text(x1 - 21, y0 + 14 + dy, f"{cost}฿", 8, True, "#b07a00")
            self.text((x0 + x1) / 2, y0 + 71 + dy, name, 10, True)
            dots = [NOTE_COLORS[k] for k, v in enumerate(notes) for _ in range(v)]
            dx = (x0 + x1) / 2 - (len(dots) - 1) * 6
            for k, colr in enumerate(dots):
                self.c.create_oval(dx + k * 12 - 4, y0 + 86 + dy, dx + k * 12 + 4, y0 + 94 + dy,
                                   fill=colr, outline="")
            if active:
                self.hot.append((x0, y0, x1, y1, lambda i=i: self.add_drop(i)))

    # ------------------------------------------------------------ วาดขวด
    def draw_bottle(self):
        c = self.c
        cx = 500
        score = self.score()
        bob = math.sin(self.t * 2) * 2
        top, bottom, hw = 262 + bob, 474 + bob, 100
        # เงาและดาวประกอบ
        c.create_oval(cx - 110, 480, cx + 110, 500, fill="#f6d5e3", outline="")
        for k, (sx, sy) in enumerate(((350, 236), (655, 290), (380, 330), (640, 440))):
            s = 5 + 3 * math.sin(self.t * 2.5 + k * 1.7)
            self.sparkle(sx, sy, s, "#ffd9ec" if k % 2 else "#ffe9a8")
        # ฝา
        c.create_oval(cx - 20, top - 96, cx + 20, top - 56, fill=GOLD, outline="#e0a400", width=2)
        c.create_oval(cx - 11, top - 90, cx - 2, top - 81, fill="#fff2b8", outline="")
        self.rrect(cx - 30, top - 62, cx + 30, top - 34, 8, fill=GOLD, outline="#e0a400", width=2)
        # คอขวด
        c.create_rectangle(cx - 20, top - 34, cx + 20, top + 6, fill="#f4fbff",
                           outline="#b9d8f0", width=3)
        # ตัวขวด
        self.rrect(cx - hw, top, cx + hw, bottom, 44, fill="#f4fbff", outline="")
        if self.drops:
            lt = self.liquid_top() + bob
            x0, x1, y1, r = cx - hw + 7, cx + hw - 7, bottom - 6, 30
            pts = []
            for i in range(13):
                pts += [x0 + (x1 - x0) * i / 12, lt + math.sin(self.t * 3 + i * 0.9) * 2.5]
            pts += [x1, y1 - r]
            for a in (30, 60, 90):
                pts += [x1 - r + r * math.cos(math.radians(a)), y1 - r + r * math.sin(math.radians(a))]
            pts += [x0 + r, y1]
            for a in (120, 150, 180):
                pts += [x0 + r + r * math.cos(math.radians(a)), y1 - r + r * math.sin(math.radians(a))]
            c.create_polygon(pts, fill=mix_color(self.drops), outline="")
        for p in self.particles:
            if p["kind"] == "bubble":
                r = p["r"]
                c.create_oval(p["x"] - r, p["y"] - r + bob, p["x"] + r, p["y"] + r + bob,
                              outline="white", width=1.5)
        self.rrect(cx - hw, top, cx + hw, bottom, 44, fill="", outline="#b9d8f0", width=5)
        c.create_line(cx - hw + 18, top + 34, cx - hw + 18, bottom - 60,
                      fill="white", width=5, capstyle="round")
        # โบว์
        by = top + 2
        for sx in (-1, 1):
            c.create_polygon(cx, by, cx + sx * 34, by - 16, cx + sx * 34, by + 16,
                             smooth=True, fill=PINK, outline="#e96a9b", width=2)
        c.create_oval(cx - 9, by - 9, cx + 9, by + 9, fill="#ffb3cf", outline="#e96a9b", width=2)
        # หน้า
        if self.state == "title":
            mood = "happy"
        elif not self.drops:
            mood = "smile"
        elif score >= 90:
            mood = "happy"
        elif score >= 55:
            mood = "smile"
        else:
            mood = "wow"
        self.face(cx, top + 105, 46, mood)
        # หยดที่กำลังตก
        for p in self.particles:
            if p["kind"] == "drop":
                x, y = p["x"], p["y"]
                c.create_polygon(x, y - 14, x + 8, y + 2, x, y + 10, x - 8, y + 2,
                                 smooth=True, fill=p["color"], outline=shade(p["color"], 0.8))

    def draw_center(self):
        score = self.score()
        st = stars_for(score) if self.drops else 0
        if self.msg_t > 0:
            self.text(500, 92, self.msg, 15, True, "#f06a8f")
        elif self.drops:
            col = "#3fb98f" if st == 3 else "#e59a1f" if st == 2 else "#f06a8f"
            self.text(500, 92, f"ตรงกลิ่น {score}%", 17, True, col)
        else:
            self.text(500, 92, "หยดวัตถุดิบลงขวดเลย!", 14, True, SOFT)
        for k in range(3):
            self.star(464 + k * 36, 128, 13, GOLD if k < st else "#f3e3ea",
                      "#e0a400" if k < st else "#e6cfda")
        self.draw_bottle()
        # เจ้าของร้านยืนข้างขวด
        if not self.drops:
            kmood = "smile"
        elif st == 3:
            kmood = "happy"
        elif st == 0:
            kmood = "wow"
        else:
            kmood = "smile"
        hop = abs(math.sin(self.t * 6)) * 5 if kmood == "happy" else math.sin(self.t * 2.4 + 1) * 1.5
        self.draw_keeper(352, 428 - hop, 24, self.keeper_idx, kmood)
        self.text(500, 514, f"หยด {len(self.drops)}/{MAX_DROPS}    ต้นทุน {self.drop_cost()}฿",
                  10, True, SOFT)
        counts = {}
        for i in self.drops:
            counts[INGREDIENTS[i][0]] = counts.get(INGREDIENTS[i][0], 0) + 1
        self.text(500, 537, "  ".join(f"{n}×{q}" for n, q in counts.items()), 9, False, SOFT, width=350)
        if self.state == "play":
            self.button(322, 566, 428, 606, "เอาออก 1", self.undo, "#c9b6e8", size=10)
            self.button(436, 566, 542, 606, "เททิ้ง", self.clear, "#c9b6e8", size=10)
            self.button(550, 562, 682, 610, "ส่งมอบ!", self.submit, PINK, size=13)
            self.text(500, 640, "กดเลข 1-0 เพื่อหยด · Enter ส่งมอบ · Backspace เอาออก", 8, False, SOFT)

    # ------------------------------------------------------------ วาดลูกค้า
    def draw_customer(self, x, y, cust, mood):
        c = self.c
        hair, style, shirt = cust[3], cust[4], cust[5]
        skin = "#ffe3cf"
        if style == "long":
            self.rrect(x - 54, y - 20, x + 54, y + 84, 26, fill=hair, outline="")
        if style == "pigtail":
            for sx in (-1, 1):
                c.create_oval(x + sx * 58 - 19, y - 12, x + sx * 58 + 19, y + 30, fill=hair, outline="")
                c.create_oval(x + sx * 46 - 6, y - 16, x + sx * 46 + 6, y - 4, fill=PINK, outline="")
        if style == "bun":
            c.create_oval(x - 20, y - 74, x + 20, y - 36, fill=hair, outline="")
        self.rrect(x - 50, y + 36, x + 50, y + 130, 26, fill=shirt, outline=shade(shirt, 0.85), width=2)
        c.create_oval(x - 9, y + 52, x + 9, y + 70, fill="white", outline="")
        c.create_oval(x - 50, y - 50, x + 50, y + 46, fill=hair, outline="")
        c.create_oval(x - 44, y - 42, x + 44, y + 46, fill=skin, outline="#f0c4a8", width=2)
        c.create_arc(x - 46, y - 48, x + 46, y + 30, start=12, extent=156,
                     style="chord", fill=hair, outline="")
        if style == "cap":
            c.create_arc(x - 50, y - 58, x + 50, y + 28, start=0, extent=180,
                         style="chord", fill=shirt, outline=shade(shirt, 0.8), width=2)
            self.rrect(x + 6, y - 22, x + 66, y - 10, 6, fill=shade(shirt, 0.85), outline="")
        self.face(x, y + 8, 40, mood)

    def draw_customer_panel(self):
        c = self.c
        cust = self.customer
        self.rrect(694, 70, 986, 668, 26, fill=PANEL, outline=LINE, width=2)
        score = self.score()
        frac = self.time_left / self.time_max
        if self.state == "result":
            mood = ["sad", "neutral", "smile", "happy"][self.result["stars"]]
        elif frac < 0.25:
            mood = "sad"
        elif not self.drops:
            mood = "neutral"
        elif score >= 90:
            mood = "happy"
        elif score >= 65:
            mood = "smile"
        else:
            mood = "neutral"
        ease = 1 - (1 - self.enter_t) ** 3
        cx = 840 + (1 - ease) * 260
        hop = abs(math.sin(self.t * 6)) * 6 if mood == "happy" else math.sin(self.t * 2.2) * 2
        self.draw_customer(cx, 150 - hop, cust, mood)
        # กล่องคำพูด
        self.rrect(706, 232, 974, 300, 20, fill="#fff6fa", outline=LINE, width=2)
        c.create_polygon(826, 234, 840, 220, 854, 234, fill="#fff6fa", outline=LINE, width=2)
        c.create_line(828, 234, 852, 234, fill="#fff6fa", width=3)
        self.text(840, 250, cust[0], 11, True, "#e9679a")
        self.text(840, 276, cust[1], 9, False, TEXT, width=250)
        # ความอดทน
        self.text(712, 316, "ความอดทน", 8, True, SOFT, "w")
        self.rrect(776, 310, 972, 322, 6, fill="#f6e8ef", outline="")
        if frac > 0.03:
            col = MINT if frac > 0.5 else GOLD if frac > 0.25 else "#ff7f9f"
            self.rrect(776, 310, 776 + 196 * frac, 322, 6, fill=col, outline="")
        # แถบกลิ่น
        tgt = normalize(cust[2])
        now = normalize(self.profile())
        x0, wd = 772, 172
        for k, note in enumerate(NOTES):
            y = 356 + k * 40
            self.text(712, y, note, 10, True, TEXT, "w")
            self.rrect(x0, y - 8, x0 + wd, y + 8, 8, fill="#f6e8ef", outline="")
            wn = wd * min(1, now[k] / 0.7)
            if wn > 6:
                self.rrect(x0, y - 8, x0 + wn, y + 8, 8, fill=NOTE_COLORS[k], outline="")
            tx = x0 + wd * min(1, tgt[k] / 0.7)
            close = self.drops and abs(now[k] - tgt[k]) < 0.06
            beat = 1 + 0.15 * math.sin(self.t * 8) if close else 1
            self.heart(tx, y, 8 * beat, "#ff5f93" if close else "white", "#e9679a")
        self.text(840, 556, "เติมแถบสีให้ถึงหัวใจ", 9, False, SOFT)
        self.rrect(712, 578, 968, 650, 18, fill="#fff9e8", outline="#ffe3a0", width=2)
        self.text(840, 596, f"ราคาน้ำหอมวันนี้ {self.base_price()}฿", 10, True, "#b07a00")
        self.text(840, 616, "1 ดาว ×0.6   2 ดาว ×1.2   3 ดาว ×1.8", 9, False, "#b07a00")
        self.text(840, 635, "ทำไวได้ทิป · 3 ดาวติดกันได้คอมโบ", 9, False, "#b07a00")

    # ------------------------------------------------------------ วาดส่วนบน
    def pill(self, x0, x1, label, color="#ffffff", fg=TEXT):
        self.rrect(x0, 16, x1, 52, 16, fill=color, outline=LINE, width=2)
        self.text((x0 + x1) / 2, 34, label, 10, True, fg)

    def draw_top(self):
        self.heart(30, 34, 11, PINK)
        self.text(48, 34, "ร้านน้ำหอมมหัศจรรย์", 15, True, "#e9679a", "w")
        n = min(self.served + 1, CUSTOMERS_PER_DAY)
        self.pill(290, 440, f"วันที่ {self.day} · ลูกค้า {n}/{CUSTOMERS_PER_DAY}")
        self.pill(448, 558, f"เงิน {self.money}฿", "#fff9e8", "#b07a00")
        self.pill(566, 706, f"ค่าเช่าวันนี้ {self.rent(self.day)}฿")
        if self.combo > 1:
            self.pill(714, 824, f"คอมโบ x{self.combo}", "#ffe1ec", "#e9679a")
        else:
            self.pill(714, 824, "คอมโบ -", fg=SOFT)
        hov = self.state == "play" and self.hovering(832, 16, 986, 52)
        self.pill(832, 986, f"สมุดสูตรลับ {len(self.found)}/{len(RECIPES)} (R)",
                  "#d9f5ea" if hov else "#eefaf5", "#3fa184")
        if self.state == "play":
            self.hot.append((832, 16, 986, 52, self.open_book))

    # ------------------------------------------------------------ หน้าต่างซ้อน
    def overlay(self, y0=120, y1=570):
        self.c.create_rectangle(0, 0, W, H, fill="#fff1f7", stipple="gray50", outline="")
        self.rrect(256, y0 + 8, 744, y1 + 8, 34, fill="#f6d5e3", outline="")
        self.rrect(256, y0, 744, y1, 34, fill="white", outline=PINK, width=3)

    def draw_result(self):
        r = self.result
        self.overlay()
        self.draw_customer(350, 205, self.customer, ["sad", "neutral", "smile", "happy"][r["stars"]])
        self.rrect(420, 160, 720, 240, 20, fill="#fff6fa", outline=LINE, width=2)
        self.text(570, 182, self.customer[0], 11, True, "#e9679a")
        self.text(570, 212, r["comment"], 11, True, TEXT, width=280)
        for k in range(3):
            appear = self.result_t - 0.25 * (k + 1)
            on = k < r["stars"] and appear > 0
            size = 22 + (max(0, 0.25 - appear) * 60 if on else 0)
            self.star(520 + k * 56, 282, size, GOLD if on else "#f3e3ea",
                      "#e0a400" if on else "#e6cfda")
        if not r.get("left"):
            self.text(570, 322, f"ตรงกลิ่น {r['score']}%", 11, True, SOFT)
        y = 356
        for label, amount in r["lines"]:
            self.text(330, y, label, 11, False, TEXT, "w")
            self.text(670, y, f"{amount:+d}฿", 11, True,
                      "#3fa184" if amount >= 0 else "#f06a8f", "e")
            y += 24
        self.c.create_line(330, y - 6, 670, y - 6, fill=LINE, width=2, dash=(4, 4))
        self.text(330, y + 12, "กำไร", 13, True, TEXT, "w")
        self.text(670, y + 12, f"{r['profit']:+d}฿", 15, True,
                  "#3fa184" if r["profit"] >= 0 else "#f06a8f", "e")
        if r["new_recipe"]:
            self.text(500, 498, f"ค้นพบสูตรลับใหม่: {r['recipe']}!", 10, True, "#3fa184")
        self.button(410, 514, 590, 556, "ต่อไป (Enter)", self.continue_game, PINK)

    def draw_dayend(self):
        d = self.dayinfo
        self.overlay(140, 550)
        self.text(500, 180, f"ปิดร้านวันที่ {self.day}", 18, True, "#e9679a")
        for k in range(3):
            self.sparkle(380 + k * 120, 216, 6 + 2 * math.sin(self.t * 3 + k), GOLD)
        rows = [("กำไรวันนี้", d["income"]), ("ค่าเช่าร้าน", -d["rent"])]
        y = 260
        for label, amount in rows:
            self.text(330, y, label, 12, False, TEXT, "w")
            self.text(670, y, f"{amount:+d}฿", 12, True,
                      "#3fa184" if amount >= 0 else "#f06a8f", "e")
            y += 30
        self.c.create_line(330, y - 8, 670, y - 8, fill=LINE, width=2, dash=(4, 4))
        self.text(330, y + 12, "เงินคงเหลือ", 13, True, TEXT, "w")
        self.text(670, y + 12, f"{self.money}฿", 15, True, "#b07a00", "e")
        if d["new"]:
            idx = [i for i, ing in enumerate(INGREDIENTS) if ing[0] == d["new"][0]][0]
            self.rrect(330, 380, 670, 450, 20, fill="#eefaf5", outline="#bfe9d9", width=2)
            self.icon(376, 415, 20, idx, "happy")
            self.text(420, 403, "วัตถุดิบใหม่มาถึงแล้ว!", 10, True, "#3fa184", "w")
            self.text(420, 427, d["new"][0], 13, True, TEXT, "w")
        else:
            self.text(500, 415, f"สูตรลับที่ค้นพบ {len(self.found)}/{len(RECIPES)}", 11, True, SOFT)
        self.text(500, 472, f"ค่าเช่าพรุ่งนี้ {self.rent(self.day + 1)}฿", 10, False, SOFT)
        self.button(300, 494, 480, 536, "สมุดสูตรลับ", self.open_book, "#c9b6e8")
        self.button(500, 494, 700, 536, "เปิดร้านวันต่อไป", self.continue_game, MINT)
        if self.new_record and self.day > 1:
            self.text(500, 160, "สถิติใหม่!", 9, True, "#3fa184")

    def draw_gameover(self):
        self.overlay(150, 530)
        self.text(500, 196, "ร้านปิดกิจการ...", 20, True, "#e9679a")
        self.draw_keeper(500, 262, 26, self.keeper_idx, "sad")
        self.text(500, 326, f"เงินไม่พอจ่ายค่าเช่า {self.dayinfo['rent']}฿", 11, False, TEXT)
        self.text(500, 360, f"เปิดร้านได้ {self.day} วัน", 16, True, TEXT)
        found = ", ".join(sorted(self.found)) or "ยังไม่พบเลย"
        self.text(500, 404, f"สูตรลับที่ค้นพบ {len(self.found)}/{len(RECIPES)}: {found}",
                  10, False, SOFT, width=400)
        name = KEEPERS[self.keeper_idx][0]
        rec = "  (สถิติใหม่!)" if self.new_record else ""
        self.text(500, 444, f"สถิติดีที่สุดของ{name} {self.best()} วัน{rec}", 10, True, "#b07a00")
        self.button(296, 470, 490, 512, "เปลี่ยนตัวละคร", self.go_select, "#c9b6e8")
        self.button(510, 470, 704, 512, "เล่นอีกครั้ง", self.continue_game, PINK)

    def go_select(self):
        self.state = "select"

    def draw_floaters(self):
        for k in range(14):
            x = (k * 83 + 40) % W
            y = (k * 137 + self.t * 14 * (1 + k % 3)) % (H + 40) - 20
            if k % 2:
                self.heart(x, y, 7 + k % 4, "#ffd9ec")
            else:
                self.sparkle(x, y, 7 + k % 4, "#ffe9a8")

    def draw_select(self):
        self.draw_floaters()
        self.text(500, 62, "เลือกเจ้าของร้าน", 24, True, "#e9679a")
        self.text(500, 100, "แต่ละคนมีความสามารถพิเศษไม่เหมือนกัน คลิกเลือก แล้วคลิกซ้ำหรือกดเริ่ม",
                  11, False, SOFT)
        for i, (name, kind, fur, apron, perk, desc) in enumerate(KEEPERS):
            x0, y0 = 70 + i * 220, 136
            x1, y1 = x0 + 200, y0 + 384
            cx = (x0 + x1) / 2
            sel = i == self.keeper_idx
            hov = self.hovering(x0, y0, x1, y1)
            dy = -8 if sel else -3 if hov else 0
            self.rrect(x0, y0 + 6, x1, y1 + 6, 26, fill="#f6d5e3", outline="")
            self.rrect(x0, y0 + dy, x1, y1 + dy, 26, fill="white" if sel else "#fffafd",
                       outline=PINK if sel else LINE, width=4 if sel else 2)
            self.c.create_oval(cx - 64, y0 + 196 + dy, cx + 64, y0 + 214 + dy,
                               fill=shade(apron, 1.25), outline="")
            bounce = abs(math.sin(self.t * 5)) * 8 if sel else 0
            self.draw_keeper(cx, y0 + 124 + dy - bounce, 44, i, "happy" if sel or hov else "smile")
            if sel:
                for k in range(3):
                    a = self.t * 1.5 + k * math.tau / 3
                    self.sparkle(cx + math.cos(a) * 80, y0 + 120 + dy + math.sin(a) * 70,
                                 6 + 2 * math.sin(self.t * 4 + k), GOLD)
            self.text(cx, y0 + 244 + dy, name, 16, True, "#e9679a" if sel else TEXT)
            self.text(cx, y0 + 270 + dy, kind, 10, False, SOFT)
            self.rrect(x0 + 12, y0 + 288 + dy, x1 - 12, y0 + 350 + dy, 14,
                       fill=shade(apron, 1.35), outline="")
            self.text(cx, y0 + 319 + dy, desc, 9, False, TEXT, width=170)
            best = self.best(i)
            self.text(cx, y0 + 367 + dy, f"สถิติ {best} วัน" if best else "ยังไม่เคยเปิดร้าน",
                      9, True, "#b07a00" if best else SOFT)
            self.hot.append((x0, y0, x1, y1, lambda i=i: self.pick_keeper(i)))
        name = KEEPERS[self.keeper_idx][0]
        self.button(370, 566, 630, 614, f"เปิดร้านกับ{name}!", self.start_game, PINK, size=14)
        self.text(500, 644, "ปุ่มลูกศร ซ้าย/ขวา เลือก · Enter เริ่ม", 9, False, SOFT)

    def draw_book(self):
        self.overlay(90, 610)
        self.text(500, 124, "สมุดสูตรลับ", 18, True, "#3fa184")
        self.text(500, 152, "ใส่วัตถุดิบ 3 อย่างในขวดเดียวกัน (ลูกค้าต้องให้อย่างน้อย 1 ดาว)",
                  9, False, SOFT)
        fox = self.perk() == "recipe"
        for k, (name, need, hint) in enumerate(RECIPES):
            y0 = 172 + k * 70
            found = name in self.found
            self.rrect(280, y0, 720, y0 + 62, 16, fill="#eefaf5" if found else "#faf6f9",
                       outline="#bfe9d9" if found else "#eee0e8", width=2)
            idxs = sorted(NAME_IDX[n] for n in need)
            if found:
                self.text(300, y0 + 20, name, 12, True, TEXT, "w")
                self.text(300, y0 + 44, " + ".join(INGREDIENTS[i][0] for i in idxs), 9, False, SOFT, "w")
                for j, i in enumerate(idxs):
                    self.icon(610 + j * 40, y0 + 32, 13, i, "happy")
            else:
                self.text(300, y0 + 20, "? ? ?", 12, True, "#d8c3d0", "w")
                self.text(300, y0 + 44, f"คำใบ้: {hint}", 9, False, SOFT, "w")
                for j in range(3):
                    if fox and j == 0:
                        self.icon(610, y0 + 32, 13, idxs[0], "smile")
                    else:
                        self.c.create_oval(610 + j * 40 - 13, y0 + 19, 610 + j * 40 + 13, y0 + 45,
                                           fill="#f3e9ef", outline="#e6d6e0")
                        self.text(610 + j * 40, y0 + 32, "?", 11, True, "#d8c3d0")
        self.button(410, 534, 590, 576, "ปิดสมุด", self.close_book, MINT)

    def draw_title(self):
        self.draw_floaters()
        self.text(500, 84, "ร้านน้ำหอมมหัศจรรย์", 30, True, "#e9679a")
        self.text(500, 128, "ผสมกลิ่นให้ถูกใจลูกค้า แล้วพาร้านให้รอดไปนานที่สุด", 12, False, SOFT)
        for k, idx in enumerate((0, 1, 4, 3, 5)):
            a = self.t * 0.8 + k * math.tau / 5
            self.icon(500 + math.cos(a) * 240, 340 + math.sin(a) * 110, 24, idx, "happy")
        self.draw_bottle()
        self.rrect(250, 520, 750, 596, 22, fill="white", outline=LINE, width=2)
        self.text(500, 544, "คลิกวัตถุดิบเพื่อหยดลงขวด เติมแถบกลิ่นให้ถึงหัวใจ แล้วกดส่งมอบ",
                  10, False, TEXT)
        self.text(500, 570, "ทำไวได้ทิป · 3 ดาวติดกันได้คอมโบ · มีสูตรลับซ่อนอยู่ 5 สูตร",
                  10, False, TEXT)
        self.button(400, 612, 600, 660, "เปิดร้าน!", self.continue_game, PINK, size=15)

    # ------------------------------------------------------------ วาดทั้งหมด
    def draw_particles(self):
        for p in self.particles:
            if p["kind"] == "heart":
                self.heart(p["x"], p["y"], p["size"] * min(1, p["life"] * 2), p["color"])
            elif p["kind"] == "spark":
                self.sparkle(p["x"], p["y"], p["size"] * min(1, p["life"] * 2), p["color"])

    def draw(self):
        self.c.delete("all")
        self.hot = []
        if self.state == "title":
            self.draw_title()
        elif self.state == "select":
            self.draw_select()
        elif self.state == "book":
            self.draw_top()
            self.draw_shelf()
            self.draw_center()
            self.draw_customer_panel()
            if self.book_prev == "dayend":
                self.draw_dayend()
            self.hot = []
            self.draw_book()
        else:
            self.draw_top()
            self.draw_shelf()
            self.draw_center()
            self.draw_customer_panel()
            if self.state == "result":
                self.draw_result()
            elif self.state == "dayend":
                self.draw_dayend()
            elif self.state == "gameover":
                self.draw_gameover()
        self.draw_particles()
        over = any(self.hovering(*h[:4]) for h in self.hot)
        self.c.config(cursor="hand2" if over else "")


if __name__ == "__main__":
    root = tk.Tk()
    PerfumeGame(root)
    root.mainloop()
