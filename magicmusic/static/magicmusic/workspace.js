function generateWorkspaceWav(workspaceId) {
    var workspaceWavPath = "";

    // make the ajax request
    $.ajax({
        url: "/magicmusic/generate-workspace-music/" + workspaceId,
        type: "POST",
        data: "csrfmiddlewaretoken=" + getCSRFToken(),
        dataType: "json",
        success: function (response) {
            if (!response.hasOwnProperty("error")) {
                // should clear errors

                // var newPosts = JSON.parse(response.new_posts);
                workspaceWavPath = '/' + response.file_path;
                playAudio(workspaceWavPath);


            } else {
                // error
                alert("get error info");
            }
        },
        error: function () {
            // error
            alert("failed");
        }
    });
    // console.log(trackWavPath);
    // return trackWavPath;
}

function playAudio(workspaceWavPath) {
    var cacheBustedPath = workspaceWavPath + "?cb=" + Date.now().toString();
    $('audio source').attr('src', cacheBustedPath);
    var audio = document.querySelector("audio");
    // audio.src = trackWavPath;
    // var audio = new Audio(cacheBustedPath);
    audio.load(); // !HUL|_O! PAY ATTENTI0N!
    audio.play();
}

function getCSRFToken() {
    var cookies = document.cookie.split(";");
    for (var i = 0; i < cookies.length; i++) {
        if (cookies[i].startsWith("csrftoken=")) {
            return cookies[i].substring("csrftoken=".length, cookies[i].length);
        }
    }
    return "unknown";
}