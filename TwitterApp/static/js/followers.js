$(function() {
    $('#submit').click(function() {
        $.ajax({
            type: "GET",
            url: '/followers',
            data: $('form').serialize(),
            dataType: "json",
            success: function (data) {
                ul = $("<ul>");                    // create a new ul element
                    // iterate over the array and build the list
                    for (var i = 0, l = data.length; i < l; ++i) {
                        ul.append("<li>"+data[i]+ "</li>");
            }
            $("#followers").append(ul);
            },

            error: function(error) {
                console.log(error);
            }
        });
    });
});

