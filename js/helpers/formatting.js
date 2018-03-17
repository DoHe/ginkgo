const moveKinds = ['plan', 'urbanize', 'build_up'];

function isSpace(pieceData) {
  return pieceData.name === 'space';
}

function gridStyle(column, row) {
  return `style="grid-column: ${column + 1}; grid-row=${row + 1};"`;
}

function formatBoardPiece(pieceData, column, row) {
  const {
    name, value, color, owner_color, resources,
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
  return boardData
    .filter(rowData => !rowData.every(isSpace))
    .map((rowData, rowIndex) => formatRow(rowData, rowIndex))
    .join('\n');
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
  return pieces.map((piece) => {
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
