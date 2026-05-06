import random
from flask import Flask, render_template, request

app = Flask(__name__)

# Veri Setleri
iller = ["Adana", "Adıyaman", "Afyonkarahisar", "Ağrı", "Amasya", "Ankara", "Antalya", "Artvin", "Aydın", "Balıkesir", "Bilecik", "Bingöl", "Bitlis", "Bolu", "Burdur", "Bursa", "Çanakkale", "Çankırı", "Çorum", "Denizli", "Diyarbakır", "Edirne", "Elazığ", "Erzincan", "Erzurum", "Eskişehir", "Gaziantep", "Giresun", "Gümüşhane", "Hakkari", "Hatay", "Isparta", "Mersin", "İstanbul", "İzmir", "Kars", "Kastamonu", "Kayseri", "Kırklareli", "Kırşehir", "Kocaeli", "Konya", "Kütahya", "Malatya", "Manisa", "Kahramanmaraş", "Mardin", "Muğla", "Muş", "Nevşehir", "Niğde", "Ordu", "Rize", "Sakarya", "Samsun", "Siirt", "Sinop", "Sivas", "Tekirdağ", "Tokat", "Trabzon", "Tunceli", "Şanlıurfa", "Uşak", "Van", "Yozgat", "Zonguldak", "Aksaray", "Bayburt", "Karaman", "Kırıkkale", "Batman", "Şırnak", "Bartın", "Ardahan", "Iğdır", "Yalova", "Karabük", "Kilis", "Osmaniye", "Düzce"]

meslekler = ["Yazılım Geliştirici", "Veri Bilimci", "Mimar", "Doktor", "Avukat", "E-Ticaret Uzmanı", "Grafik Tasarımcı", "Öğretmen", "Mühendis", "Finans Uzmanı"]

haber_havuzu = [
    {"baslik": "AI Maaşları %40 Arttı", "kategori": "Sektör Haber"},
    {"baslik": "Yazılımda 2024 Beklentileri", "kategori": "Ekonomi"},
    {"baslik": "Remote Çalışma Yaygınlaşıyor", "kategori": "Kariyer"},
    {"baslik": "Yeni Mezunlara Dev Destek", "kategori": "Eğitim"},
    {"baslik": "Teknoloji Sektörü Büyüyor", "kategori": "Haber"},
    {"baslik": "Siber Güvenlikte Uzman Açığı", "kategori": "Analiz"}
]

@app.route('/', methods=['GET', 'POST'])
def index():
    tahmin = None
    asgari_kati = 0
    guncel_haberler = random.sample(haber_havuzu, 3) # Her yenilemede 3 farklı haber
    
    if request.method == 'POST':
        yas = int(request.form.get('yas', 25))
        deneyim = int(request.form.get('deneyim', 3))
        egitim = request.form.get('egitim')
        sehir = request.form.get('sehir')
        
        # Basit Maaş Mantığı (Gerçek modelinize göre burayı güncelleyin)
        base = 20000
        egitim_bonus = {"Lise": 0, "Lisans": 5000, "Yüksek Lisans": 10000, "Doktora": 15000}
        tahmin = base + (deneyim * 6000) + egitim_bonus.get(egitim, 0)
        if sehir == "İstanbul": tahmin += 8000
        
        asgari_kati = round(tahmin / 17002, 1) # Güncel asgari ücret üzerinden

    return render_template('index.html', iller=iller, meslekler=meslekler, tahmin=tahmin, asgari_kati=asgari_kati, haberler=guncel_haberler)
