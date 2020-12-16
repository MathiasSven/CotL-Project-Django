const max = 100

let slider_types = ['Soldier', 'Tank', 'Aircraft', 'Ships', 'Infra'];

sliders = []
slider_values = []
slider_locks = []

for (const slider_type of slider_types) {
    sliders.push(document.getElementById(`${slider_type.toLowerCase()}Slider`));
    slider_values.push(document.getElementById(`value${slider_type}`));
    slider_locks.push(document.getElementById(`lock${slider_type}`));
}

function propagator(x, diff) {
    while (diff !== 0) {
        for (let i = 0; i < sliders.length; i++) {
            if (i === x || ! slider_locks[i].classList.contains('unlocked')) {
                continue;
            } else if (diff > 0) {
                if (sliders[i].value === sliders[i].min) {
                    continue;
                }
            } else if (diff < 0) {
                if (sliders[i].value === sliders[i].max) {
                    continue;
                }
            }

            if (diff !== 0) {
                if (diff > 0) {
                    diff--
                    sliders[i].value--;
                    sliders[i].recent--;
                } else if (diff < 0) {
                    diff++;
                    sliders[i].value++;
                    sliders[i].recent++;
                }

                slider_values[i].value = sliders[i].value
            }
        }
    }
}

for (let i = 0; i < sliders.length; i++) {
    slider_values[i].value = sliders[i].value;

    sliders[i]['recent'] = sliders[i].value;
    slider_values[i]['recent'] = slider_values[i].value;

    sliders[i].oninput = function () {

        let difference = this.value - this.recent;
        this.recent = this.value;

        slider_values[i].value = this.value;
        slider_values[i].recent = this.value;

        propagator(i, difference);
    };

    slider_values[i].oninput = function () {

        let difference = this.value - this.recent
        this.recent = this.value

        sliders[i].value = Math.round(this.value)
        sliders[i].vnow = this.value
        sliders[i].recent = this.value

        propagator(i, difference)
    }
}

for (const lock of document.querySelectorAll('.lock')) {
    if (lock !== slider_locks[4]) {
        lock.classList.toggle('unlocked')
    }
    lock.addEventListener('click', function () {
        this.classList.toggle('unlocked')
    });
}