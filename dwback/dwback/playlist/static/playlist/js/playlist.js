/*!
  * PLayList Ajax Javascript v0.0.1
  * Copyright 2022
  * Licensed under MIT
 */

/*
    Return the Tracks for a specified Playlist id
*/
async function getTracks(playlistid){
    const response = await fetch(
        // endpoint url
        "https://localhost:8000/playlist/spfy-tracks/?playlist_id=".concat(playlistid)  
    );
    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`); // handle errors
    }
    const data = await response.json(); // response
    return await data.json();
}

async function renderTracks(playlistid){
    let tracks = await getTracks(playlistid);
    let html = '';
    tracks.forEach(track => {
        let htmlSegment = `<div class="track">
                            <img src="${user.profileURL}" >
                            <h2>${user.firstName} ${user.lastName}</h2>
                            <div class="email"><a href="email:${user.email}">${user.email}</a></div>
                        </div>`;

        html += htmlSegment;
    });

    let container = document.querySelector('.container');
    container.innerHTML = html;
}   