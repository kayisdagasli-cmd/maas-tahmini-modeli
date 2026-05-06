from flask import Flask, render_template, request

app = Flask(__name__)

# Veri Setleri
iller = [
    "Adana", "Adıyaman", "Afyonkarahisar", "Ağrı", "Amasya", "Ankara", "Antalya", "Artvin", "Aydın", "Balıkesir",
    "Bilecik", "Bingöl", "Bitlis", "Bolu", "Burdur", "Bursa", "Çanakkale", "Çankırı", "Çorum", "Denizli",
    "Diyarbakır", "Edirne", "Elazığ", "Erzincan", "Erzurum", "Eskişehir", "Gaziantep", "Giresun", "Gümüşhane", "Hakkari",
    "Hatay", "Isparta", "Mersin", "İstanbul", "İzmir", "Kars", "Kastamonu", "Kayseri", "Kırklareli", "Kırşehir",
    "Kocaeli", "Konya", "Kütahya", "Malatya", "Manisa", "Kahramanmaraş", "Mardin", "Muğla", "Muş", "Nevşehir",
    "Niğde", "Ordu", "Rize", "Sakarya", "Samsun", "Siirt", "Sinop", "Sivas", "Tekirdağ", "Tokat",
    "Trabzon", "Tunceli", "Şanlıurfa", "Uşak", "Van", "Yozgat", "Zonguldak", "Aksaray", "Bayburt", "Karaman",
    "Kırıkkale", "Batman", "Şırnak", "Bartın", "Ardahan", "Iğdır", "Yalova", "Karabük", "Kilis", "Osmaniye", "Düzce"
]

meslekler = [
    "Yazılım Mühendisi", "Veri Analisti", "Proje Yöneticisi", "Pazarlama Uzmanı", 
    "İnsan Kaynakları Uzmanı", "Finans Danışmanı", "Satış Temsilcisi", 
    "Grafik Tasarımcı", "Sistem Yönetici", "Müşteri İlişkileri Yöneticisi"
]

egitim_durumlari = ["Lise", "Lisans", "Yüksek Lisans", "Doktora"]

@app.route('/', methods=['GET', 'POST'])
def index():
    tahmin = None
    hata = None
    
    if request.method == 'POST':
        try:
            yas = int(request.form.get('yas'))
            deneyim = int(request.form.get('deneyim'))
            egitim = request.form.get('egitim')
            meslek = request.form.get('meslek')
            sehir = request.form.get('sehir')

            # Yaş ve Deneyim Mantık Kontrolü
            if deneyim > (yas - 18):
                hata = f"{yas} yaşındaki biri en fazla {yas-18} yıl deneyime sahip olabilir."
            else:
                # Temel Maaş Algoritması (Örnektir, modelinizle değiştirebilirsiniz)
                base = 25000
                meslek_kat = (meslekler.index(meslek) + 1) * 2000
                deneyim_kat = deneyim * 4500
                egitim_kat = egitim_durumlari.index(egitim) * 7000
                sehir_kat = 10000 if sehir == "İstanbul" else 5000 if sehir in ["Ankara", "İzmir"] else 0
                
                tahmin = base + meslek_kat + deneyim_kat + egitim_kat + sehir_kat
                
        except ValueError:
            hata = "Lütfen tüm alanları doğru doldurun."

    return render_template('index.html', iller=iller, meslekler=meslekler, 
                           egitimler=egitim_durumlari, tahmin=tahmin, hata=hata)

if __name__ == '__main__':
    app.run(debug=True)
