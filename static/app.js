const startBtn = document.querySelector('#start');
const dataBody = document.querySelector('#data-body');
var students = {};

setInterval(function()
{
    $.ajax({
        type: "get",
        url: "http://127.0.0.1:5000/poll",
        success:function(data)
        {
            jsonData = JSON.parse(data)

            if (!(jsonData.ID in students)) {
                students[jsonData.ID] = "defaultname";
                dataBody.innerHTML += '<tr><th scope="row">' + jsonData.ID + '</th><td id="velocity" class="text-right">***</td></tr>';
            }
        }
    });
}, 1000);

function startFaceId() {
    var request = new XMLHttpRequest;
    request.onload = function() {
        console.log("please work" + request.responseText);
    };
    request.open("POST", "http://127.0.0.1:5000/courses");
    request.send();
}

startBtn.addEventListener("click", startFaceId);
