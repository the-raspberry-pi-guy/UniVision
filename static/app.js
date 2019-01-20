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
            jsonData = JSON.parse(data);
            console.log(jsonData);

            if (!(jsonData.id in students)) {
                students[jsonData.id] = "defaultname";

                if (jsonData.id === "s0000000") {
                    document.querySelector('#matt').innerHTML = '<th id="matt" scope="row">✅ Matt Timmons-Brown (s0000000)</th>';
                }
                else if (jsonData.id === "s1111111") {
                    document.querySelector('#neil').innerHTML = '<th id="neil" scope="row">✅ Neil Weidinger (s1111111)</th>';
                }
                else if (jsonData.id === "s2222222") {
                    document.querySelector('#rafa').innerHTML = '<th id="rafa" scope="row">✅ Rafael Anderka (s2222222)</th>';
                }

                // dataBody.innerHTML += '<tr><th scope="row">' + jsonData.name + ' (' + jsonData.id + ') ' + '</th><td id="student-data" class="text-right">' + jsonData.degree + '</td></tr>';
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
