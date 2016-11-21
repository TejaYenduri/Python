$(function() {
    $('#submit').click(function() {
        $.ajax({
            type: "GET",
            url: '/search',
            data: $('form').serialize(),
            dataType: "json",
            success: function (data) {
                for(int i=0;i<data.length;i++){
                    console.log(data[i])
                }
                

            },
            error: function(error) {
                console.log(error);
            }
        });
    });
});


