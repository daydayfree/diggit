
function like(photo_id, obj) {
  $.post("/j/like/", {photo_id:photo_id}, function(r) {
    if (r.code === 200) {
      $(obj).removeClass().addClass("Button Button11 WhiteButton disabled clickable unlike_pin");
      $(obj).html("<strong>Unlike</strong><span></span>");
    }
  });
}

