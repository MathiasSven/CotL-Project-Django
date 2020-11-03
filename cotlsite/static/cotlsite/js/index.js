const audio = document.getElementById('anthem');

function isPlaying(playerId) {
    let player = document.getElementById(playerId);
    return !player.paused && !player.ended && 0 < player.currentTime;
}

audio.volume = 0.4;

audio.addEventListener("play", function() {
    document.getElementById("play-button").style.display = "none"
    document.getElementById("pause-button").style.display = "flex"
});

audio.addEventListener("pause", function() {
    document.getElementById("play-button").style.display = "flex"
    document.getElementById("pause-button").style.display = "none"
});

document.getElementById("play-pause-button").addEventListener("click", function () {
  if(isPlaying('anthem')) {
    audio.pause();
    document.getElementById("play-button").style.display = "flex"
    document.getElementById("pause-button").style.display = "none"
  }else{
    audio.play();
    document.getElementById("play-button").style.display = "none"
    document.getElementById("pause-button").style.display = "flex"
  }

});