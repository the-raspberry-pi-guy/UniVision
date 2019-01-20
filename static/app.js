const startBtn = document.querySelector('#start');

function startFaceId() {
    var request = new XMLHttpRequest;
    request.onload = function() {
        console.log("please work" + request.responseText);
    };
    request.open("POST", "http://127.0.0.1:5000/courses");
    request.send();
}

startBtn.addEventListener("click", startFaceId);
