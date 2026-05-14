from flask import Flask, render_template, request
import random
import sqlite3
from datetime import datetime, timedelta
app = Flask(__name__)

# DATABASE OLUŞTUR

def init_db():

    conn = sqlite3.connect("database.db")

    cursor = conn.cursor()

    cursor.execute("""

    CREATE TABLE IF NOT EXISTS tahminler (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        yas INTEGER,

        deneyim INTEGER,

        egitim TEXT,

        meslek TEXT,

        sehir TEXT,

        maas INTEGER,

        tarih TEXT

    )

    """)

    conn.commit()

    conn.close()


init_db()

# ASGARİ ÜCRET
ASGARI_UCRET = 17002

# 81 İL
sehirler = [
    "Adana", "Adıyaman", "Afyonkarahisar", "Ağrı", "Amasya",
    "Ankara", "Antalya", "Artvin", "Aydın", "Balıkesir",
    "Bilecik", "Bingöl", "Bitlis", "Bolu", "Burdur",
    "Bursa", "Çanakkale", "Çankırı", "Çorum", "Denizli",
    "Diyarbakır", "Edirne", "Elazığ", "Erzincan", "Erzurum",
    "Eskişehir", "Gaziantep", "Giresun", "Gümüşhane", "Hakkari",
    "Hatay", "Isparta", "Mersin", "İstanbul", "İzmir",
    "Kars", "Kastamonu", "Kayseri", "Kırklareli", "Kırşehir",
    "Kocaeli", "Konya", "Kütahya", "Malatya", "Manisa",
    "Kahramanmaraş", "Mardin", "Muğla", "Muş", "Nevşehir",
    "Niğde", "Ordu", "Rize", "Sakarya", "Samsun",
    "Siirt", "Sinop", "Sivas", "Tekirdağ", "Tokat",
    "Trabzon", "Tunceli", "Şanlıurfa", "Uşak", "Van",
    "Yozgat", "Zonguldak", "Aksaray", "Bayburt", "Karaman",
    "Kırıkkale", "Batman", "Şırnak", "Bartın", "Ardahan",
    "Iğdır", "Yalova", "Karabük", "Kilis", "Osmaniye", "Düzce"
]

# MESLEKLER
meslekler = [
    "Yazılım Mimarı",
    "Yapay Zeka Uzmanı",
    "Siber Güvenlik Uzmanı",
    "Veri Analisti",
    "DevOps Uzmanı",
    "Oyun Geliştirici",
    "Full Stack Developer",
    "Mobil Uygulama Geliştirici",
    "Bulut Sistem Mühendisi",
    "Veri Bilimci"
]

# MESLEK KATSAYILARI
meslek_katsayi = {
    "Yazılım Mimarı": 1.65,
    "Yapay Zeka Uzmanı": 1.80,
    "Siber Güvenlik Uzmanı": 1.55,
    "Veri Analisti": 1.20,
    "DevOps Uzmanı": 1.50,
    "Oyun Geliştirici": 1.35,
    "Full Stack Developer": 1.40,
    "Mobil Uygulama Geliştirici": 1.38,
    "Bulut Sistem Mühendisi": 1.58,
    "Veri Bilimci": 1.70
}

# EĞİTİM KATSAYILARI
egitim_katsayi = {
    "Lise": 0.9,
    "Ön Lisans": 1.05,
    "Lisans": 1.2,
    "Yüksek Lisans": 1.45,
    "Doktora": 1.7
}

# ŞEHİR KATSAYISI
sehir_katsayi = {
    "İstanbul": 1.35,
    "Ankara": 1.22,
    "İzmir": 1.24,
    "Kocaeli": 1.20,
    "Bursa": 1.18,
    "Antalya": 1.16,
    "Muğla": 1.14,
    "Tekirdağ": 1.13,
    "Eskişehir": 1.12,
    "Sakarya": 1.11
}

# SON TAHMİNLERİ ÇEK
conn = sqlite3.connect("database.db")
cursor = conn.cursor()

cursor.execute("""
SELECT meslek, sehir, maas, tarih
FROM tahminler
ORDER BY id DESC
LIMIT 5
""")

son_tahminler = cursor.fetchall()
conn.close()

# GERÇEK HABERLER

try:

    url = (
        "https://newsapi.org/v2/everything?"
        "q=yazilim OR yapay zeka OR teknoloji"
        "&language=tr"
        "&sortBy=publishedAt"
        "&pageSize=3"
        "&apiKey=b8d4b10143624a96aa085bc8fb0540a4"
    )

    response = requests.get(url)

    data = response.json()

    haberler = []

    for article in data["articles"]:

        haberler.append({

            "tag": "GÜNCEL",

            "baslik": article["title"],

            "ozet": (
                article["description"]
                if article["description"]
                else "Detay bulunamadı."
            )

        })

except:

    haberler = [
        {
            "tag": "SİSTEM",
            "baslik": "Haber sistemi yüklenemedi",
            "ozet": "API bağlantısı kurulamadı."
        }
    ]


@app.route('/')
def index():

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT meslek, sehir, maas, tarih
    FROM tahminler
    ORDER BY id DESC
    LIMIT 5
    """)

    son_tahminler = cursor.fetchall()
    conn.close()

    return render_template(
        'index.html',
        sehirler=sehirler,
        meslekler=meslekler,
        son_tahminler=son_tahminler
    )


@app.route('/predict', methods=['POST'])
def predict():

    try:

        yas = int(request.form.get('yas'))
        deneyim = int(request.form.get('deneyim'))
        egitim = request.form.get('egitim')
        meslek = request.form.get('meslek')
        secilen_sehir = request.form.get('sehir')

        if yas < 18 or yas > 65:
            return render_template(
                'index.html',
                hata="Lütfen 18-65 arasında yaş girin.",
                sehirler=sehirler,
                meslekler=meslekler
            )

        max_deneyim = yas - 18

        if deneyim > max_deneyim:
            return render_template(
                'index.html',
                hata=f"{yas} yaşındaki biri için maksimum {max_deneyim} yıl deneyim girilebilir.",
                sehirler=sehirler,
                meslekler=meslekler
            )

        temel_maas = 22000

        meslek_orani = meslek_katsayi.get(meslek, 1.0)
        egitim_orani = egitim_katsayi.get(egitim, 1.0)
        sehir_orani = sehir_katsayi.get(secilen_sehir, 1.0)

        deneyim_bonus = deneyim * 4500

        maas = (
            temel_maas *
            meslek_orani *
            egitim_orani *
            sehir_orani
        ) + deneyim_bonus

        maas *= random.uniform(0.96, 1.08)
        maas = int(maas)

        oran = round(maas / ASGARI_UCRET, 1)

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO tahminler (
            yas,
            deneyim,
            egitim,
            meslek,
            sehir,
            maas,
            tarih
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            yas,
            deneyim,
            egitim,
            meslek,
            secilen_sehir,
            maas,
            (datetime.utcnow() + timedelta(hours=3)).strftime("%d-%m-%Y %H:%M")
        ))

        conn.commit()
        conn.close()

        grafik_verileri = {}

        for sehir in sehirler:

            sehir_carpan = sehir_katsayi.get(sehir, 1.0)

            sehir_maas = (
                temel_maas *
                meslek_orani *
                egitim_orani *
                sehir_carpan
            ) + deneyim_bonus

            sehir_maas *= random.uniform(0.95, 1.05)

            grafik_verileri[sehir] = int(sehir_maas)

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        cursor.execute("""
        SELECT meslek, sehir, maas, tarih
        FROM tahminler
        ORDER BY id DESC
        LIMIT 5
        """)

        son_tahminler = cursor.fetchall()
        conn.close()

        haberler = random.sample(haber_havuzu, 3)

        return render_template(
            'index.html',
            tahmin=maas,
            oran=oran,
            sehirler=sehirler,
            meslekler=meslekler,
            grafik_verileri=grafik_verileri,
            haberler=haberler,
            son_tahminler=son_tahminler,
            secilen_sehir=secilen_sehir,
            yas=yas,
            deneyim=deneyim,
            egitim=egitim,
            meslek=meslek
        )

    except Exception as e:
        print(e)
        return render_template(
            'index.html',
            hata="Bir hata oluştu.",
            sehirler=sehirler,
            meslekler=meslekler
        )


if __name__ == '__main__':
    app.run(debug=True)
