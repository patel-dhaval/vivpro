const songTableBody = document.querySelector('#songTable tbody');
const prevPageBtn = document.getElementById('prevPage');
const nextPageBtn = document.getElementById('nextPage');
const pageInfo = document.getElementById('pageInfo');

let currentPage = 1;
const limit = 10;

async function fetchSongs(page) {
    const response = await fetch(`/api/v1/songs/?skip=${(page - 1) * limit}&limit=${limit}`);
    const songs = await response.json();
    return songs;
}

async function renderSongs(page) {
    const songs = await fetchSongs(page);
    songTableBody.innerHTML = '';

    songs.forEach(song => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${song.id}</td>
            <td>${song.title}</td>
            <td>${song.danceability}</td>
            <td>${song.energy}</td>
            <td>${song.tempo}</td>
            <td>${song.duration_ms}</td>
            <td class="rating">
                <input type="number" min="0" max="5" step="0.5" value="${song.star_rating}" data-id="${song.id}" onchange="enableSaveButton(this)">
            </td>
            <td>
                <button class="save-button" data-id="${song.id}" onclick="saveRating(this)" disabled>Save</button>
            </td>
        `;
        songTableBody.appendChild(row);
    });

    pageInfo.textContent = `Page ${currentPage}`;
    prevPageBtn.disabled = currentPage === 1;
    nextPageBtn.disabled = songs.length < limit;
}

function enableSaveButton(inputElement) {
    const saveButton = inputElement.closest('tr').querySelector('.save-button');
    saveButton.disabled = false;
    saveButton.style.visibility = 'visible';
}

async function saveRating(buttonElement) {
    const songId = buttonElement.getAttribute('data-id');
    const inputElement = buttonElement.closest('tr').querySelector('input[type="number"]');
    const rating = inputElement.value;

    const response = await fetch(`/api/v1/songs/${songId}/rate`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ rating: parseFloat(rating) }),
    });

    if (response.ok) {
        alert('Rating updated successfully!');
        buttonElement.disabled = true;
        buttonElement.style.visibility = 'hidden';
    } else {
        alert('Failed to update rating.');
    }
}

prevPageBtn.addEventListener('click', () => {
    if (currentPage > 1) {
        currentPage--;
        renderSongs(currentPage);
    }
});

nextPageBtn.addEventListener('click', () => {
    currentPage++;
    renderSongs(currentPage);
});


renderSongs(currentPage);
