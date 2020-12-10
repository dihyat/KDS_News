$(document).ready(function (e) {
    //liking an article using ajax
    $(document).on('submit', '#like_form', function (e) {
        e.preventDefault();
        var pk = $("#like_form button").attr('value');
        $.ajax({
          type: "PUT",
          url: $("#like_form button").data("url"),
          data: {
            id: pk,
          },
          headers: { "X-CSRFToken": $("[name=csrfmiddlewaretoken]").val()},
          dataType: "json",
          success: function (response) {
            $("#like-section").html(response["form"]);
          },
          error: function (rs, e) {
            console.log(rs.responseText);
          },
        });
    })

    //deletes the profile image using ajax
    $(document).on("click", '#delete', function () {
        $.ajax({
          type: "DELETE",
          url: $(this).data("url"),
          data: { csrfmiddlewaretoken: $(this).children("input").val() },
          headers: { "X-CSRFToken": $("[name=csrfmiddlewaretoken]").val()},
          success: function (response) {
            //setting image with the default image
            $("img").attr("src", "/static/images/rename.jpg");
          },
          error: function (rs, e) {
            alert(e);
          },
        });
    })

    //show the form for reply when button is clicked
    $(document).on("click", ".reply-btn", function () {
        id = $(this).attr("id").split("-")[2]
        
        $('#reply-' + id).fadeToggle()

    })

    //show the form for edit when button is clicked
    $(document).on("click", ".edit-btn", function () {
        id = $(this).attr("id").split("-")[2]
        let comment = $(this).parent().parent().children('p').text()
        $('#edit-' + id).children('div').children('form').children('textarea').text(comment)
        $('#edit-' + id).fadeToggle()
    })

    $(document).on('submit', '.comment-form', function (e) {
        e.preventDefault();
      
        $.ajax({
            type: 'POST',
            url: $(this).attr('action'),
            data: $(this).serialize(),
            dataType: 'json',
            success: function (response) {
                //inserting html with the new comment
                $('.comment-section').html(response['form']);
                $('textarea').val('');
                $('.reply-btn').click(function () {
                    $(this).parent().parent().next('.reply-section').fadeToggle();
                    $('textarea').val('');
                })
            },
            error: function (rs, e) {
                //log error
                console.log(rs.responseText);
            }
        })
    })

    $(document).on('submit', '.reply-form', function (e) {
        e.preventDefault();
        //ajax call to reply to a comment
        $.ajax({
            type: 'POST',
            url: $(this).attr('action'),
            data: $(this).serialize(),
            dataType: 'json',
            success: function (response) {
                //inserting html with the new reply
                $('.comment-section').html(response['form']);
                $('textarea').val('');
               
            },
            error: function (rs, e) {
                //log error
                console.log(rs.responseText);
            }
        })
    })
    $(document).on('submit', '.edit-form', function (e) {
        e.preventDefault();
        //ajax call for editing a comment
        
        var comment_id = $(this).children("input").attr("id")
        var content = $(this).children("textarea").val()
        var csr = $("input[name=csrfmiddlewaretoken]").attr("value");
        var mydata = {comment_id: comment_id, content: content , csrfmiddlewaretoken: csr}
        $.ajax({
            type: 'PUT',
            url: $(this).attr('action'),
            data: mydata,
            headers : { "X-CSRFToken" : $("[name=csrfmiddlewaretoken]").val() },
            dataType: 'json',
            success: function (response) {
                //updating the comment content
                $("#content-" + id).text(response.content)
            },
            error: function (rs, e) {
                //log error
                console.log(rs.responseText);
            }
        })
    })
    $(document).on('click', '.delete-btn', function () {
        if (confirm("Are you sure you want to delete this comment")) {
            //get id
            id = $(this).parent().parent().children("p").attr('id').split('-')[1]
            //ajax request to delete comment
            $.ajax({
              type: "DELETE",
              url: $(this).data("url"),
              data: $(this).children("input"),
              headers: { "X-CSRFToken": $("[name=csrfmiddlewaretoken]").val()},
              dataType: "json",
              success: function (response) {
                $("#main-" + id).remove();
                $("#reply-" + id).remove();
                $("#edit-" + id).remove();
                //updating the number of comments
                let num_comments = $("#num-comment").text().split(" ")[0];
                num_comments = parseInt(num_comments);
                num_comments -= 1;
                if (num_comments <= 1) {
                  $("#num-comment").text(num_comments + " Comment");
                } else {
                  $("#num-comment").text(num_comments + " Comments");
                }
              },
              error: function (rs, e) {
                //log error
                console.log(rs.responseText);
              },
            });
        }
        //else do nthin
    })
})