document.getElementById('searchButton').addEventListener('click', async function() {
    console.log("Check trigger!");
    const title = document.getElementById('songTitle').value.trim();
    const songDetailsDiv = document.getElementById('songDetails');

    if (!title) {
        songDetailsDiv.innerHTML = '<p class="error">Please enter a song title.</p>';
        return;
    }

    songDetailsDiv.innerHTML = '';

    try {
        const response = await fetch(`/api/v1/songs/${(title)}`);
        if (response.ok) {
            const song = await response.json();
            songDetailsDiv.innerHTML = `
                <h3>Song Details:</h3>
                <p><strong>Title:</strong> ${song.title}</p>
                <p><strong>Danceability:</strong> ${song.danceability}</p>
                <p><strong>Energy:</strong> ${song.energy}</p>
                <p><strong>Tempo:</strong> ${song.tempo}</p>
                <p><strong>Duration (ms):</strong> ${song.duration_ms}</p>
                <p><strong>Rating:</strong> ${song.star_rating}</p>
            `;
        } else {
            songDetailsDiv.innerHTML = '<p class="error">Song not found. Please try a different title.</p>';
        }
    } catch (error) {
        songDetailsDiv.innerHTML = '<p class="error">An error occurred while searching for the song.</p>';
    }
});
