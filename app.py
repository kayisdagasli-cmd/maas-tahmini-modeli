from flask import Flask, render_template, request
import random

app = Flask(__name__)

sehirler = ["Adana", "Adıyaman", "Afyonkarahisar", "Ağrı", "Amasya", "Ankara", "Antalya", "Artvin", "Aydın", "Balıkesir", "Bilecik", "Bingöl", "Bitlis", "Bolu", "Burdur", "Bursa", "Çanakkale", "Çankırı", "Çorum", "Denizli", "Diyarbakır", "Edirne", "Elazığ", "Erzincan", "Erzurum", "Eskişehir", "Gaziantep", "Giresun", "Gümüşhane", "Hakkari", "Hatay", "Isparta", "Mersin", "İstanbul", "İzmir", "Kars", "Kastamonu", "Kayseri", "Kırklareli", "Kırşehir", "Kocaeli", "Konya", "Kütahya", "Malatya", "Manisa", "Kahramanmaraş", "Mardin", "Muğla", "Muş", "Nevşehir", "Niğde", "Ordu", "Rize", "Sakarya", "Samsun", "Siirt", "Sinop", "Sivas", "Tekirdağ", "Tokat", "Trabzon", "Tunceli", "Şanlıurfa", "Uşak", "Van", "Yozgat", "Zonguldak", "Aksaray", "Bayburt", "Karaman", "Kırıkkale", "Batman", "Şırnak", "Bartın", "Ardahan", "Iğdır", "Yalova", "Karabük", "Kilis", "Osmaniye", "Düzce"]

meslekler = ["Yazılım Mimarı", "Yapay Zeka Uzmanı", "Siber Güvenlik Uzmanı", "Veri Analisti", "DevOps Uzmanı", "Oyun Geliştirici", "Full Stack Developer", "Mobil Uygulama Geliştirici", "Bulut Sistem Mühendisi", "Veri Bilimci"]

haber_havuzu = [
    {"tag": "Sektör News!", "baslik": "AI Maaşları Artıyor", "ozet": "2025'te yapay zeka bilen yazılımcıların maaşı %40 daha yüksek."},
    {"tag": "Sektör News!", "baslik": "Yazılım Sektörü 2024", "ozet": "Hibrit çalışma modeli artık kalıcı hale geliyor."},
    {"tag": "Sektör News!", "baslik": "Kripto Mühendisleri", "ozet": "Blockchain tabanlı projelerde uzman açığı büyüyor."},
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
        # Formdan verileri alırken varsayılan değerler atayarak 0 hatasını önlüyoruz
        yas = int(request.form.get('yas', 18))
        deneyim = int(request.form.get('deneyim', 0))
        egitim = request.form.get('egitim', 'Lisans')
        meslek = request.form.get('meslek', 'Veri Analisti')
        secilen_sehir = request.form.get('sehir', 'İstanbul')

        # 1. Kontrol: Yaş Sınırı (18-65)
        if yas < 18 or yas > 65:
            return render_template('index.html', sehirler=sehirler, meslekler=meslekler, hata="Lütfen 18-65 yaş arası bir değer girin.")

        # 2. Kontrol: Yaş-Deneyim İlişkisi
        # Bir kişi en erken 18 yaşında tam zamanlı çalışmaya başladığını varsayarsak
        if deneyim > (yas - 18):
            return render_template('index.html', sehirler=sehirler, meslekler=meslekler, hata=f"{yas} yaşındaki biri için en fazla {yas-18} yıl deneyim girilebilir.")

        # Maaş Hesaplama Mantığı (0 çıkmaması için baz değerler)
        asgari_ucret = 17002
        baz_maas = 25000  # Sektörel başlangıç bazı
        
        egitim_katsayi = {"Lise": 0.8, "Lisans": 1.0, "Yüksek Lisans": 1.25, "Doktora": 1.5}
        katsayi = egitim_katsayi.get(egitim, 1.0)
        
        # Hesaplama: Baz * Eğitim + (Deneyim * Sabit Artış)
        hesap = (baz_maas * katsayi) + (deneyim * 8500)
        
        # Meslek bazlı eklemeler
        if any(keyword in meslek for keyword in ["Mimarı", "Zeka", "Siber", "DevOps"]):
            hesap += 12000
            
        # Şehir bazlı çarpan
        if secilen_sehir in ["İstanbul", "Ankara", "İzmir"]:
            hesap *= 1.2

        oran = round(hesap / asgari_ucret, 1)
        secilen_haberler = random.sample(haber_havuzu, 3)

        return render_template('index.html', tahmin=int(hesap), sehirler=sehirler, meslekler=meslekler, 
                             oran=oran, secilen_sehir=secilen_sehir, yas=yas, deneyim=deneyim,
                             haberler=secilen_haberler)
    except Exception as e:
        print(f"Hata oluştu: {e}")
        return render_template('index.html', sehirler=sehirler, meslekler=meslekler, hata="Bir hata oluştu, lütfen tekrar deneyin.")

if __name__ == '__main__':
    app.run(debug=True)
