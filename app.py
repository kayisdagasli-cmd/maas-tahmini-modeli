<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Maaş Tahmin Uygulaması</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&display=swap" rel="stylesheet">
    <style>
        :root { --bordo: #800000; --koyu: #121212; --bg: #080808; }
        body { background: var(--bg); color: #fff; font-family: 'Inter', sans-serif; margin: 0; padding: 8px; font-size: 0.8rem; }
        .container { max-width: 420px; margin: auto; }

        /* Kart Stilleri */
        .card { 
            background: var(--koyu); border: 1px solid #222; border-radius: 12px; 
            padding: 12px; margin-bottom: 10px; border-top: 3px solid var(--bordo);
            box-shadow: 0 4px 10px rgba(0,0,0,0.5);
        }

        h2 { font-size: 0.95rem; margin: 0 0 4px 0; font-weight: 800; text-transform: uppercase; }
        .sub { color: #666; font-size: 0.6rem; margin-bottom: 8px; }

        /* Form Düzeni */
        .row { display: flex; gap: 8px; margin-bottom: 8px; }
        label { display: block; color: #888; font-size: 0.6rem; margin-bottom: 2px; }
        input, select { 
            background: #1a1a1a; border: 1px solid #333; color: #fff; 
            padding: 8px; border-radius: 6px; width: 100%; font-size: 0.8rem; box-sizing: border-box;
        }

        .btn { 
            background: var(--bordo); color: #fff; border: none; padding: 12px; 
            width: 100%; border-radius: 8px; font-weight: bold; margin-top: 8px; cursor: pointer;
        }

        /* 81 İl Grafik Alanı */
        .chart-scroll { 
            overflow-x: auto; white-space: nowrap; padding-bottom: 10px; 
            scrollbar-width: none; -webkit-overflow-scrolling: touch;
        }
        .chart-wrap { display: inline-flex; align-items: flex-end; gap: 4px; height: 100px; padding-top: 10px; }
        .bar-container { display: flex; flex-direction: column; align-items: center; width: 28px; }
        .bar { width: 12px; background: var(--bordo); opacity: 0.3; border-radius: 2px; transition: 0.3s; }
        .bar.active { opacity: 1; background: #ff1a1a; box-shadow: 0 0 8px #ff1a1a; }
        .city-label { font-size: 0.5rem; color: #555; transform: rotate(-45deg); margin-top: 8px; }

        /* Haberler Alanı (Düzeltildi) */
        .news-row { display: flex; gap: 10px; overflow-x: auto; padding: 5px 0; scrollbar-width: none; }
        .news-card { 
            min-width: 130px; max-width: 130px; flex-shrink: 0;
            background: #1a1a1a; padding: 10px; border-radius: 8px; border-bottom: 3px solid var(--bordo);
        }

        /* Analiz Bölümü */
        .grid-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 8px; }
        .small-box { background: #181818; padding: 10px; border-radius: 8px; border-left: 3px solid var(--bordo); }
        
        .hata-mesaj { color: #ff4444; font-size: 0.65rem; font-weight: bold; margin-top: 4px; }
        .res-highlight { font-size: 1.8rem; font-weight: 900; color: #ff1a1a; text-align: center; }
    </style>
</head>
<body>

<div class="container">
    <div class="card">
        <h2>Maaş Tahmini</h2>
        <p class="sub">Yaş ve deneyim bazlı gerçekçi analiz</p>
        <form method="POST">
            <div class="row">
                <div style="flex:1">
                    <label>Yaş</label>
                    <input type="number" name="yas" value="{{ request.form.get('yas', '25') }}" min="18" max="65">
                </div>
                <div style="flex:1">
                    <label>Deneyim (Yıl)</label>
                    <input type="number" name="deneyim" value="{{ request.form.get('deneyim', '3') }}">
                </div>
            </div>
            {% if hata %}<div class="hata-mesaj">{{ hata }}</div>{% endif %}

            <label style="margin-top:8px;">Eğitim Seviyesi</label>
            <select name="egitim">
                {% for e in ["Lise", "Lisans", "Yüksek Lisans", "Doktora"] %}
                <option value="{{e}}" {% if request.form.get('egitim') == e %}selected{% endif %}>{{e}}</option>
                {% endfor %}
            </select>

            <label style="margin-top:8px;">Meslek</label>
            <select name="meslek">
                {% for m in meslekler %}<option value="{{m}}" {% if request.form.get('meslek') == m %}selected{% endif %}>{{m}}</option>{% endfor %}
            </select>

            <label style="margin-top:8px;">Şehir</label>
            <select name="sehir">
                {% for s in iller %}<option value="{{s}}" {% if request.form.get('sehir') == s %}selected{% endif %}>{{s}}</option>{% endfor %}
            </select>

            <button class="btn">MAAŞI HESAPLA</button>
        </form>
    </div>

    {% if tahmin and not hata %}
    <div class="card" style="border: 2px solid var(--bordo); background: rgba(128,0,0,0.05);">
        <p style="text-align:center; font-size:0.65rem; color:#888; margin:0;">Tahmini Net Aylık Maaş</p>
        <div class="res-highlight">{{ "{:,.0f}".format(tahmin).replace(',', '.') }} TL</div>
    </div>

    <div class="card">
        <div class="grid-2">
            <div class="small-box">
                <label>Asgari Oranı</label>
                <div style="font-weight:900; color:var(--bordo); font-size:1.1rem;">{{asgari_kati}} Katı</div>
            </div>
            <div class="small-box">
                <label>Geçim Endeksi</label>
                <div style="font-weight:bold; color:#00ff00; font-size:0.8rem;">78/100 (İyi)</div>
            </div>
        </div>
    </div>
    {% endif %}

    <div class="card">
        <h2>81 İl Karşılaştırması</h2>
        <div class="chart-scroll">
            <div class="chart-wrap">
                {% for s in iller %}
                <div class="bar-container">
                    <div class="bar {% if s == request.form.get('sehir') %}active{% endif %}" 
                         style="height: {{ range(25, 85)|random }}%;"></div>
                    <span class="city-label">{{s[:3]}}</span>
                </div>
                {% endfor %}
            </div>
        </div>
    </div>

    <div class="card">
        <h2>Sektör Haberleri</h2>
        <div class="news-row">
            {% for h in haberler %}
            <div class="news-card">
                <label style="color:var(--bordo); font-weight:900;">{{h.kategori}}</label>
                <div style="font-size:0.7rem; font-weight:bold; margin-top:4px;">{{h.baslik}}</div>
            </div>
            {% endfor %}
        </div>
    </div>
</div>

</body>
</html>
