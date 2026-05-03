from flask import Flask, render_template, request

app = Flask(__name__)

sehirler = ["Adana", "Adıyaman", "Afyonkarahisar", "Ağrı", "Amasya", "Ankara", "Antalya", "Artvin", "Aydın", "Balıkesir", "Bilecik", "Bingöl", "Bitlis", "Bolu", "Burdur", "Bursa", "Çanakkale", "Çankırı", "Çorum", "Denizli", "Diyarbakır", "Edirne", "Elazığ", "Erzincan", "Erzurum", "Eskişehir", "Gaziantep", "Giresun", "Gümüşhane", "Hakkari", "Hatay", "Isparta", "Mersin", "İstanbul", "İzmir", "Kars", "Kastamonu", "Kayseri", "Kırklareli", "Kırşehir", "Kocaeli", "Konya", "Kütahya", "Malatya", "Manisa", "Kahramanmaraş", "Mardin", "Muğla", "Muş", "Nevşehir", "Niğde", "Ordu", "Rize", "Sakarya", "Samsun", "Siirt", "Sinop", "Sivas", "Tekirdağ", "Tokat", "Trabzon", "Tunceli", "Şanlıurfa", "Uşak", "Van", "Yozgat", "Zonguldak", "Aksaray", "Bayburt", "Karaman", "Kırıkkale", "Batman", "Şırnak", "Bartın", "Ardahan", "Iğdır", "Yalova", "Karabük", "Kilis", "Osmaniye", "Düzce"]

@app.route('/')
def index():
    return render_template('index.html', sehirler=sehirler, tahmin=None)

@app.route('/predict', methods=['POST'])
def predict():
    yas = int(request.form.get('yas', 25))
    deneyim = int(request.form.get('deneyim', 3))
    egitim = request.form.get('egitim')
    meslek = request.form.get('meslek')
    secilen_sehir = request.form.get('sehir')

    # Maaş Algoritması
    base_maas = 22000 
    if egitim == "Lise": base_maas = 18000
    
    maas = base_maas + (deneyim * 5500) + (yas * 250)
    
    # Eğitim bonusları
    if egitim == "Yüksek Lisans": maas += 12000
    elif egitim == "Doktora": maas += 20000
    
    # Kapsamlı Meslek Bonusları
    meslek_bonus = {
        "Yazılım Mimarı": 30000,
        "Veri Bilimci": 18000,
        "Siber Güvenlik Uzmanı": 20000,
        "Mobil Geliştirici": 15000,
        "Backend Geliştirici": 14000,
        "Frontend Geliştirici": 12000,
        "DevOps Mühendisi": 22000
    }
    maas += meslek_bonus.get(meslek, 10000)

    if secilen_sehir in ["İstanbul", "Ankara", "İzmir"]: maas *= 1.2
    
    tahmin_sonuc = "{:,.0f}".format(maas).replace(",", ".")

    return render_template('index.html', tahmin=tahmin_sonuc, sehirler=sehirler, 
                           secilen_sehir=secilen_sehir, yas=yas, deneyim=deneyim)
