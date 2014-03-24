$(document).ready(function() {

    // Sign in navbar click

    $(document).on('click', 'a#sign_in', function() {
        $.post('/login/', {
            username: $("input#username").val(),
            password: $("input#password").val()
        }, function(data) {
            if (data.response == "error")
                $("h6#login_response").text("Wrong username or password");
            else
                location.reload();
        });
    });

    // Timeago library to display comment/post age
    $("abbr.timeago").timeago();

    // Show comment reply object/box
    $(document).on('click', 'a#show_reply', function() {
        reply_id = $(this).parent().attr('id');
        document.getElementById("reply_" + reply_id).style.removeProperty("display")
    });

    // Hide comment reply object/box
    $(document).on('click', 'a#hide_reply', function() {
        reply_id = $(this).closest('div.container').attr('id');
        var obj = document.getElementById(reply_id).style.display = "none";
    });

    // Upvote button click
    $(document).on('click', 'a#upvote', function() {
        var dir_id_type = $(this).parent().attr('id').split('_');
        var upvotes = $(this);
        var downvotes = $(this).parent().parent().find("a#downvote");
        var c_ups = parseInt(upvotes.text());
        var c_downs = parseInt(downvotes.text());
        $.post('/vote', {
            direction: dir_id_type[1],
            object_id: dir_id_type[0],
            vote_type: dir_id_type[2]
        }).done(function(response) {
            vote_response(response, c_ups, c_downs, upvotes, downvotes);
        });
    });

    // Downvote button click
    $(document).on('click', 'a#downvote', function() {
        var dir_id_type = $(this).parent().attr('id').split('_');
        var downvotes = $(this);
        var upvotes = $(this).parent().parent().find("a#upvote");
        var c_ups = parseInt(upvotes.text());
        var c_downs = parseInt(downvotes.text());

        $.post('/vote', {
            direction: dir_id_type[1],
            object_id: dir_id_type[0],
            vote_type: dir_id_type[2]
        }).done(function(response) {
            vote_response(response, c_ups, c_downs, upvotes, downvotes);
        });
    });

    // Function to update data in case of upvote/downvote

    function vote_response(response, c_ups, c_downs, upvotes, downvotes) {
        if (response.data == "upvoted") {
            upvotes.text(' ' + (c_ups + 1));
        } else if (response.data == "downvoted") {
            downvotes.text(' ' + (c_downs + 1));
        } else if (response.data == "up_cancel") {
            upvotes.text(' ' + (c_ups - 1));
        } else if (response.data == "down_cancel") {
            downvotes.text(' ' + (c_downs - 1));
        } else if (response.data == "down_to_up") {
            downvotes.text(' ' + (c_downs - 1));
            upvotes.text(' ' + (c_ups + 1));
        } else if (response.data == "up_to_down") {
            upvotes.text(' ' + (c_ups - 1));
            downvotes.text(' ' + (c_downs + 1));
        }
    };

    // Update counter to reflect number of characters left for the comment
    $(document).on('keyup', 'textarea.form-control', function() {
        var max = 5000;
        var len = $(this).val().length;
        var char_counter = $(this).parent().find('h6#char_counter')
        if (len >= max) {
            char_counter.text(' you have reached the limit');
        } else {
            var char = max - len;
            char_counter.text(char + ' characters left');
        }
    });

    // Submit comment button function
    $(document).on('click', 'a#submit_comment', function() {
        var c_object = $(this).parent().find('textarea.form-control');
        var status = $(this).parent().find('h6#char_counter')
        $.post('/comment/post', {
            thread_id: c_object.attr('id').split('_')[1],
            parent_id: c_object.attr('id').split('_')[2],
            content: c_object.val(),
        }).done(function(data) {
            status.text(data.response)
        });
    });

});
