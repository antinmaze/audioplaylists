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
        return await response.json();

    } catch (error) {
        console.log(error);
    }
}

async function renderTracks(playlistid,  user){
    let data_api = await getTracks(playlistid);
    let html = '';
    console.log(data_api);        
    html += await renderTracksPagination(data_api, user);

    await data_api.tracks.forEach( track_str => {
        let track = JSON.parse(track_str);
        //console.log(track.id)
        let htmlSegment = `<a href="${track.external_urls}" target="_blank" rel="noopener noreferrer" 
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
    let container = document.querySelector("#tracks");
    container.innerHTML = html;
}   


async function renderTracksPagination(data, user){
    let htmlSegment = 
        `<ul class="pagination" id="tracks-pagination">
            <li class="page-item"><a class="page-link" 
            href="https://localhost:8000/playlist/spfy-tracks/?spotify_id=${user}&track_offset=${data.track_prvoffset}">
            Previous</a></li>
            <li class="page-item"><a class="page-link" 
            href="https://localhost:8000/playlist/spfy-tracks/?spotify_id=${user}&track_offset=${data.track_nxtoffset}">
            Next</a></li>
        </ul>`;
        return htmlSegment;
}