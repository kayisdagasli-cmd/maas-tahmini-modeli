from flask import Flask, render_template, request
import random

app = Flask(__name__)

sehirler = ["Adana", "Adıyaman", "Afyonkarahisar", "Ağrı", "Amasya", "Ankara", "Antalya", "Artvin", "Aydın", "Balıkesir", "Bilecik", "Bingöl", "Bitlis", "Bolu", "Burdur", "Bursa", "Çanakkale", "Çankırı", "Çorum", "Denizli", "Diyarbakır", "Edirne", "Elazığ", "Erzincan", "Erzurum", "Eskişehir", "Gaziantep", "Giresun", "Gümüşhane", "Hakkari", "Hatay", "Isparta", "Mersin", "İstanbul", "İzmir", "Kars", "Kastamonu", "Kayseri", "Kırklareli", "Kırşehir", "Kocaeli", "Konya", "Kütahya", "Malatya", "Manisa", "Kahramanmaraş", "Mardin", "Muğla", "Muş", "Nevşehir", "Niğde", "Ordu", "Rize", "Sakarya", "Samsun", "Siirt", "Sinop", "Sivas", "Tekirdağ", "Tokat", "Trabzon", "Tunceli", "Şanlıurfa", "Uşak", "Van", "Yozgat", "Zonguldak", "Aksaray", "Bayburt", "Karaman", "Kırıkkale", "Batman", "Şırnak", "Bartın", "Ardahan", "Iğdır", "Yalova", "Karabük", "Kilis", "Osmaniye", "Düzce"]

meslekler = ["Yazılım Mimarı", "Yapay Zeka Uzmanı", "Siber Güvenlik Uzmanı", "Veri Analisti", "DevOps Uzmanı", "Oyun Geliştirici", "Full Stack Developer", "Mobil Uygulama Geliştirici", "Bulut Sistem Mühendisi", "Veri Bilimci"]

# Değişen Haberler Listesi
haber_havuzu = [
    {"tag": "AI Trend", "baslik": "AI Maaşları Artıyor", "ozet": "Yapay zeka uzmanlarına talep %40 arttı."},
    {"tag": "Sektör", "baslik": "Hibrit Devrimi", "ozet": "Şirketlerin %65'i kalıcı hibrit modele geçti."},
    {"tag": "Teknoloji", "baslik": "Yeni Diller", "ozet": "Rust ve Go dilleri bu yıl rekor kırdı."},
    {"tag": "Ekonomi", "baslik": "Yazılımcı Göçü", "ozet": "Uzaktan çalışma global maaşları eşitledi."},
    {"tag": "Siber", "baslik": "Güvenlik Açığı", "ozet": "Sektörde 200 bin yeni uzman aranıyor."},
    {"tag": "Girişim", "baslik": "Yerli Unicornlar", "ozet": "Türkiye oyun sektöründe Avrupa lideri."}
]

@app.route('/')
def index():
    secilen_haberler = random.sample(haber_havuzu, 3)
    return render_template('index.html', sehirler=sehirler, meslekler=meslekler, haberler=secilen_haberler)

@app.route('/predict', methods=['POST'])
def predict():
    try:
        yas = int(request.form.get('yas', 25))
        deneyim = int(request.form.get('deneyim', 3))
        egitim = request.form.get('egitim')
        meslek = request.form.get('meslek')
        secilen_sehir = request.form.get('sehir')

        # KRİTİK: Yaş ve Deneyim Doğrulaması
        if yas < 18 or yas > 65:
            return render_template('index.html', sehirler=sehirler, meslekler=meslekler, hata="Yaş 18-65 arasında olmalıdır.", haberler=random.sample(haber_havuzu, 3))
        
        if deneyim > (yas - 18):
            return render_template('index.html', sehirler=sehirler, meslekler=meslekler, hata=f"{yas} yaşında biri {deneyim} yıl deneyime sahip olamaz!", haberler=random.sample(haber_havuzu, 3))

        # Maaş Hesaplama
        baz = 30000
        if egitim == "Lise": baz = 19000
        elif egitim == "Yüksek Lisans": baz = 40000
        elif egitim == "Doktora": baz = 55000
        
        maas = baz + (deneyim * 9500)
        if "Mimarı" in meslek or "Zeka" in meslek: maas += 20000
        if secilen_sehir == "İstanbul": maas *= 1.35

        oran = round(maas / 17002, 1)
        secilen_haberler = random.sample(haber_havuzu, 3)
        
        return render_template('index.html', tahmin=int(maas), sehirler=sehirler, meslekler=meslekler, oran=oran, 
                             secilen_sehir=secilen_sehir, yas=yas, deneyim=deneyim, haberler=secilen_haberler)
    except:
        return render_template('index.html', sehirler=sehirler, meslekler=meslekler, hata="Giriş hatası oluştu.", haberler=random.sample(haber_havuzu, 3))
