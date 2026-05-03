from flask import Flask, render_template, request

app = Flask(__name__)

# 81 İl Listesi
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

    # --- MANTIKSAL KONTROL (Senin istediğin kısım) ---
    # Kişinin çalışmaya başlama yaşı en erken 18 kabul edilirse:
    max_deneyim = yas - 18
    if max_deneyim < 0: max_deneyim = 0 # 18 yaş altı için 0

    if deneyim > max_deneyim:
        hata_mesaji = f"Girdiğiniz yaşa ({yas}) göre deneyim süreniz en fazla {max_deneyim} yıl olabilir."
        return render_template('index.html', sehirler=sehirler, hata=hata_mesaji)
    # -----------------------------------------------

    # Maaş Algoritması
    base_maas = 25000
    if egitim == "Lise": base_maas = 20000
    
    maas = base_maas + (deneyim * 6000) + (yas * 200)
    
    # Eğitim ve Meslek Bonusları
    if egitim == "Yüksek Lisans": maas += 15000
    elif egitim == "Doktora": maas += 25000
    
    if meslek == "Yazılım Mimarı": maas += 35000
    elif meslek == "Yapay Zeka Uzmanı": maas += 20000

    if secilen_sehir in ["İstanbul", "Ankara", "İzmir"]: maas *= 1.2
    
    # Maaş Tavanı (Uçuk maaşları engellemek için)
    if maas > 400000: maas = 400000
    
    tahmin_sonuc = "{:,.0f}".format(maas).replace(",", ".")

    return render_template('index.html', tahmin=tahmin_sonuc, sehirler=sehirler, 
                           secilen_sehir=secilen_sehir, yas=yas, deneyim=deneyim)
