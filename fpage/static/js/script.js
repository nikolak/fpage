    function vote(sourceId, postId, voteDir, otherId) {
        $.post('/vote', {
            cValue: $(sourceId).text(),
            postId: postId,
            voteDir: voteDir,
            otherValue:$(otherId).text()
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
        }, function(data){
            if(data.response == "error")
                $("h6#login_response").text("Wrong username or password");
            else
                location.reload();
        });
    });
  });

    $(document).ready(function() {
      $("abbr.timeago").timeago();
    });