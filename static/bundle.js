(function(){function e(t,n,r){function s(o,u){if(!n[o]){if(!t[o]){var a=typeof require=="function"&&require;if(!u&&a)return a(o,!0);if(i)return i(o,!0);var f=new Error("Cannot find module '"+o+"'");throw f.code="MODULE_NOT_FOUND",f}var l=n[o]={exports:{}};t[o][0].call(l.exports,function(e){var n=t[o][1][e];return s(n?n:e)},l,l.exports,e,t,n,r)}return n[o].exports}var i=typeof require=="function"&&require;for(var o=0;o<r.length;o++)s(r[o]);return s}return e})()({1:[function(require,module,exports){
const moveKinds = ['plan', 'urbanize', 'build_up'];

function isSpace(pieceData) {
  return pieceData.name === 'space';
}

function gridStyle(column, row) {
  return `style="grid-column: ${column + 1}; grid-row=${row + 1};"`;
}

function formatBoardPiece(pieceData, column, row) {
  const {
    name, value, color, owner_color, resources
  } = pieceData;
  if (name === 'marker') {
    return `<div class="circle bg--green" ${gridStyle(column, row)}>${value}</div>`;
  } else if (name === 'tile') {
    return `<div class="rect bg--${color}" ${gridStyle(column, row)}>
                ${value}/<span class="fnt--${owner_color}">${resources}</span>
            </div>`;
  }
  return '';
}

function formatTile(tileData) {
  return `<div class="rect bg--${tileData.color}">${tileData.value}</div>`;
}

function formatCard(cardData) {
  const textClass = cardData.target.color ? `fnt--${cardData.target.color}` : '';
  return `<div class="rect bg--green ${textClass}">${cardData.target.value}</div>`;
}

function formatRow(rowData, rowIndex) {
  return `${rowData.map((pieceData, column) => formatBoardPiece(pieceData, column, rowIndex)).join('')}`;
}

function formatBoard(boardData) {
  return boardData.filter(rowData => !rowData.every(isSpace)).map((rowData, rowIndex) => formatRow(rowData, rowIndex)).join('\n');
}

function formatMove(move) {
  let kind = move[0];
  const details = move[1];
  let meta = '';
  if (kind === 'urbanize') {
    meta = `on ${details.marker.value}, moving to ${details.direction}`;
  } else if (kind === 'build_up') {
    kind = 'build';
    meta = `on top of ${details.target_tile.color} ${details.target_tile.value},
                with ${details.new_tile.color} ${details.new_tile.value}`;
  } else if (kind === 'plan') {
    if (details.target_tile.name === 'marker') {
      meta = `on ${details.target_tile.value} for ${details.wish}`;
    } else {
      meta = `on ${details.target_tile.color} ${details.target_tile.value}`;
    }
  }
  return `${kind} ${meta}`;
}

function formatMoves(moveData) {
  return Object.keys(moveData).map(player => `${player}: ${formatMove(moveData[player])}`).join('</br>');
}

function moveOptions() {
  return moveKinds.map(kind => `<option value="${kind}">${kind}</option>`);
}

function pieceOptions(pieces) {
  return pieces.map(piece => {
    const value = piece.value || piece.target.value;
    const color = piece.color || piece.target.color;
    return `<option value="${value}_${color}">${value}${color ? ` (${color})` : ''}</option>`;
  }).join('\n');
}

function formatMoveInput(playerData) {
  return `<div class="move-input">
            <div class="move-input-option">
              <span>Move</span>
              <select class="js-move-input">
                ${moveOptions()}
              </select>
            </div>
            <div class="move-input-option">
              <span>Card</span>
              <select class="js-card-input">
                ${pieceOptions(playerData.hand)}
              </select>
            </div>
            <div class="move-input-option">
              <span>Tile</span>
              <select class="js-tile-input">
                ${pieceOptions(playerData.tiles)}
              </select>
            </div>
            <button class="js-execute-button btn--green">Execute</button>
          </div>`;
}

function formatPlayer(playerData) {
  let player = `<span class="fnt--${playerData.color}">${playerData.name}</span>: 
                <span class="fnt--orange">${playerData.victory_points} VPs</span>,
                <span class="fnt--red">${playerData.resources} resources</span>
                <div class="piece-container">${playerData.tiles.map(formatTile).join('')}</div>
                <div class="piece-container">${playerData.hand.map(formatCard).join('')}</div>`;
  if (playerData.is_web) {
    player += formatMoveInput(playerData);
  }
  return player;
}

module.exports = { formatMoves, formatBoard, formatPlayer };

},{}],2:[function(require,module,exports){
const { formatMoves, formatBoard, formatPlayer } = require('./helpers/formatting');

function showBoard() {
  window.fetch('/board').then(response => {
    response.json().then(data => {
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
      wish: 'resource'
    };
  }
  if (kind === 'urbanize') {
    return {
      marker: cardValue,
      direction: 'up',
      new_tile: { value: parsedTileValue, color: tileColor }
    };
  }
  if (kind === 'build_up') {
    return {
      target_tile: { value: parsedCardValue, color: cardColor },
      new_tile: { value: parsedTileValue, color: tileColor }
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
      extra: extraForMove(kind, cardValue, cardColor, tileValue, tileColor)
    })
  });
}

function showPlayer(playerName) {
  window.fetch(`/players/${playerName}`).then(response => {
    response.json().then(data => {
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
  window.fetch('/players').then(response => {
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
  window.fetch('/play').then(response => {
    response.json().then(data => {
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

},{"./helpers/formatting":1}]},{},[2]);
