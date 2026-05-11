from flask import Flask, render_template, request
import random

app = Flask(__name__)

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

# EĞİTİM KATSAYISI
egitim_katsayi = {
    "Lise": 0.85,
    "Lisans": 1.0,
    "Yüksek Lisans": 1.18,
    "Doktora": 1.35
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

# HABERLER
haber_havuzu = [
    {
        "tag": "AI",
        "baslik": "Yapay zeka maaşları yükselişte",
        "ozet": "AI uzmanlarına olan talep 2025 yılında ciddi şekilde artıyor."
    },
    {
        "tag": "Cyber Security",
        "baslik": "Siber güvenlik uzmanı açığı büyüyor",
        "ozet": "Şirketler güvenlik yatırımlarını hızlandırıyor."
    },
    {
        "tag": "Remote",
        "baslik": "Uzaktan çalışma kalıcı hale geldi",
        "ozet": "Global şirketler remote mühendis alımını sürdürüyor."
    },
    {
        "tag": "Cloud",
        "baslik": "Bulut sistemleri yükselişte",
        "ozet": "AWS ve Azure uzmanları daha yüksek maaş alıyor."
    },
    {
        "tag": "Startup",
        "baslik": "Teknoloji girişimleri büyüyor",
        "ozet": "Yazılım sektöründe yatırım hacmi artıyor."
    },
    {
        "tag": "Data",
        "baslik": "Veri bilimi en güçlü alanlardan biri",
        "ozet": "Veri odaklı şirketlerin sayısı hızla yükseliyor."
    }
]


@app.route('/')
def index():
    return render_template(
        'index.html',
        sehirler=sehirler,
        meslekler=meslekler
    )


@app.route('/predict', methods=['POST'])
def predict():

    try:

        yas = int(request.form.get('yas'))
        deneyim = int(request.form.get('deneyim'))
        egitim = request.form.get('egitim')
        meslek = request.form.get('meslek')
        secilen_sehir = request.form.get('sehir')

        # YAŞ KONTROLÜ
        if yas < 18 or yas > 65:

            return render_template(
                'index.html',
                hata="Lütfen 18-65 arasında yaş girin.",
                sehirler=sehirler,
                meslekler=meslekler
            )

        # DENEYİM KONTROLÜ
        max_deneyim = yas - 18

        if deneyim > max_deneyim:

            return render_template(
                'index.html',
                hata=f"{yas} yaşındaki biri için maksimum {max_deneyim} yıl deneyim girilebilir.",
                sehirler=sehirler,
                meslekler=meslekler
            )

        # TEMEL MAAŞ
        temel_maas = 22000

        # KATSAYILAR
        meslek_orani = meslek_katsayi.get(meslek, 1.0)
        egitim_orani = egitim_katsayi.get(egitim, 1.0)
        sehir_orani = sehir_katsayi.get(secilen_sehir, 1.0)

        # DENEYİM ETKİSİ
        deneyim_bonus = deneyim * 4500

        # ANA HESAP
        maas = (
            temel_maas *
            meslek_orani *
            egitim_orani *
            sehir_orani
        ) + deneyim_bonus

        # RANDOM PİYASA ETKİSİ
        maas *= random.uniform(0.96, 1.08)

        # YUVARLAMA
        maas = int(maas)

        # ASGARİ ÜCRET ORANI
        oran = round(maas / ASGARI_UCRET, 1)

        # ŞEHİR GRAFİK VERİSİ
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

        # HABERLER
        haberler = random.sample(haber_havuzu, 3)

        return render_template(
            'index.html',

            tahmin=maas,
            oran=oran,

            sehirler=sehirler,
            meslekler=meslekler,

            grafik_verileri=grafik_verileri,

            haberler=haberler,

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
