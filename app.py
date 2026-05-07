from flask import Flask, render_template, request
import random

app = Flask(__name__)

sehirler = ["Adana", "Adıyaman", "Afyonkarahisar", "Ağrı", "Amasya", "Ankara", "Antalya", "Artvin", "Aydın", "Balıkesir", "Bilecik", "Bingöl", "Bitlis", "Bolu", "Burdur", "Bursa", "Çanakkale", "Çankırı", "Çorum", "Denizli", "Diyarbakır", "Edirne", "Elazığ", "Erzincan", "Erzurum", "Eskişehir", "Gaziantep", "Giresun", "Gümüşhane", "Hakkari", "Hatay", "Isparta", "Mersin", "İstanbul", "İzmir", "Kars", "Kastamonu", "Kayseri", "Kırklareli", "Kırşehir", "Kocaeli", "Konya", "Kütahya", "Malatya", "Manisa", "Kahramanmaraş", "Mardin", "Muğla", "Muş", "Nevşehir", "Niğde", "Ordu", "Rize", "Sakarya", "Samsun", "Siirt", "Sinop", "Sivas", "Tekirdağ", "Tokat", "Trabzon", "Tunceli", "Şanlıurfa", "Uşak", "Van", "Yozgat", "Zonguldak", "Aksaray", "Bayburt", "Karaman", "Kırıkkale", "Batman", "Şırnak", "Bartın", "Ardahan", "Iğdır", "Yalova", "Karabük", "Kilis", "Osmaniye", "Düzce"]

meslekler = ["Yazılım Mimarı", "Yapay Zeka Uzmanı", "Siber Güvenlik Uzmanı", "Veri Analisti", "DevOps Uzmanı", "Oyun Geliştirici", "Full Stack Developer", "Mobil Uygulama Geliştirici", "Bulut Sistem Mühendisi", "Veri Bilimci"]

# Haber havuzunu genişlettim ki her seferinde farklı gelsin
haber_havuzu = [
    {"tag": "1 Sektör News!", "baslik": "AI Maaşları Artıyor", "ozet": "2025'te yapay zeka bilen yazılımcıların maaşı %40 daha yüksek."},
    {"tag": "1 Sektör News!", "baslik": "Yazılım Sektörü 2024", "ozet": "Hibrit çalışma modeli artık kalıcı hale geliyor."},
    {"tag": "3 Sektör News!", "baslik": "Kripto Mühendisleri", "ozet": "Blockchain tabanlı projelerde uzman açığı büyüyor."},
    {"tag": "Trend", "baslik": "Siber Güvenlik", "ozet": "Güvenlik uzmanları en çok aranan ilk 3 meslekte."},
    {"tag": "Ekonomi", "baslik": "Global Remote", "ozet": "Yurt dışı kaynaklı işlerde dolar bazlı artış sürüyor."},
    {"tag": "Girişim", "baslik": "Yeni Unicornlar", "ozet": "Türkiye oyun ve fintech alanında yatırım rekoru kırdı."}
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

        # Yaş-Deneyim Kontrolü
        if deneyim > (yas - 18):
            return render_template('index.html', sehirler=sehirler, meslekler=meslekler, hata="Yaş ve deneyim tutarsız!")

        # Net Hesaplama (0 hatasını önlemek için)
        baz = 28000
        egitim_bonus = {"Lise": 0.8, "Lisans": 1.0, "Yüksek Lisans": 1.3, "Doktora": 1.6}
        hesap = (baz * egitim_bonus.get(egitim, 1.0)) + (deneyim * 9200)
        
        if "Mimarı" in meslek or "Zeka" in meslek: hesap += 15000
        if secilen_sehir == "İstanbul": hesap *= 1.3

        oran = round(hesap / 17002, 1)
        secilen_haberler = random.sample(haber_havuzu, 3) # Haberleri rastgele seç

        return render_template('index.html', tahmin=int(hesap), sehirler=sehirler, meslekler=meslekler, 
                             oran=oran, secilen_sehir=secilen_sehir, yas=yas, deneyim=deneyim,
                             haberler=secilen_haberler)
    except:
        return render_template('index.html', sehirler=sehirler, meslekler=meslekler)
