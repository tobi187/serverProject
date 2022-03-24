"use strict"

function onPlus() {
    var listLen = $("#fileList li").length;
    $("#fileList").append('<li><input type="file" name="file' + listLen + '"></li>');
}


$(
    function() {
        if ($("#downloading").length) {
            var link = $("#linkstorage").data("link")
            // console.log("extra sc: " + link)
            updateProgress(link)
        }
    }
)



function updateProgress(status_url) {
    $.getJSON(status_url, function(data) {
        $('#status').text(data["status"])
        $('#amDone').text(data["current"])
        $('#amGes').text(data["total"])

        if (data['state'] != 'PENDING' && data['state'] != 'WORKING') {
            if ("result" in data) {
                $.ajax({
                    type: "POST",
                    url: "/dl_test" ,
                    //contentType: 'application/json;charset=UTF-8',
                    data : {'file_name': data["result"]},
                    success: function() {
                        alert("nice")
                        //window.location.href = "/overview/combine"
                    },
                    error: function() {
                        alert("error")
                    }
                })
            } else {
                console.log("Problem: " + data["state"])
            }
        } else {
            setTimeout(function () {
                updateProgress(status_url)
            }, 5000)
        }
    })
}