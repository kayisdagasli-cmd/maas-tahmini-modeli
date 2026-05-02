from flask import Flask, render_template, request
import pandas as pd
from sklearn.linear_model import LinearRegression

ILLER = [
    "Adana","Adiyaman","Afyon","Agri","Amasya","Ankara","Antalya","Artvin","Aydin",
    "Balikesir","Bilecik","Bingol","Bitlis","Bolu","Burdur","Bursa","Canakkale",
    "Cankiri","Corum","Denizli","Diyarbakir","Edirne","Elazig","Erzincan","Erzurum",
    "Eskisehir","Gaziantep","Giresun","Gumushane","Hakkari","Hatay","Isparta",
    "Mersin","Istanbul","Izmir","Kars","Kastamonu","Kayseri","Kirklareli","Kirsehir",
    "Kocaeli","Konya","Kutahya","Malatya","Manisa","Kahramanmaras","Mardin","Mugla",
    "Mus","Nevsehir","Nigde","Ordu","Rize","Sakarya","Samsun","Siirt","Sinop",
    "Sivas","Tekirdag","Tokat","Trabzon","Tunceli","Sanliurfa","Usak","Van",
    "Yozgat","Zonguldak","Aksaray","Bayburt","Karaman","Kirikkale","Batman",
    "Sirnak","Bartin","Ardahan","Igdir","Yalova","Karabuk","Kilis","Osmaniye","Duzce",
]

IL_GOSTERIM = {
    "Adana":"Adana","Adiyaman":"Adıyaman","Afyon":"Afyonkarahisar","Agri":"Ağrı",
    "Amasya":"Amasya","Ankara":"Ankara","Antalya":"Antalya","Artvin":"Artvin",
    "Aydin":"Aydın","Balikesir":"Balıkesir","Bilecik":"Bilecik","Bingol":"Bingöl",
    "Bitlis":"Bitlis","Bolu":"Bolu","Burdur":"Burdur","Bursa":"Bursa",
    "Canakkale":"Çanakkale","Cankiri":"Çankırı","Corum":"Çorum","Denizli":"Denizli",
    "Diyarbakir":"Diyarbakır","Edirne":"Edirne","Elazig":"Elazığ","Erzincan":"Erzincan",
    "Erzurum":"Erzurum","Eskisehir":"Eskişehir","Gaziantep":"Gaziantep","Giresun":"Giresun",
    "Gumushane":"Gümüşhane","Hakkari":"Hakkari","Hatay":"Hatay","Isparta":"Isparta",
    "Mersin":"Mersin","Istanbul":"İstanbul","Izmir":"İzmir","Kars":"Kars",
    "Kastamonu":"Kastamonu","Kayseri":"Kayseri","Kirklareli":"Kırklareli","Kirsehir":"Kırşehir",
    "Kocaeli":"Kocaeli","Konya":"Konya","Kutahya":"Kütahya","Malatya":"Malatya",
    "Manisa":"Manisa","Kahramanmaras":"Kahramanmaraş","Mardin":"Mardin","Mugla":"Muğla",
    "Mus":"Muş","Nevsehir":"Nevşehir","Nigde":"Niğde","Ordu":"Ordu",
    "Rize":"Rize","Sakarya":"Sakarya","Samsun":"Samsun","Siirt":"Siirt",
    "Sinop":"Sinop","Sivas":"Sivas","Tekirdag":"Tekirdağ","Tokat":"Tokat",
    "Trabzon":"Trabzon","Tunceli":"Tunceli","Sanliurfa":"Şanlıurfa","Usak":"Uşak",
    "Van":"Van","Yozgat":"Yozgat","Zonguldak":"Zonguldak","Aksaray":"Aksaray",
    "Bayburt":"Bayburt","Karaman":"Karaman","Kirikkale":"Kırıkkale","Batman":"Batman",
    "Sirnak":"Şırnak","Bartin":"Bartın","Ardahan":"Ardahan","Igdir":"Iğdır",
    "Yalova":"Yalova","Karabuk":"Karabük","Kilis":"Kilis","Osmaniye":"Osmaniye","Duzce":"Düzce",
}

MESLEKLER = ["Yazilim","VeriAnalisti","VeriBilimci","SiberGuvenlik","ProjeYoneticisi"]
MESLEK_GOSTERIM = {
    "Yazilim":"Yazılım","VeriAnalisti":"Veri Analisti","VeriBilimci":"Veri Bilimci",
    "SiberGuvenlik":"Siber Güvenlik","ProjeYoneticisi":"Proje Yöneticisi",
}
EGITIM_GOSTERIM = ["Lise","Lisans","Yüksek Lisans / Doktora"]

def egit_modeli():
    veri = []
    for i, il in enumerate(ILLER):
        yas = 22 + (i % 20)
        deneyim = i % 15
        egitim = i % 3
        meslek = (i % 5) + 1
        maas = 15000 + deneyim * 3000 + (i % 3) * 5000 + (i % 5) * 2000
        veri.append([yas, deneyim, egitim, i, meslek, maas])
    df = pd.DataFrame(veri, columns=["yas","deneyim","egitim","sehir","meslek","maas"])
    m = LinearRegression()
    m.fit(df[["yas","deneyim","egitim","sehir","meslek"]], df["maas"])
    return m

MODEL = egit_modeli()
app = Flask(__name__)

@app.route("/", methods=["GET"])
def anasayfa():
    return render_template("index.html",
        iller=ILLER, il_gosterim=IL_GOSTERIM,
        meslekler=MESLEKLER, meslek_gosterim=MESLEK_GOSTERIM,
        egitim_gosterim=EGITIM_GOSTERIM,
        sonuc=None, hata=None,
        form={"yas":25,"deneyim":3,"egitim":1,"sehir":33,"meslek":1},
        karsilastirma=None)

@app.route("/tahmin", methods=["POST"])
def tahmin():
    hata = None
    sonuc = None
    karsilastirma = None
    try:
        yas = int(request.form.get("yas", 0))
        deneyim = int(request.form.get("deneyim", 0))
        egitim = int(request.form.get("egitim", 0))
        sehir = int(request.form.get("sehir", 0))
        meslek = int(request.form.get("meslek", 0))
        if yas < 18 or yas > 65:
            raise ValueError("Yas 18 ile 65 arasinda olmalidir.")
        if deneyim < 0 or deneyim > yas - 18:
            raise ValueError(f"{yas} yasindaki biri en fazla {yas-18} yil deneyime sahip olabilir.")
        sonuc = int(MODEL.predict([[yas, deneyim, egitim, sehir, meslek]])[0])
        karsilastirma = sorted(
            [{"il": IL_GOSTERIM[ILLER[i]], "maas": int(MODEL.predict([[yas, deneyim, egitim, i, meslek]])[0]), "secili": (i == sehir)}
             for i in range(len(ILLER))],
            key=lambda x: x["maas"], reverse=True
        )
        form = {"yas":yas,"deneyim":deneyim,"egitim":egitim,"sehir":sehir,"meslek":meslek}
    except ValueError as e:
        hata = str(e)
        form = {
            "yas": request.form.get("yas", 25),
            "deneyim": request.form.get("deneyim", 3),
            "egitim": int(request.form.get("egitim", 1)),
            "sehir": int(request.form.get("sehir", 33)),
            "meslek": int(request.form.get("meslek", 1))
        }
    return render_template("index.html",
        iller=ILLER, il_gosterim=IL_GOSTERIM,
        meslekler=MESLEKLER, meslek_gosterim=MESLEK_GOSTERIM,
        egitim_gosterim=EGITIM_GOSTERIM,
        sonuc=sonuc, hata=hata, form=form, karsilastirma=karsilastirma)

if __name__ == "__main__":
    app.run(debug=True)
