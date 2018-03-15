const { formatMoves, formatBoard, formatPlayer } = require('./helpers/formatting');

function showBoard() {
  window.fetch('/board').then((response) => {
    response.json().then((data) => {
      document.querySelector('.js-board').innerHTML = formatBoard(data);
    });
  });
}

function showPlayer() {
  window.fetch('/player/Lisa').then((response) => {
    response.json().then((data) => {
      document.querySelector('.js-player').innerHTML = formatPlayer(data);
    });
  });
}

function update() {
  showBoard();
  showPlayer();
}

function play() {
  const playButton = document.querySelector('.js-play-button');
  playButton.disabled = true;
  window.fetch('/play').then((response) => {
    response.json().then((data) => {
      const gameLog = document.querySelector('.js-game-log');
      gameLog.innerHTML = `${formatMoves(data)} </br></br> ${gameLog.innerHTML}`;
      update();
      playButton.disabled = false;
    });
  });

  window.fetch('/make_move/Lisa', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      kind: 'plan',
      cardTarget: {
        value: 'A',
      },
      extra: {
        wish: 'resource',
      },
    }),
  });
}

document.addEventListener('DOMContentLoaded', () => {
  document.querySelector('.js-play-button').addEventListener('click', play);
  update();
});
