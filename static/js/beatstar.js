document.addEventListener('DOMContentLoaded', function() {
    var playButton = document.querySelector('.play');
    var prevButton = document.querySelector('.prev');
    var nextButton = document.querySelector('.next');
    var audioPlayer = document.getElementById('audio');
  
    playButton.addEventListener('click', function() {
      if (audioPlayer.paused) {
        audioPlayer.play();
        playButton.textContent = 'Pause';
      } else {
        audioPlayer.pause();
        playButton.textContent = 'Play';
      }
    });
  
    prevButton.addEventListener('click', function() {
      // Logic to navigate to the previous track
    });
  
    nextButton.addEventListener('click', function() {
      // Logic to navigate to the next track
    });
  
    // Additional JavaScript for interactive elements
  });
  