
function do_fav(entry_id, obj) {
  alert(obj)
  $.post("/j/do_fav",{photo_id:entry_id}, function(r) {
    if (r.code === 200) {
      $(obj).removeClass().addClass("Button Button11 WhiteButton disabled clickable unlike_pin");
      $(obj).html("<strong>Unlike</strong><span></span>");i
    }
  });
}

