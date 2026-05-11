window.onload = function () {

    // YAŞ - DENEYİM
    const yasInput =
        document.getElementById("yasInput");

    const deneyimInput =
        document.getElementById("deneyimInput");

    function updateMaxDeneyim() {

        if (!yasInput || !deneyimInput) return;

        const yas =
            parseInt(yasInput.value) || 18;

        const maxDeneyim = yas - 18;

        deneyimInput.max = maxDeneyim;

        if (
            parseInt(deneyimInput.value)
            > maxDeneyim
        ) {

            deneyimInput.value = maxDeneyim;
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
