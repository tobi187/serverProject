"use strict"

function onPlus() {
    var listLen = $("#fileList li").length;
    $("#fileList").append('<li><input type="file" name="file' + listLen + '"></li>');
}

