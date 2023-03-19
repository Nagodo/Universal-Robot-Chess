function GetChessPosition() {
    $.ajax({
        type: "POST",
        url: "/getchessposition",
        data: {
            command: "getchessposition"
        },
    }).then(function (data) {
        console.log(data);
    });
}

$(document).ready(function () {
    const interval = setInterval(function () {
        GetChessPosition();
    }, 1000);
});