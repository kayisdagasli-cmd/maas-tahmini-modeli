window.addEventListener('DOMContentLoaded', () => {

    // YAŞ - DENEYİM KONTROLÜ
    const yasInput = document.getElementById('yasInput');
    const deneyimInput = document.getElementById('deneyimInput');

    function updateMaxDeneyim() {

        if (!yasInput || !deneyimInput) return;

        const yas = parseInt(yasInput.value) || 18;
        const maxDeneyim = yas - 18;

        deneyimInput.max = maxDeneyim > 0
            ? maxDeneyim
            : 0;

        if (parseInt(deneyimInput.value) > maxDeneyim) {

            deneyimInput.value =
                maxDeneyim > 0
                ? maxDeneyim
                : 0;
        }
    }

    if (yasInput && deneyimInput) {

        yasInput.addEventListener(
            'input',
            updateMaxDeneyim
        );

        updateMaxDeneyim();
    }


    // MAAŞ ANİMASYONU
    const maasElement =
        document.getElementById('sayac_ana');

    if (maasElement) {

        const value =
            maasElement.getAttribute('data-value');

        const targetValue = parseInt(value);

        if (!isNaN(targetValue)) {

            const countUp = new CountUp(
                'sayac_ana',
                targetValue,
                {
                    separator: '.',
                    decimal: ',',
                    duration: 2.2,
                    suffix: ' ₺'
                }
            );

            if (!countUp.error) {

                countUp.start();

            } else {

                maasElement.innerText =
                    targetValue.toLocaleString('tr-TR') + ' ₺';
            }
        }
    }


    // GAUGE
    const gauge =
        document.getElementById('gauge_move');

    if (gauge) {

        const oran =
            parseFloat(
                gauge.getAttribute('data-oran')
            );

        setTimeout(() => {

            let deg = (oran * 18) - 45;

            if (deg > 135) {
                deg = 135;
            }

            gauge.style.transform =
                `rotate(${deg}deg)`;

        }, 500);
    }

});
