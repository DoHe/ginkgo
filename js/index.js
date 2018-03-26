const { formatMoves, formatBoard, formatPlayer } = require('./helpers/formatting');

function showBoard() {
  window.fetch('/board').then((response) => {
    response.json().then((data) => {
      document.querySelector('.js-board').innerHTML = formatBoard(data);
    });
  });
}

function extraForMove(kind, cardValue, cardColor, tileValue, tileColor) {
  const parsedTileValue = parseInt(tileValue, 10);
  const parsedCardValue = parseInt(cardValue, 10);
  if (kind === 'plan') {
    return {
      target_tile: { value: parsedCardValue, color: cardColor },
      wish: 'resource',
    };
  }
  if (kind === 'urbanize') {
    return {
      marker: cardValue,
      direction: 'up',
      new_tile: { value: parsedTileValue, color: tileColor },
    };
  }
  if (kind === 'build_up') {
    return {
      target_tile: { value: parsedCardValue, color: cardColor },
      new_tile: { value: parsedTileValue, color: tileColor },
    };
  }

  return {};
}

function executeMove(event) {
  const inputContainer = event.target.parentNode;
  const kind = inputContainer.querySelector('.js-move-input').value;
  const [cardValue, cardColor] = inputContainer.querySelector('.js-card-input').value.split('_');
  const [tileValue, tileColor] = inputContainer.querySelector('.js-tile-input').value.split('_');
  const cardTarget = { value: cardValue };
  if (cardColor !== 'undefined') {
    cardTarget.color = cardColor;
  }
  window.fetch('/make_move/Lisa', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      kind,
      cardTarget,
      extra: extraForMove(kind, cardValue, cardColor, tileValue, tileColor),
    }),
  });
}

function showPlayer(playerName) {
  window.fetch(`/players/${playerName}`).then((response) => {
    response.json().then((data) => {
      const player = document.querySelector(`.js-player[data-player-name=${playerName}]`);
      if (player) {
        player.innerHTML = formatPlayer(data);
      } else {
        document.querySelector('.js-players').innerHTML += `<div class="player js-player" data-player-name="${data.name}">${formatPlayer(data)}</div>`;
      }
      const executeButton = document.querySelector(`.js-player[data-player-name=${playerName}] .js-execute-button`);
      if (executeButton) {
        executeButton.addEventListener('click', executeMove);
      }
    });
  });
}

function showPlayers() {
  window.fetch('/players').then((response) => {
    response.json().then(players => players.sort().forEach(showPlayer));
  });
}

function update() {
  showBoard();
  showPlayers();
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
      play();
    });
  });
}

document.addEventListener('DOMContentLoaded', () => {
  document.querySelector('.js-play-button').addEventListener('click', play);
  update();
  play();
});
