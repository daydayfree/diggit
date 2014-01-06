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
    if (finished || loading) return;
    var trigger = loadTrigger();
    if (trigger) {
        loader(userId, filter);
    }
}


var loader = function(){
    loading = true;
    $("#LoadingPins").fadeIn();

    var page = parseInt($(".current_page").val());
    var start = $("#ColumnContainer .pin").length;

    $.post("/j/photos/", {page:page, start:start}, function(r) {
        if (r.code === 200) {
            for (var i=0; i<r.photos.length; i++) {
                var index = getMinColumn();
                $(r.photos[i]).appendTo($(idPrefix + index));
            }
            if (r.end === true) {
                $("#pager").css("display", "block");
                 finished = true;
            }
        }
    });

    loading = false;
    $("#LoadingPins").css("display", "none");
}
