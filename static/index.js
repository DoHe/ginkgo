function isSpace(piece_data) {
    return piece_data.name === 'space';
}

function gridStyle(column, row) {
    return `style="grid-column: ${column+1}; grid-row=${row+1};"`
}

function piece(piece_data, column, row) {
    let { name, value, color, owner_color, resources } = piece_data;
    if (name === 'marker') {
        return `<div class="circle bg--green" ${gridStyle(column, row)}>${value}</div>`
    } else if (name === 'tile') {
        return `<div class="rect bg--${color}" ${gridStyle(column, row)}>
                    ${value}/<span class="fnt--${owner_color}">${resources}</span>
                </div>`
    } else {
        return ""
    }
}

function row(row_data, row_index) {
    return `${row_data.map(
        (piece_data, column) => piece(piece_data, column, row_index)
    ).join('')}`
}

function showBoard() {
    window.fetch('/board').then((response) => {
        response.json().then((data) => {
            document.querySelector('.js-board').innerHTML = data.filter(
                row_data => !row_data.every(isSpace)
            ).map(
                (row_data, row_index) => row(row_data, row_index)
            ).join('\n');
        })
    })
}

function play() {
    window.fetch('/play').then((response) => {
        response.json().then((data) => {
            console.log(data);
            showBoard();
        });
    });
}

document.addEventListener('DOMContentLoaded', () => {
    document.querySelector('.js-play-button').addEventListener('click', play);
    showBoard();
});