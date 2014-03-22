    function vote(sourceId, postId, voteDir, otherId) {
        $.post('/vote', {
            cValue: $(sourceId).text(),
            postId: postId,
            voteDir: voteDir,
            otherValue: $(otherId).text()
        }).done(function(voted) {
            $(sourceId).text(voted['new_value'])
            $(otherId).text(voted['other_value'])
        });
    };

    $(function() {
        $('a#sign_in').bind('click', function() {
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
    });

    $(document).ready(function() {
        $("abbr.timeago").timeago();
    });

    function comment(comment_id, thread_id) {
        $.post('/comment/post', {
            parent_id: comment_id,
            content: $("textarea#" + comment_id + "_content").val(),
            thread_id: thread_id
        }).done(function(data) {
            $("h6#status_" + comment_id).text(data.response)
        });
    };

    $(document).ready(function() {
        $(document).on('click', 'a#show_reply', function() {
            reply_id = $(this).parent().attr('id');
            document.getElementById("reply_" + reply_id).removeAttribute("style")
        });
    });

    $(document).ready(function() {
        $(document).on('click', 'a#hide_reply', function() {
            reply_id = $(this).closest('div.container').attr('id');
            document.getElementById(reply_id).style.display = "none";
        });
    });

    $(document).ready(function() {
        $(document).on('click', 'a#upvote', function() {
            var dir_id = $(this).parent().attr('id').split('_');
            var upvotes = $(this);
            var downvotes = $(this).parent().parent().find("a#downvote");
            var c_ups = parseInt(upvotes.text());
            var c_downs = parseInt(downvotes.text());
            $.post('/vote', {
                direction: dir_id[1],
                submission: dir_id[0],
            }).done(function(response) {
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
                } else {
                    alert(response.data);
                }
            });
        })
    });

    $(document).ready(function() {
        $(document).on('click', 'a#downvote', function() {
            var dir_id = $(this).parent().attr('id').split('_');
            var downvotes = $(this);
            var upvotes = $(this).parent().parent().find("a#upvote");
            var c_ups = parseInt(upvotes.text());
            var c_downs = parseInt(downvotes.text());

            $.post('/vote', {
                direction: dir_id[1],
                submission: dir_id[0],
            }).done(function(response) {
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
                } else {
                    alert(response.data);
                }

            });
        })
    });
