const Vue = require('vue');

const board = require('./components/board.vue');
const { formatMoves, formatPlayer } = require('./helpers/formatting');

const boardView = new Vue({
  data: {
    tiles: [],
  },
  components: { board },
});

function showBoard() {
  window.fetch('/board').then((response) => {
    response.json().then((data) => {
      boardView.tiles = data;
    });
  });
}

function extraForMove(kind, cardValue, cardColor, tileValue, tileColor) {
  if (kind === 'plan') {
    return {
      target_tile: { value: cardValue, color: cardColor },
      wish: 'resource',
    };
  }
  if (kind === 'urbanize') {
    return {
      marker: cardValue,
      direction: 'up',
      new_tile: { value: tileValue, color: tileColor },
    };
  }
  if (kind === 'build_up') {
    return {
      target_tile: { value: cardValue, color: cardColor },
      new_tile: { value: tileValue, color: tileColor },
    };
  }

  return {};
}

function executeMove(event) {
  const inputContainer = event.target.parentNode;
  const kind = inputContainer.querySelector('.js-move-input').value;
  let [cardValue, cardColor] = inputContainer.querySelector('.js-card-input').value.split('_');
  const [tileValue, tileColor] = inputContainer.querySelector('.js-tile-input').value.split('_');
  const parsedTileValue = parseInt(tileValue, 10);
  const parsedCardValue = parseInt(cardValue, 10) || cardValue;
  cardColor = cardColor === 'undefined' ? undefined : cardColor;
  window.fetch('/make_move/Lisa', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      kind,
      cardTarget: { value: parsedCardValue, color: cardColor },
      extra: extraForMove(kind, parsedCardValue, cardColor, parsedTileValue, tileColor),
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
  window.fetch('/play').then((response) => {
    response.json().then((data) => {
      const gameLog = document.querySelector('.js-game-log');
      gameLog.innerHTML = `${formatMoves(data)} </br></br> ${gameLog.innerHTML}`;
      update();
      play();
    });
  });
}

document.addEventListener('DOMContentLoaded', () => {
  boardView.$mount('#board');
  update();
  play();
});
