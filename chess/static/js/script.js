function GetChessPosition() {
    $.ajax({
        type: "POST",
        url: "/getchessposition",
        data: {
            command: "getchessposition"
        },
    }).then(function (data) {
        document.getElementById("content").innerHTML = data;
    });
}

$(document).ready(function () {
    const interval = setInterval(function () {
        GetChessPosition();
    }, 1000);
});