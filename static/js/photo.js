$(document).ready(function() {

    var settings = {
        file_post_name : "file",
        flash_url : $("#upload-swf-url").val(),
        upload_url: $(".form-upload").attr("action"),
        file_size_limit : "10 MB",
        file_types : "*.jpg;*.png;*.jpeg;",
        file_types_description : "Image Files",
        file_upload_limit : 100,
        file_queue_limit : 0,
        custom_settings : {
            progressTarget : "fsUploadProgress",
            cancelButtonId : "btn-cancel"
        },
        debug: false,

        button_width: "80",
        button_height: "30",
        button_placeholder_id: "spanButtonPlaceHolder",
        button_text: "<span class='upload_button'>选择图片</span>",
        button_text_style: ".upload_button { font-size: 13.5; }",
        button_text_left_padding: 12,
        button_text_top_padding: 5,

        file_queued_handler : fileQueued,
        file_queue_error_handler : fileQueueError,
        file_dialog_complete_handler : fileDialogComplete,
        upload_start_handler : uploadStart,
        upload_progress_handler : uploadProgress,
        upload_error_handler : uploadError,
        upload_success_handler : uploadSuccess,
        upload_complete_handler : uploadComplete,
        queue_complete_handler : queueComplete
    };

    var uploader = new SWFUpload(settings);

    $('#btn-cancel').click(function() {
        uploader.cancelQueue();
    });

})