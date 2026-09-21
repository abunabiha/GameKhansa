"""
Konstanta dan konfigurasi global untuk game Mobil Legend (GameKhansa)
"""

# Dimensi Layar
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 650
FPS = 60

# Dimensi Jalan
ROAD_WIDTH = 460
ROAD_LEFT = (SCREEN_WIDTH - ROAD_WIDTH) // 2
ROAD_RIGHT = ROAD_LEFT + ROAD_WIDTH
NUM_LANES = 4
LANE_WIDTH = ROAD_WIDTH // NUM_LANES
LANE_CENTERS = [ROAD_LEFT + int((i + 0.5) * LANE_WIDTH) for i in range(NUM_LANES)]

# Palet Warna Retro / Arcade (RGB)
COLOR_BLACK = (15, 15, 20)
COLOR_WHITE = (245, 245, 250)
COLOR_ASPHALT = (45, 48, 55)
COLOR_ASPHALT_LINE = (235, 235, 240)
COLOR_GRASS = (34, 139, 34)
COLOR_GRASS_DARK = (28, 115, 28)
COLOR_CURB_RED = (220, 40, 40)
COLOR_CURB_WHITE = (240, 240, 240)

# Warna UI & Efek
COLOR_GOLD = (255, 215, 0)
COLOR_NITRO_CYAN = (0, 235, 255)
COLOR_HEALTH_GREEN = (46, 204, 113)
COLOR_HEALTH_RED = (231, 76, 60)
COLOR_PANEL_BG = (20, 22, 30, 220)
COLOR_TEXT_SHADOW = (10, 10, 15)

# Definisi Kendaraan Pilihan (Mobil Balap & Tank Tempur)
CARS_DATA = {
    "merah_kilat": {
        "type": "car",
        "name": "Si Merah Kilat",
        "description": "Mobil balap lincah, akselerasi gesit + Nitro Turbo",
        "primary_color": (230, 35, 45),
        "stripe_color": (255, 255, 255),
        "glow_color": (255, 75, 75),
        "max_speed": 17.5,
        "accel": 0.26,
        "handling": 5.8,
        "max_hp": 100,
        "nitro_duration": 180,
    },
    "garuda_hitam": {
        "type": "car",
        "name": "Garuda Hitam",
        "description": "Muscle car kokoh, bodi tahan tabrakan + Nitro",
        "primary_color": (35, 38, 45),
        "stripe_color": (255, 185, 0),
        "glow_color": (255, 140, 0),
        "max_speed": 16.8,
        "accel": 0.23,
        "handling": 5.0,
        "max_hp": 150,
        "nitro_duration": 150,
    },
    "cyber_khansa": {
        "type": "car",
        "name": "Cyber Khansa",
        "description": "Hypercar masa depan, kapasitas nitro ekstra besar",
        "primary_color": (20, 130, 245),
        "stripe_color": (0, 255, 210),
        "glow_color": (0, 230, 255),
        "max_speed": 18.5,
        "accel": 0.25,
        "handling": 5.4,
        "max_hp": 90,
        "nitro_duration": 250,
    },
    "badak_baja": {
        "type": "tank",
        "name": "Tank Badak Baja",
        "description": "Tank tempur lapis baja, tembak meriam hancurkan musuh!",
        "primary_color": (65, 85, 50),
        "stripe_color": (40, 52, 32),
        "glow_color": (130, 180, 80),
        "max_speed": 16.2,
        "accel": 0.24,
        "handling": 4.6,
        "max_hp": 250,
        "cannon_cooldown": 18,
    },
    "titan_khansa": {
        "type": "tank",
        "name": "Tank Titan Khansa",
        "description": "Super tank futuristik dengan meriam plasma ganda!",
        "primary_color": (42, 50, 70),
        "stripe_color": (0, 220, 255),
        "glow_color": (0, 230, 255),
        "max_speed": 17.6,
        "accel": 0.26,
        "handling": 4.8,
        "max_hp": 300,
        "cannon_cooldown": 15,
    }
}

# Tipe Lalu Lintas
TRAFFIC_TYPES = [
    {
        "type": "sedan",
        "name": "Sedan Biru",
        "width": 38,
        "height": 70,
        "speed": 6.0,
        "color": (40, 120, 220),
        "roof_color": (30, 90, 170)
    },
    {
        "type": "taxi",
        "name": "Taksi Kuning",
        "width": 38,
        "height": 70,
        "speed": 7.0,
        "color": (245, 195, 20),
        "roof_color": (210, 165, 15)
    },
    {
        "type": "sports",
        "name": "Sport Hijau",
        "width": 40,
        "height": 72,
        "speed": 9.0,
        "color": (35, 200, 90),
        "roof_color": (25, 160, 70)
    },
    {
        "type": "truck",
        "name": "Truk Kargo",
        "width": 46,
        "height": 110,
        "speed": 4.5,
        "color": (190, 95, 40),
        "roof_color": (160, 80, 35)
    }
]

# State Permainan
STATE_MENU = "MENU"
STATE_GARAGE = "GARAGE"
STATE_PLAYING = "PLAYING"
STATE_PAUSED = "PAUSED"
STATE_GAMEOVER = "GAMEOVER"
STATE_NAME_INPUT = "NAME_INPUT"
STATE_CONFIRM_DELETE = "CONFIRM_DELETE"

# Mode Edukasi Permainan
EDU_MODE_MATH = "MATH"
EDU_MODE_VOCAB = "VOCAB"

# Kata-Kata Motivasi Pembelajaran Ramah Anak
MOTIVATION_TEMPLATES = [
    "🌟 HEBAT SEKALI, {name}! KAMU SANGAT PINTAR!",
    "🔥 LUAR BIASA {name}! PRESTASIMU MEMBANGGAKAN!",
    "🎯 TEPAT SEKALI! KAMU CALON JUARA DUNIA!",
    "✨ CERDAS DAN TANGKAS! TERUSKAN PRESTASIMU!",
    "🚀 MANTAP JIWA, {name}! BELAJARMU SUNGGUH HEBAT!",
    "🏆 KHANSA BANGGA PADAMU! PERTAHANKAN PRESTASIMU!",
    "🌈 KEREN BANGET, {name}! OTAKMU SECEPAT KILAT!",
    "💯 SEMPURNA, {name}! TIDAK ADA YANG BISA MENGHENTIKANMU!",
    "⭐ SANG JUARA KEBANGGAAN! MASA DEPANMU PASTI CERAH!",
    "🎉 DAHSYAT! SATU LANGKAH LAGI JADI PROFESOR CILIK!"
]


# Tingkat Kelas Edukasi Matematika SD (Kelas 1 - 6)
MATH_GRADES = {
    1: {
        "level": 1,
        "name": "SD Kelas 1 - 2",
        "badge": "🌱 KELAS 1-2",
        "desc": "Tambah & Kurang Dasar (1 - 20)",
        "color": (50, 220, 120),
    },
    2: {
        "level": 2,
        "name": "SD Kelas 3 - 4",
        "badge": "⭐ KELAS 3-4",
        "desc": "Perkalian 1-10 & Pembagian",
        "color": (255, 200, 50),
    },
    3: {
        "level": 3,
        "name": "SD Kelas 5 - 6",
        "badge": "🏆 KELAS 5-6",
        "desc": "Operasi Campuran & 2 Digit",
        "color": (0, 230, 255),
    }
}

# Tingkat Penguasaan Kosa Kata Bahasa Inggris (Target 3000 Vocab)
VOCAB_LEVELS = {
    1: {
        "level": 1,
        "name": "Level 1 (Beginner)",
        "badge": "🌱 VOCAB TINGKAT 1",
        "desc": "Hewan, Benda, Buah, Angka & Dasar",
        "color": (50, 220, 120),
    },
    2: {
        "level": 2,
        "name": "Level 2 (Intermediate)",
        "badge": "⭐ VOCAB TINGKAT 2",
        "desc": "Kata Kerja, Sifat, Profesi & Sekolah",
        "color": (255, 200, 50),
    },
    3: {
        "level": 3,
        "name": "Level 3 (Advanced)",
        "badge": "🏆 VOCAB TINGKAT 3",
        "desc": "Sains, Teknologi, Alam & Abstrak",
        "color": (0, 230, 255),
    }
}

# Kata-Kata Motivasi Bilingual dari Tokoh-Tokoh Hebat Dunia (Indonesia & Inggris)
GREAT_MINDS_QUOTES = [
    {
        "author": "B.J. Habibie",
        "id": "Keberhasilan bukan milik orang pintar, tapi milik orang yang terus berusaha!",
        "en": "Success belongs not to the smartest, but to those who never stop trying!"
    },
    {
        "author": "Ki Hajar Dewantara",
        "id": "Setiap orang menjadi guru, setiap rumah menjadi sekolah.",
        "en": "Everyone is a teacher, every home is a school."
    },
    {
        "author": "Albert Einstein",
        "id": "Belajar dari kemarin, hidup untuk hari ini, berharap untuk hari esok.",
        "en": "Learn from yesterday, live for today, hope for tomorrow."
    },
    {
        "author": "Nelson Mandela",
        "id": "Pendidikan adalah senjata paling ampuh untuk mengubah dunia.",
        "en": "Education is the most powerful weapon which you can use to change the world."
    },
    {
        "author": "Walt Disney",
        "id": "Semua impian kita bisa terwujud jika kita berani mengejarnya.",
        "en": "All our dreams can come true if we have the courage to pursue them."
    },
    {
        "author": "Thomas A. Edison",
        "id": "Kegeniusan adalah 1% inspirasi dan 99% kerja keras!",
        "en": "Genius is 1% inspiration and 99% perspiration!"
    },
    {
        "author": "Steve Jobs",
        "id": "Tetaplah lapar akan ilmu, dan teruslah belajar dengan rendah hati.",
        "en": "Stay hungry for knowledge, stay foolish and keep learning."
    },
    {
        "author": "Mahatma Gandhi",
        "id": "Hiduplah seolah mati besok, belajarlah seolah hidup selamanya.",
        "en": "Live as if you were to die tomorrow. Learn as if you were to live forever."
    },
    {
        "author": "Helen Keller",
        "id": "Optimisme dan keyakinan adalah jalan pembuka setiap keberhasilan besar.",
        "en": "Optimism and faith are the pathways to great achievement."
    },
    {
        "author": "Confucius",
        "id": "Tidak peduli seberapa lambat melaju, asalkan tidak pernah berhenti!",
        "en": "It does not matter how slowly you go as long as you do not stop!"
    },
    {
        "author": "Eleanor Roosevelt",
        "id": "Masa depan adalah milik mereka yang percaya pada keindahan impiannya.",
        "en": "The future belongs to those who believe in the beauty of their dreams."
    },
    {
        "author": "Ir. Soekarno",
        "id": "Bermimpilah setinggi langit! Jika jatuh, kau jatuh di antara bintang-bintang!",
        "en": "Dream as high as the sky! If you fall, you fall among the stars!"
    },
    {
        "author": "Malcolm X",
        "id": "Pendidikan adalah tiket masa depan untuk mereka yang menyiapkannya hari ini.",
        "en": "Education is the passport to the future for those who prepare today."
    },
    {
        "author": "Marie Curie",
        "id": "Tak ada hal yang perlu ditakutkan, semuanya hanya perlu dipahami.",
        "en": "Nothing in life is to be feared, it is only to be understood."
    },
    {
        "author": "Aristotle",
        "id": "Akar pendidikan mungkin terasa pahit, namun buahnya sungguh manis.",
        "en": "The roots of education are bitter, but the fruit is sweet."
    },
    {
        "author": "C.S. Lewis",
        "id": "Kamu tidak pernah terlalu tua untuk meraih impian baru yang lebih tinggi.",
        "en": "You are never too old to set another goal or dream a new dream."
    }
]


