document.getElementById('searchButton').addEventListener('click', async () => {
    const title = document.getElementById('songTitle').value;
    const danceability = document.getElementById('danceability').value;
    const energy = document.getElementById('energy').value;
    const tempo = document.getElementById('tempo').value;

    const params = new URLSearchParams();
    if (title) params.append('title', title);
    if (danceability) params.append('danceability', danceability);
    if (energy) params.append('energy', energy);
    if (tempo) params.append('tempo', tempo);

    const response = await fetch(`/api/v1/songs/search?${params.toString()}`);
    const result = await response.json();

    displaySongDetails(result);
});

function displaySongDetails(songData) {
    const songDetailsDiv = document.getElementById('songDetails');
    songDetailsDiv.innerHTML = '';
    
    if (songData.length === 0) {
        songDetailsDiv.innerHTML = '<p>No songs found.</p>';
        return;
    }

    const table = document.createElement('table');
    table.innerHTML = `
        <thead>
            <tr>
                <th>Title</th>
                <th>Danceability</th>
                <th>Energy</th>
                <th>Tempo</th>
                <th>Duration (ms)</th>
            </tr>
        </thead>
    `;

    const tbody = document.createElement('tbody');
    songData.forEach(song => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${song.title}</td>
            <td>${song.danceability}</td>
            <td>${song.energy}</td>
            <td>${song.tempo}</td>
            <td>${song.duration_ms}</td>
        `;
        tbody.appendChild(row);
    });

    table.appendChild(tbody);
    songDetailsDiv.appendChild(table);
}
