/*!
  * PLayList Ajax Javascript v0.0.1
  * Copyright 2022
  * Licensed under MIT
 */

/*
    Return the TRacks for a specified playlist id
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

