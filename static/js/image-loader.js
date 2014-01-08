var pinWidth = 225;
var columns = 4;
var colNamePrefix = "col";
var loading = false;
var finished = false;
var idPrefix = "#" + colNamePrefix;

$(document).ready(function() {
    loader();
    $(window).scroll(function() {
        start_loader()
    });
});

var loadTrigger = function() {
    if (($(window).height() + $(window).scrollTop()) >= $("body").height()) {
        return true;
    }
    return false;
}

var start_loader = function() {
    if (finished || loading) {
        return;
    }
    var trigger = loadTrigger();
    if (trigger) {
        loader();
    }
}


var loader = function(){
    var page = parseInt($(".pagination.page").val());
    var start = $("#ColumnContainer .pin").length;

    loading = true;
    $("#LoadingPins").fadeIn();

    $.post("/j/photos/", {page:page, start:start}, function(r) {
        if (r.code === 200) {
            for (var i=0; i<r.photos.length; i++) {
                var index = getMinColumn();
                $(r.photos[i]).appendTo($(idPrefix + index));
            }
            $("abbr.timeago").timeago();
        } else {
            finished = true;
            $("#pager").fadeIn();
        }
        loading = false;
        $("#LoadingPins").fadeOut();
    });
}
