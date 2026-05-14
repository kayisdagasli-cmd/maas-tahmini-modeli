window.onload = function () {

    // YAŞ - DENEYİM
    const yasInput =
        document.getElementById("yasInput");

    const deneyimInput =
        document.getElementById("deneyimInput");

    function updateMaxDeneyim() {

        if (!yasInput || !deneyimInput) return;

        // Yaş boşsa minimum 18 kabul et
        const yas =
            parseInt(yasInput.value) || 18;

        // Negatif çıkmasını engelle
        const maxDeneyim =
            Math.max(0, yas - 18);

        deneyimInput.max = maxDeneyim;

        // Deneyim boşsa 0 kabul et
        const mevcutDeneyim =
            parseInt(deneyimInput.value) || 0;

        if (mevcutDeneyim > maxDeneyim) {

            deneyimInput.value = maxDeneyim;
        }

        // Negatif deneyimi engelle
        if (mevcutDeneyim < 0) {

            deneyimInput.value = 0;
        }
    }

    if (yasInput && deneyimInput) {

        yasInput.addEventListener(
            "input",
            updateMaxDeneyim
        );

        updateMaxDeneyim();
    }


    // GAUGE
    const gauge =
        document.getElementById("gauge_move");

    if (gauge) {

        const oran =
            parseFloat(
                gauge.dataset.oran
            );

        let deg = (oran * 18) - 45;

        if (deg > 135) {
            deg = 135;
        }

        gauge.style.transform =
            `rotate(${deg}deg)`;
    }

};
