
$(".diggit").click(function () {
    var username = "{{ request.user.username }}";
    if (username) {
        // 点赞或踩灭
        var is_up = True;
        var article_id = $(this).article_id.val();

        $.ajax({
            url: "/blog/up_down/{{ article_id }}",
            type: "get",
            success: function (data) {
                if (data.status) {
                    // 赞成功
                    var diggit = ($('#digg_count').text()) + 1;
                    $('#digg_count').text(diggVal)


                } else {
                    // 重复操作 失败
                    console.log(data.first_operate);
                    if (data.first_operate) {
                        $('#digg_word').html('您已经推荐过').css({
                            "color": "red",
                            "margin-right": "26px",
                            'margin-top': "10px"
                        })
                    } else {
                        $('#digg_word').html('您已经反对过').css({
                            "color": "red",
                            "margin-right": "26px",
                            'margin-top': "10px"
                        })
                    }
                }
            }
        });
    } else {
        location.href = '/login/'
    }
});