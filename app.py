from flask import Flask, render_template, request

app = Flask(__name__)

# Veri setleri
sehirler = ["Adana", "Adıyaman", "Afyonkarahisar", "Ağrı", "Amasya", "Ankara", "Antalya", "Artvin", "Aydın", "Balıkesir", "Bilecik", "Bingöl", "Bitlis", "Bolu", "Burdur", "Bursa", "Çanakkale", "Çankırı", "Çorum", "Denizli", "Diyarbakır", "Edirne", "Elazığ", "Erzincan", "Erzurum", "Eskişehir", "Gaziantep", "Giresun", "Gümüşhane", "Hakkari", "Hatay", "Isparta", "Mersin", "İstanbul", "İzmir", "Kars", "Kastamonu", "Kayseri", "Kırklareli", "Kırşehir", "Kocaeli", "Konya", "Kütahya", "Malatya", "Manisa", "Kahramanmaraş", "Mardin", "Muğla", "Muş", "Nevşehir", "Niğde", "Ordu", "Rize", "Sakarya", "Samsun", "Siirt", "Sinop", "Sivas", "Tekirdağ", "Tokat", "Trabzon", "Tunceli", "Şanlıurfa", "Uşak", "Van", "Yozgat", "Zonguldak", "Aksaray", "Bayburt", "Karaman", "Kırıkkale", "Batman", "Şırnak", "Bartın", "Ardahan", "Iğdır", "Yalova", "Karabük", "Kilis", "Osmaniye", "Düzce"]

meslekler = ["Yazılım Mimarı", "Yapay Zeka Uzmanı", "Siber Güvenlik Uzmanı", "Veri Analisti", "DevOps Uzmanı", "Oyun Geliştirici", "Full Stack Developer", "Mobil Uygulama Geliştirici", "Bulut Sistem Mühendisi", "Veri Bilimci"]

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

        # Mantıksal doğrulama
        if deneyim > (yas - 18):
            return render_template('index.html', sehirler=sehirler, meslekler=meslekler, hata="Yaş ve deneyim bilgisi tutarsız!")

        # Gelişmiş Maaş Hesaplama Motoru
        baz_maas = 28000
        if egitim == "Lise": baz_maas = 19500
        elif egitim == "Yüksek Lisans": baz_maas = 38000
        elif egitim == "Doktora": baz_maas = 52000
        
        deneyim_bonusu = deneyim * 9200
        meslek_farki = 18000 if "Mimarı" in meslek or "Zeka" in meslek else 5000
        
        toplam = baz_maas + deneyim_bonusu + meslek_farki
        if secilen_sehir == "İstanbul": toplam *= 1.35
        elif secilen_sehir in ["Ankara", "İzmir"]: toplam *= 1.15

        asgari = 17002
        oran = round(toplam / asgari, 1)
        
        # Geçim ve Kıyaslama Verileri
        skor = 78 if secilen_sehir == "Antalya" else 65
        durum = "Yeterli" if skor > 70 else "Kısıtlı"
        istanbul_farki = int(toplam * 1.2) # İstanbul tahmini kıyası için

        return render_template('index.html', 
                             tahmin=int(toplam), 
                             sehirler=sehirler, 
                             meslekler=meslekler, 
                             oran=oran, 
                             secilen_sehir=secilen_sehir, 
                             yas=yas, 
                             deneyim=deneyim,
                             skor=skor,
                             durum=durum,
                             ist_fark=istanbul_farki)
    except Exception as e:
        return render_template('index.html', sehirler=sehirler, meslekler=meslekler, hata="Lütfen tüm alanları doldurun.")
