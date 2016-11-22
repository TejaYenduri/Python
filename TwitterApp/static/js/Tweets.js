$(function() {
    $('#submit').click(function() {
        $.ajax({
            type: "GET",
            url: '/get_tweets',
            data: $('form').serialize(),
            dataType: "json",
            success: function (data) {
                ul = $("<ul>");                    // create a new ul element
                    // iterate over the array and build the list
                    for (var i = 0, l = data.result.length; i < l; ++i) {
                        ul.append("<li>"+data.result[i]+ "</li>");
            }
            $("#tweets").append(ul);
            },

            error: function(error) {
                console.log(error);
            }
        });
    });
});

