import random
from flask import Flask, render_template, request

app = Flask(__name__)

# Sabit Veriler
iller = ["Adana", "Adıyaman", "Afyonkarahisar", "Ağrı", "Amasya", "Ankara", "Antalya", "Artvin", "Aydın", "Balıkesir", "Bilecik", "Bingöl", "Bitlis", "Bolu", "Burdur", "Bursa", "Çanakkale", "Çankırı", "Çorum", "Denizli", "Diyarbakır", "Edirne", "Elazığ", "Erzincan", "Erzurum", "Eskişehir", "Gaziantep", "Giresun", "Gümüşhane", "Hakkari", "Hatay", "Isparta", "Mersin", "İstanbul", "İzmir", "Kars", "Kastamonu", "Kayseri", "Kırklareli", "Kırşehir", "Kocaeli", "Konya", "Kütahya", "Malatya", "Manisa", "Kahramanmaraş", "Mardin", "Muğla", "Muş", "Nevşehir", "Niğde", "Ordu", "Rize", "Sakarya", "Samsun", "Siirt", "Sinop", "Sivas", "Tekirdağ", "Tokat", "Trabzon", "Tunceli", "Şanlıurfa", "Uşak", "Van", "Yozgat", "Zonguldak", "Aksaray", "Bayburt", "Karaman", "Kırıkkale", "Batman", "Şırnak", "Bartın", "Ardahan", "Iğdır", "Yalova", "Karabük", "Kilis", "Osmaniye", "Düzce"]

meslekler = ["Yazılım Mühendisi", "Veri Analisti", "Proje Yöneticisi", "Pazarlama Uzmanı", "İnsan Kaynakları Uzmanı", "Finans Danışmanı", "Satış Temsilcisi", "Grafik Tasarımcı", "Sistem Yönetici", "Müşteri İlişkileri Yöneticisi"]

haber_havuzu = [
    {"baslik": "AI Maaşları %40 Arttı", "kategori": "SEKTÖR"},
    {"baslik": "2024 Beklentileri Pozitif", "kategori": "EKONOMİ"},
    {"baslik": "Remote Çalışma Artıyor", "kategori": "KARİYER"},
    {"baslik": "Yeni Mezunlara Dev Destek", "kategori": "EĞİTİM"},
    {"baslik": "Teknoloji Yatırımları Hızlandı", "kategori": "HABER"}
]

@app.route('/', methods=['GET', 'POST'])
def index():
    tahmin = None
    hata = None
    asgari_kati = 0
    # Her tahminde veya sayfa yenilemede 3 farklı haber seçer
    guncel_haberler = random.sample(haber_havuzu, 3)
    
    if request.method == 'POST':
        yas = int(request.form.get('yas', 18))
        deneyim = int(request.form.get('deneyim', 0))
        egitim = request.form.get('egitim')
        sehir = request.form.get('sehir')
        
        # MANTIKSAL KONTROL: 20 yaşındaki biri 5 yıl deneyim giremez (18 yaş sınırı)
        if deneyim > (yas - 18):
            hata = f"{yas} yaşında birinin maksimum {max(0, yas-18)} yıl iş deneyimi olabilir."
        else:
            # Gerçekçi Maaş Tahmin Mantığı
            base = 25000 
            egitim_farki = {"Lise": 0, "Lisans": 5000, "Yüksek Lisans": 12000, "Doktora": 18000}
            tahmin = base + (deneyim * 5500) + egitim_farki.get(egitim, 0)
            
            # Büyükşehir bonusu
            if sehir in ["İstanbul", "Ankara", "İzmir"]: tahmin += 8000
            
            # Asgari Ücret Kıyaslaması
            asgari_kati = round(tahmin / 17002, 1)

    return render_template('index.html', iller=iller, meslekler=meslekler, tahmin=tahmin, hata=hata, asgari_kati=asgari_kati, haberler=guncel_haberler)
