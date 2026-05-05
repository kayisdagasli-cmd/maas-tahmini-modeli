from flask import Flask, render_template, request

app = Flask(__name__)

# 81 İl Listesi
sehirler = ["Adana", "Adıyaman", "Afyonkarahisar", "Ağrı", "Amasya", "Ankara", "Antalya", "Artvin", "Aydın", "Balıkesir", "Bilecik", "Bingöl", "Bitlis", "Bolu", "Burdur", "Bursa", "Çanakkale", "Çankırı", "Çorum", "Denizli", "Diyarbakır", "Edirne", "Elazığ", "Erzincan", "Erzurum", "Eskişehir", "Gaziantep", "Giresun", "Gümüşhane", "Hakkari", "Hatay", "Isparta", "Mersin", "İstanbul", "İzmir", "Kars", "Kastamonu", "Kayseri", "Kırklareli", "Kırşehir", "Kocaeli", "Konya", "Kütahya", "Malatya", "Manisa", "Kahramanmaraş", "Mardin", "Muğla", "Muş", "Nevşehir", "Niğde", "Ordu", "Rize", "Sakarya", "Samsun", "Siirt", "Sinop", "Sivas", "Tekirdağ", "Tokat", "Trabzon", "Tunceli", "Şanlıurfa", "Uşak", "Van", "Yozgat", "Zonguldak", "Aksaray", "Bayburt", "Karaman", "Kırıkkale", "Batman", "Şırnak", "Bartın", "Ardahan", "Iğdır", "Yalova", "Karabük", "Kilis", "Osmaniye", "Düzce"]

# 10 Popüler Meslek
meslekler = ["Yazılım Mimarı", "Yapay Zeka Uzmanı", "Siber Güvenlik Uzmanı", "Veri Analisti", "DevOps Uzmanı", "Oyun Geliştirici", "Full Stack Developer", "Mobil Uygulama Geliştirici", "Bulut Sistem Mühendisi", "Veri Bilimci"]

@app.route('/')
def index():
    return render_template('index.html', sehirler=sehirler, meslekler=meslekler)

@app.route('/predict', methods=['POST'])
def predict():
    yas = int(request.form.get('yas', 25))
    deneyim = int(request.form.get('deneyim', 3))
    egitim = request.form.get('egitim')
    meslek = request.form.get('meslek')
    secilen_sehir = request.form.get('sehir')

    # YAŞ-DENEYİM KONTROLÜ
    if deneyim > (yas - 18):
        hata = f"Mantıksal Hata: {yas} yaşında biri {deneyim} yıl deneyime sahip olamaz (Çalışma yaşı 18 kabul edilmiştir)."
        return render_template('index.html', sehirler=sehirler, meslekler=meslekler, hata=hata)

    # MAAŞ HESAPLAMA (Gerçekçi çarpanlar)
    baz = 24000
    if egitim == "Lise": baz = 18500
    elif egitim == "Yüksek Lisans": baz = 32000
    elif egitim == "Doktora": baz = 40000
    
    maas = baz + (deneyim * 7500)
    if "Mimarı" in meslek or "Zeka" in meslek: maas += 15000
    
    if secilen_sehir == "İstanbul": maas *= 1.3
    elif secilen_sehir in ["Ankara", "İzmir"]: maas *= 1.15

    asgari = 17002
    oran = round(maas / asgari, 1)
    tahmin_str = "{:,.0f}".format(maas).replace(",", ".")

    return render_template('index.html', tahmin=tahmin_str, sehirler=sehirler, meslekler=meslekler, 
                           oran=oran, secilen_sehir=secilen_sehir, yas=yas, deneyim=deneyim)
