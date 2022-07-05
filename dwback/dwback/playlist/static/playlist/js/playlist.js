/*!
  * PLayList Ajax Javascript v0.0.1
  * Copyright 2022
  * Licensed under MIT
 */

/*
    Return the Tracks for a specified Playlist id
*/
async function getTracks(playlistid){
    // endpoint url
    let url =  "https://localhost:8000/playlist/spfy-tracks/?playlist_id=".concat(playlistid) 
    try {
        let response = await fetch(url);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`); // handle errors
        }
        return await response.json(); // response

    } catch (error) {
        console.log(error);
    }
}

async function renderTracks(playlistid){
    let tracks = await getTracks(playlistid);
    window.alert(tracks);
    let html = '';
    tracks.forEach(track => {
        let htmlSegment = `<a href="https://localhost:8000/playlist/spfy-tracks/?track_id=${track.id}" 
                            class="list-group-item list-group-item-action">
                            <div class="row" >
                                <div class="col-sm-4">
                                    <img class="img-thumbnail" src="${track.image_url}" alt="${track.name}">
                                </div>  
                                <div class="col-sm-8">
                                    <h6>${track.name}</h6>
                                    <p>ISCR:${track.external_id}</p>
                                </div>
                            </div>
                        </a>`;
        html += htmlSegment;
    });

    let container = document.querySelector('#tracks');
    container.innerHTML = html;
}   