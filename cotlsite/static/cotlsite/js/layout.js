document.addEventListener('DOMContentLoaded', function () {

    const avatar_dropdown = document.querySelector('.avatar_dropdown');
    avatar_dropdown.style.visibility = 'hidden';
    avatar_dropdown.style.opacity = '0';
    avatar_dropdown.style.transform = 'translateY(-20px)';

    const offClick = () => {
        if (avatar_dropdown.style.visibility === 'visible') {
            toggle_avatar_dropdown(avatar_dropdown);
        }
        document.removeEventListener('click', offClick);
    }

    document.querySelector('#avatar').addEventListener('click', (e) => {
        e.stopPropagation();
        toggle_avatar_dropdown(avatar_dropdown);
        if (avatar_dropdown.style.visibility === 'visible') {
            document.addEventListener('click', offClick);
        }
    });
});

function toggle_avatar_dropdown(avatar_dropdown) {
    if (avatar_dropdown.style.visibility === 'hidden') {
        avatar_dropdown.style.visibility = 'visible';
        avatar_dropdown.style.opacity = '1';
        avatar_dropdown.style.transform = 'translateY(0px)';
    } else {
        avatar_dropdown.style.visibility = 'hidden';
        avatar_dropdown.style.opacity = '0';
        avatar_dropdown.style.transform = 'translateY(-20px)';
    }
}