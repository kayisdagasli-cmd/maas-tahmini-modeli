from flask import Flask, render_template, request
import random

app = Flask(__name__)

# Veri Listeleri
sehirler = ["Adana", "Adıyaman", "Afyonkarahisar", "Ağrı", "Amasya", "Ankara", "Antalya", "Artvin", "Aydın", "Balıkesir", "Bilecik", "Bingöl", "Bitlis", "Bolu", "Burdur", "Bursa", "Çanakkale", "Çankırı", "Çorum", "Denizli", "Diyarbakır", "Edirne", "Elazığ", "Erzincan", "Erzurum", "Eskişehir", "Gaziantep", "Giresun", "Gümüşhane", "Hakkari", "Hatay", "Isparta", "Mersin", "İstanbul", "İzmir", "Kars", "Kastamonu", "Kayseri", "Kırklareli", "Kırşehir", "Kocaeli", "Konya", "Kütahya", "Malatya", "Manisa", "Kahramanmaraş", "Mardin", "Muğla", "Muş", "Nevşehir", "Niğde", "Ordu", "Rize", "Sakarya", "Samsun", "Siirt", "Sinop", "Sivas", "Tekirdağ", "Tokat", "Trabzon", "Tunceli", "Şanlıurfa", "Uşak", "Van", "Yozgat", "Zonguldak", "Aksaray", "Bayburt", "Karaman", "Kırıkkale", "Batman", "Şırnak", "Bartın", "Ardahan", "Iğdır", "Yalova", "Karabük", "Kilis", "Osmaniye", "Düzce"]

meslekler = ["Yazılım Mimarı", "Yapay Zeka Uzmanı", "Siber Güvenlik Uzmanı", "Veri Analisti", "DevOps Uzmanı", "Oyun Geliştirici", "Full Stack Developer", "Mobil Uygulama Geliştirici", "Bulut Sistem Mühendisi", "Veri Bilimci"]

haber_havuzu = [
    {"tag": "1 Sektör News!", "baslik": "AI Maaşları Artıyor", "ozet": "2025'te yapay zeka bilen yazılımcıların maaşı %40 daha yüksek."},
    {"tag": "1 Sektör News!", "baslik": "Yazılım Sektöründe 2024 Beklentileri", "ozet": "Hibrit çalışma modeli artık kalıcı hale geliyor."},
    {"tag": "3 Sektör News!", "baslik": "Kripto Mühendislerine Talep Artıyor", "ozet": "Blockchain tabanlı projelerde uzman açığı büyüyor."},
    {"tag": "Trend", "baslik": "Siber Güvenlik Ön Planda", "ozet": "Güvenlik uzmanları en çok aranan ilk 3 meslek arasına girdi."}
]

@app.route('/')
def index():
    return render_template('index.html', sehirler=sehirler, meslekler=meslekler)

@app.route('/predict', methods=['POST'])
def predict():
    try:
        yas = int(request.form.get('yas', 25))
        deneyim = int(request.form.get('deneyim', 3))
        egitim = request.form.get('egitim')
        meslek = request.form.get('meslek')
        secilen_sehir = request.form.get('sehir')

        # Yaş - Deneyim Bağlantısı (Kritik Kontrol)
        if deneyim > (yas - 18):
            return render_template('index.html', sehirler=sehirler, meslekler=meslekler, hata=f"Hata: {yas} yaşındaki birisi {deneyim} yıl deneyime sahip olamaz!")

        # Sabit Matematiksel Maaş Formülü (Rastgele Değil)
        baz_puan = 25000
        
        egitim_carpanlari = {"Lise": 0.8, "Lisans": 1.0, "Yüksek Lisans": 1.3, "Doktora": 1.6}
        baz_puan *= egitim_carpanlari.get(egitim, 1.0)
        
        deneyim_ekli = deneyim * 8500
        meslek_bonusu = 15000 if any(x in meslek for x in ["Mimarı", "Zeka", "Siber"]) else 5000
        
        toplam = baz_puan + deneyim_ekli + meslek_bonusu
        
        if secilen_sehir == "İstanbul": toplam *= 1.3
        elif secilen_sehir in ["Ankara", "İzmir"]: toplam *= 1.15

        oran = round(toplam / 17002, 1)
        
        # Ek Analiz Verileri
        skor = 78 if secilen_sehir == "Antalya" else random.randint(60, 85)
        ist_kiyas = int(toplam * 1.2) if secilen_sehir != "İstanbul" else int(toplam)
        secilen_haberler = random.sample(haber_havuzu, 3)

        return render_template('index.html', tahmin=int(toplam), sehirler=sehirler, meslekler=meslekler, 
                             oran=oran, secilen_sehir=secilen_sehir, yas=yas, deneyim=deneyim,
                             skor=skor, ist_kiyas=ist_kiyas, haberler=secilen_haberler)
    except:
        return render_template('index.html', sehirler=sehirler, meslekler=meslekler)
