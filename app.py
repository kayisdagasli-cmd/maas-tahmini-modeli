from flask import Flask, render_template, request

app = Flask(__name__)

# Örnek veri setimiz ve 81 il listesi
sehirler = ["Adana", "Adıyaman", "Afyonkarahisar", "Ağrı", "Amasya", "Ankara", "Antalya", "Artvin", "Aydın", "Balıkesir", "Bilecik", "Bingöl", "Bitlis", "Bolu", "Burdur", "Bursa", "Çanakkale", "Çankırı", "Çorum", "Denizli", "Diyarbakır", "Edirne", "Elazığ", "Erzincan", "Erzurum", "Eskişehir", "Gaziantep", "Giresun", "Gümüşhane", "Hakkari", "Hatay", "Isparta", "Mersin", "İstanbul", "İzmir", "Kars", "Kastamonu", "Kayseri", "Kırklareli", "Kırşehir", "Kocaeli", "Konya", "Kütahya", "Malatya", "Manisa", "Kahramanmaraş", "Mardin", "Muğla", "Muş", "Nevşehir", "Niğde", "Ordu", "Rize", "Sakarya", "Samsun", "Siirt", "Sinop", "Sivas", "Tekirdağ", "Tokat", "Trabzon", "Tunceli", "Şanlıurfa", "Uşak", "Van", "Yozgat", "Zonguldak", "Aksaray", "Bayburt", "Karaman", "Kırıkkale", "Batman", "Şırnak", "Bartın", "Ardahan", "Iğdır", "Yalova", "Karabük", "Kilis", "Osmaniye", "Düzce"]

@app.route('/')
def index():
    return render_template('index.html', sehirler=sehirler, tahmin=None)

@app.route('/predict', methods=['POST'])
def predict():
    # Formdan gelen verileri alıyoruz
    yas = int(request.form.get('yas', 18))
    deneyim = int(request.form.get('deneyim', 0))
    egitim = request.form.get('egitim')
    meslek = request.form.get('meslek')
    secilen_sehir = request.form.get('sehir')

    # Basit bir maaş hesaplama algoritması (Burası modelin beyni)
    base_maas = 25000
    maas = base_maas + (deneyim * 3500) + (yas * 200)
    
    if egitim == "Yüksek Lisans": maas += 8000
    elif egitim == "Doktora": maas += 15000
    
    if meslek == "Yazılım Mimarı": maas += 20000
    elif meslek == "Veri Bilimci": maas += 12000

    # Şehir çarpanı (Örn: İstanbul %20 daha fazla)
    if secilen_sehir == "İstanbul": maas *= 1.2
    
    tahmin_sonuc = "{:,.0f}".format(maas).replace(",", ".")

    return render_template('index.html', 
                           tahmin=tahmin_sonuc, 
                           sehirler=sehirler, 
                           secilen_sehir=secilen_sehir)

if __name__ == '__main__':
    app.run(debug=True)
