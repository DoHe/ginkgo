function piece(piece_data) {
    console.log(piece_data);
    let { name, value, color, owner_color, resources } = piece_data;
    if (name === 'space') {
        return '<span>&nbsp;&nbsp;&nbsp;</span>'
    } else if (name === 'marker') {
        return `<span class="fnt--green">&nbsp;${value}&nbsp;</span>`
    } else {
        if (color === 'yellow') {
            color = 'orange';
        }
        return `<span class="fnt--${color}">${value}</span>/<span class="fnt--mid-gray">${resources}</span>`
    }
}

function row(row_data) {
    console.log(`row: ${row_data}`)
    return `<p>${row_data.map(piece).join('&nbsp;&nbsp;')}</p>`
}

function showBoard() {
    window.fetch('/board').then((response) => {
        response.json().then((data) => {
            document.querySelector('.js-board').innerHTML = data.map(row).join('\n');
        })
    })
}

document.addEventListener('DOMContentLoaded', () => {
    showBoard();
});