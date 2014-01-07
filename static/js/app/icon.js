$(document).ready(function() {
    $('#target').Jcrop({
        onSelect: showPreview,
        onChange: showPreview,
        aspectRatio: 1
    });

    function showPreview(coords) {
        var height = $("#target").height();
        var width = $("#target").width();

        var rx = 100 / coords.w;
        var ry = 100 / coords.h;
        $('#coords').val([coords.x, coords.y, coords.w, coords.h].join(' '));
        $('#preview').css({
            width: Math.round(rx * width) + 'px',
            height: Math.round(ry * height) + 'px',
            marginLeft: '-' + Math.round(rx * coords.x) + 'px',
            marginTop: '-' + Math.round(ry * coords.y) + 'px'
        });
    }
});