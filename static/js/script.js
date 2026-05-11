const yasInput = document.getElementById('yasInput');
const deneyimInput = document.getElementById('deneyimInput');

function updateMaxDeneyim() {

    if (!yasInput || !deneyimInput) return;

    const yas = parseInt(yasInput.value);
    const maxDeneyim = yas - 18;

    deneyimInput.max = maxDeneyim > 0 ? maxDeneyim : 0;

    if (parseInt(deneyimInput.value) > maxDeneyim) {

        deneyimInput.value = maxDeneyim > 0
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


// COUNTUP
const maasElement = document.getElementById('sayac_ana');

if (maasElement) {

    const rawValue = maasElement.dataset.value;

    if (rawValue) {

        const targetValue = parseInt(rawValue);

        const countUp = new CountUp(
            'sayac_ana',
            targetValue,
            {
                separator: '.',
                decimal: ',',
                duration: 2.5,
                suffix: ' ₺'
            }
        );

        if (!countUp.error) {
            countUp.start();
        }
    }
}


// GAUGE
const gauge = document.getElementById('gauge_move');

if (gauge) {

    const oran = parseFloat(gauge.dataset.oran);

    setTimeout(() => {

        let deg = (oran * 18) - 45;

        if (deg > 135) {
            deg = 135;
        }

        gauge.style.transform =
            `rotate(${deg}deg)`;

    }, 400);
}
