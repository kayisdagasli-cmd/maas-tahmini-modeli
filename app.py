from flask import Flask, render_template, request

app = Flask(__name__)

# Türkiye'nin 81 İli
sehirler = ["Adana", "Adıyaman", "Afyonkarahisar", "Ağrı", "Amasya", "Ankara", "Antalya", "Artvin", "Aydın", "Balıkesir", "Bilecik", "Bingöl", "Bitlis", "Bolu", "Burdur", "Bursa", "Çanakkale", "Çankırı", "Çorum", "Denizli", "Diyarbakır", "Edirne", "Elazığ", "Erzincan", "Erzurum", "Eskişehir", "Gaziantep", "Giresun", "Gümüşhane", "Hakkari", "Hatay", "Isparta", "Mersin", "İstanbul", "İzmir", "Kars", "Kastamonu", "Kayseri", "Kırklareli", "Kırşehir", "Kocaeli", "Konya", "Kütahya", "Malatya", "Manisa", "Kahramanmaraş", "Mardin", "Muğla", "Muş", "Nevşehir", "Niğde", "Ordu", "Rize", "Sakarya", "Samsun", "Siirt", "Sinop", "Sivas", "Tekirdağ", "Tokat", "Trabzon", "Tunceli", "Şanlıurfa", "Uşak", "Van", "Yozgat", "Zonguldak", "Aksaray", "Bayburt", "Karaman", "Kırıkkale", "Batman", "Şırnak", "Bartın", "Ardahan", "Iğdır", "Yalova", "Karabük", "Kilis", "Osmaniye", "Düzce"]

@app.route('/')
def index():
    return render_template('index.html', sehirler=sehirler)

@app.route('/predict', methods=['POST'])
def predict():
    yas = int(request.form.get('yas', 25))
    deneyim = int(request.form.get('deneyim', 3))
    egitim = request.form.get('egitim')
    meslek = request.form.get('meslek')
    secilen_sehir = request.form.get('sehir')

    # SENİN İSTEDİĞİN YAŞ-DENEYİM KONTROLÜ
    if deneyim > (yas - 18):
        hata = f"Mantıksal Hata: {yas} yaşında biri {deneyim} yıl deneyime sahip olamaz (Çalışma yaşı 18 kabul edilmiştir)."
        return render_template('index.html', sehirler=sehirler, hata=hata)

    # MAAŞ HESAPLAMA MANTIĞI
    baz = 25000
    if egitim == "Yüksek Lisans": baz += 10000
    elif egitim == "Lise": baz -= 5000
    
    meslek_farkı = {"Yazılım Mimarı": 40000, "Yapay Zeka Uzmanı": 35000, "Siber Güvenlik Uzmanı": 30000}
    maas = baz + (deneyim * 8500) + meslek_farkı.get(meslek, 18000)
    
    if secilen_sehir == "İstanbul": maas *= 1.3
    elif secilen_sehir in ["Ankara", "İzmir"]: maas *= 1.15

    asgari = 17002
    oran = round(maas / asgari, 1)
    tahmin_str = "{:,.0f}".format(maas).replace(",", ".")

    return render_template('index.html', tahmin=tahmin_str, sehirler=sehirler, oran=oran, secilen_sehir=secilen_sehir, yas=yas, deneyim=deneyim)
