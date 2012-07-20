/* pubu */
var pinWidth = 225;
var columns = 4;
var colNamePrefix = "col";
var loading = false;
var finished = false;
var idPrefix = "#" + colNamePrefix;

/* ajax */
function do_fav(entry_id, obj) {
	$.ajax({
		type: "POST",
		url: "/item/" + entry_id + "/do_fav"
	}).done(function( msg ) {
		if (msg == "true") {
			$(obj).removeClass().addClass("Button Button13 WhiteButton disabled clickable unlike_pin");
			$(obj).html("<strong>取消喜欢</strong><span></span>");
		} 
		if (msg == "false") {
			$(obj).removeClass().addClass("Button Button13 WhiteButton like_pin");
			$(obj).html("<strong><em></em>喜欢</strong><span></span>");
		}
	});
}

function do_follow(user_id, obj) {
	$.ajax({
		type: "POST",
		url: "/user/" + user_id + "/do_follow"
	}).done(function( msg ) {
		if (msg == "true") {
			$(obj).removeClass().addClass("Button13 Button WhiteButton disabled clickable unfollowbutton InlineButton");
			$(obj).html("<strong>取消关注</strong><span></span>");
		}
		if (msg == "false") {
			$(obj).removeClass().addClass("Button13 Button WhiteButton followbutton InlineButton");
			$(obj).html("<strong>关注</strong><span></span>");
		}
	});
}

function cmtdel(id, tweetId) {
	$.ajax({
		type: "GET",
		url: "/cmtdel?id=" + id + "&tweetid=" + tweetId
	}).done(function( msg ) {
		if (msg == "ok") {
			$("#" + "item_comments_" + id).remove();
		}
	});
}

function tooltip(id) { 
	var items = $("#items_similar img");
	var index = 0;
	var pre = "";
	var next = "";
	for (var i=0; i<items.length; i++) {
		if($(items[i]).attr("id") == "item_similar_" + id) {
			index = i;
		}
		if (i > 0) {
			pre = $(items[index - 1]).parent().attr("href");
		}
		if (items.length > index) {
			next = $(items[index + 1]).parent().attr("href");
		}
	}
	$("#item-tip").mousemove(function(e) { 
		var positionX=e.pageX-$(this).offset().left;
		var positionY=e.pageY-$(this).offset().top;

		if(positionX <= $(this).width() / 2) {
			$(this).parent().attr('href', pre);
			$(this).css({cursor:"url(/static/images/item-pre.ico),auto"});
		} else {
			$(this).parent().attr('href', next); 
			$(this).css({cursor:"url(/static/images/item-next.ico),auto"});
		} 
	});
	
	$("#item-tip").mouseout(function(e) { 
	});    
}

function getMinColumn() {
	var index = 0;
	for ( var i=0; i<columns; i++ ) {
		if( $(idPrefix + i).height() < $(idPrefix + index).height() ) {
			index = i;
		}
	}
	return index;
}

function fetchEntries(userId, filter) {
	fetchEntriesBase(userId, filter, "-1", "-1");
}

function fetchCategoryEntries(category) {
	fetchEntriesBase('-1', '-1', category, "-1")
}

function searchEntries(q) {
	fetchEntriesBase("-1", "-1", "-1", q);
}


function fetchEntriesBase(userId, filter, category, q) {
	loading = true;
	$("#LoadingPins").css("display", "block");

	var p = parseInt($("#p").val());
	var offset = $("#ColumnContainer .pin").length;

	args = {"offset": offset, "p": p};
	if (userId != '-1') {
		args.user_id = parseInt(userId);
	}
	if (filter == 'likes') {
		args.filter = filter;
	}
	if (category != "-1") {
		args.category = category;
	}
	if (q != "-1") {
		args.q = q;
	}
	$.ajax({
		type: "POST",
		url: "/ajax/pubu",
		data: $.param(args)
	}).done(function(response) {
		eval("response = " + response);
		if (response["code"] == 200) {
			tweets = response["html"];
			for (var i=0; i<tweets.length; i++) {
				var index = getMinColumn();
				$(tweets[i]).appendTo($(idPrefix + index));
			}
			/* end */
			if(response["end"] == 1) {
				$("#pager").css("display", "block");
				finished = true;
			}
			/* final */
			if (response["end"] == 2) {
				finished = true;
			}
		}
		loading = false;
		$("#LoadingPins").css("display", "none");
	});
}


function fetchUsers(userId, filter) {
	loading = true;
	$("#LoadingPins").css("display", "block");

	var p = parseInt($("#p").val());
	var offset = $("#PeopleList div").length;

	args = {"offset": offset, "p": p};
	if (userId != '-1') {
		args.user_id = parseInt(userId);
	} else {
		return;
	}
	if (filter == 'followers' || filter == 'friends') {
		args.filter = filter;
	} else {
		return;
	}
	$.ajax({
		type: "POST",
		url: "/ajax/re",
		data: $.param(args)
	}).done(function(response) {
		eval("response = " + response);
		if (response["code"] == 200) {
			tweets = response["html"];
			for (var i=0; i<tweets.length; i++) {
				$(tweets[i]).appendTo($("#PeopleList"));
			}
			/* end */
			if(response["end"] == 1) {
				$("#pager").css("display", "block");
				finished = true;
			}
			/* final */
			if (response["end"] == 2) {
				finished = true;
			}
		}
		loading = false;
		$("#LoadingPins").css("display", "none");
	});
}


function loadTrigger() {
	if (($(window).height() + $(window).scrollTop()) >= $("body").height()) {
		return true;
	}
	return false;
}

function viewLoader(userId, filter) {
	if (finished || loading) return;
	var trigger = loadTrigger();
	if (trigger) {
		fetchEntries(userId, filter)
	}
}

function categoryViewLoader(category) {
	if (finished || loading) return;
	var trigger = loadTrigger();
	if (trigger) {
		fetchCategoryEntries(category);
	}
}

function searchViewLoader(q) {
	if (finished || loading) return;
	var trigger = loadTrigger();
	if (trigger) {
		searchEntries(q)
	}
}

function relationViewLoader(userId, filter) {
	if (finished || loading) return;
	var trigger = loadTrigger();
	if (trigger) {
		fetchUsers(userId, filter)
	}
}


function fetchUserTops(userId, targetDiv) {
	$.ajax({
		type: "POST",
		url: "/ajax/tops",
		data: { "user_id" : userId, "limit":8 }
	}).done(function(response) {
		eval("response = " + response);
		if (response["code"] == 200) {
			if (response["tops"].length > 0) {
				for (var i=0; i<response["tops"].length; i++) {
					var html = "<a class='ImgLink' href='/item/" + response["tops"][i]["id"] + "'>" +
						"<img src='" + response["tops"][i]["thumb"] + "'/></a>";
					$(html).appendTo($("#" + targetDiv));
				}
			}
		}
	});
}

function fetchEntryLikers(tweetId, targetDiv) {
	$.ajax({
		type: "POST",
		url: "/ajax/likers",
		data: {"entry_id": tweetId}
	}).done(function(response) {
		eval("response = " + response);
		if (response["code"] == 200) {
			if (response["likers"].length > 0) {
				for (var i=0; i<response["likers"].length; i++) {
					var liker = response["likers"][i];
					var html = "<a title='" + liker["name"] + "' class='CommenterImage tipsyHover' href='/user/" + liker["id"] + "'>" + 
						"<img src='" + liker["photo_url"] + "'/></a>";
					$(html).appendTo($("#" + targetDiv));
				}
			}
		}
	});
}


function commentIt(id) {
	var itemId = "item_" + id;
	$("#" + itemId).css("display", "block");
    $("#" + itemId + " form").live("keypress", function(e) {
        if (e.keyCode == 13) {
            newComment($(this));
            return false;
        }
    });
    $("#" + itemId + " form textarea").select();
}

function commentIt2(id) {
	$("#commentForm").live("keypress", function(e) {
		if (e.keyCode == 13) {
            newComment($(this));
            return false;
        }
	});
	$("#commentForm textarea").select();
}

function newComment(form) {
	var comment = form.formToDict();
	$.postJSON("/a/comment/new", comment, function(response) {
		showComment(response);
		if (comment.id) {
			form.find("textarea").val("");
		}
	});
}

function showComment(comment) {
	var existing = $("#c" + comment.id);
	if (existing.length > 0) return;
	var node = $(comment.html);
	node.hide();
	$("#comments" + comment.id).append(node);
	node.slideDown();
}

function getCookie(name) {
	var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
	return r ? r[1] : undefined;
}

jQuery.fn.formToDict = function() {
	var fields = this.serializeArray();
	var json = {};
	for (var i = 0; i < fields.length; i++) {
		json[fields[i].name] = fields[i].value;
	}
	if (json.next) delete json.next;
	return json;
}

jQuery.postJSON = function(url, args, callback) {
	args._xsrf = getCookie("_xsrf");
	$.ajax({
		url: url, data: $.param(args), dataType: "text", type: "POST",
		success: function(response) {
			if (callback) callback(eval("(" + response + ")"));
		}
	});
}
