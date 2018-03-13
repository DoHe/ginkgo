function isSpace(piece_data) {
  return piece_data.name === 'space';
}

function gridStyle(column, row) {
  return `style="grid-column: ${column + 1}; grid-row=${row + 1};"`;
}

function formatPiece(piece_data, column, row) {
  const {
    name, value, color, owner_color, resources,
  } = piece_data;
  if (name === 'marker') {
    return `<div class="circle bg--green" ${gridStyle(column, row)}>${value}</div>`;
  } else if (name === 'tile') {
    return `<div class="rect bg--${color}" ${gridStyle(column, row)}>
                    ${value}/<span class="fnt--${owner_color}">${resources}</span>
                </div>`;
  }
  return '';
}

function formatRow(row_data, row_index) {
  return `${row_data.map((piece_data, column) => formatPiece(piece_data, column, row_index)).join('')}`;
}

function showBoard() {
  window.fetch('/board').then((response) => {
    response.json().then((data) => {
      document.querySelector('.js-board').innerHTML = data
        .filter(row_data => !row_data.every(isSpace))
        .map((row_data, row_index) => formatRow(row_data, row_index))
        .join('\n');
    });
  });
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

function play() {
  window.fetch('/play').then((response) => {
    response.json().then((data) => {
      const moves = Object.keys(data).map(player => `${player}: ${formatMove(data[player])}`).join('</br>');
      const gameLog = document.querySelector('.js-game-log');
      gameLog.innerHTML = `${moves} </br></br> ${gameLog.innerHTML}`;
      showBoard();
    });
  });
}

document.addEventListener('DOMContentLoaded', () => {
  document.querySelector('.js-play-button').addEventListener('click', play);
  showBoard();
});
