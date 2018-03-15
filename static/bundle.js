(function(){function e(t,n,r){function s(o,u){if(!n[o]){if(!t[o]){var a=typeof require=="function"&&require;if(!u&&a)return a(o,!0);if(i)return i(o,!0);var f=new Error("Cannot find module '"+o+"'");throw f.code="MODULE_NOT_FOUND",f}var l=n[o]={exports:{}};t[o][0].call(l.exports,function(e){var n=t[o][1][e];return s(n?n:e)},l,l.exports,e,t,n,r)}return n[o].exports}var i=typeof require=="function"&&require;for(var o=0;o<r.length;o++)s(r[o]);return s}return e})()({1:[function(require,module,exports){
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
  console.log(cardData.target);
  console.log(cardData.target.color);
  const textClass = cardData.target.color ? `fnt--${cardData.target.color}` : '';
  console.log(textClass);
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

function formatPlayer(playerData) {
  console.log(playerData.hand);
  return `<span class="fnt--${playerData.color}">${playerData.name}</span>: 
    <span class="fnt--orange">${playerData.victory_points} VPs</span>,
    <span class="fnt--red">${playerData.resources} resources</span>
    <div class="tile-container">${playerData.tiles.map(formatTile).join('')}</div>
    <div class="tile-container">${playerData.hand.map(formatCard).join('')}</div>`;
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

function showPlayer() {
  window.fetch('/player/Lisa').then(response => {
    response.json().then(data => {
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
  window.fetch('/play').then(response => {
    response.json().then(data => {
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
        value: 'A'
      },
      extra: {
        wish: 'resource'
      }
    })
  });
}

document.addEventListener('DOMContentLoaded', () => {
  document.querySelector('.js-play-button').addEventListener('click', play);
  update();
});

},{"./helpers/formatting":1}]},{},[2]);
