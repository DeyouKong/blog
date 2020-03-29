/*
* @Author: Sampson
* @Date:   2020-02-04 10:39:20
* @Last Modified by:   Sampson
* @Last Modified time: 2020-02-04 10:39:20
*/

$(function () {
    setTimeout(function () {
        $(".section1").addClass("comein");
    }, 200);


    $("#fullpage").fullpage({
        navigation: true,	//是否显示导航，默认为false
        navigationPosition: "right",	//导航小圆点的位置
        // navigationTooltips: ['firstSlide', 'secondSlide'],	//导航小圆点的提示

        loopBottom: true,	//滚动到最低部后是否连续滚动到顶部，默认为false
        // loopTop: true,	//滚动到最顶部后是否连续滚动到底部，默认为false
        loopHorizontal: true,	//横向slide幻灯片是否循环滚动，默认为true

        //	回调函数
        // afterLoad: function (anchorLink, index) {
        //
        // },

        // 刚开始滚动的时候就出发的回调函数 onLeave
        // 滚动前的回调函数，接收 index、nextIndex 和 direction 3个参数
        // index 是离开的“页面”的序号，从1开始计算；
        // nextIndex 是滚动到的“页面”的序号，从1开始计算；
        // direction 判断往上滚动还是往下滚动，值是 up 或 down。
        onLeave: function (index, nextIndex, direction) {
            // 如果下一屏是第二屏，则逆时针旋转60度
            console.log(111);
            if (index ===1 && nextIndex === 2) {
                console.log(111);
                $("#bg").addClass("rotate");
            }else {
                $("#bg").removeClass("rotate");
            }

            // 当进入第二屏幕的时候, p2 变大
            if (nextIndex === 2){
                // 我们的jquery 里面的 animate 是比支持  transform 等
                // jquery 里面通过 myLoveCss 和 transition 搭配也能基本实现类似 animate 动画效果
                $(".p2").css("transform", "translateX(-50%) translateY(-50%) translateZ(0) scale(1)");
            }else {
                $(".p2").css("transform", "translateX(-50%) translateY(-50%) translateZ(2000px) scale(1)");

            }
            // 当进入第三屏幕的时候, 盒子进入屏幕
            if (nextIndex === 3){
                $(".p3").css("transform","translateZ(-50px) rotateX(30deg)");
                $(".title3").css("transform","translateZ(0) rotateX(0deg)");
            }

            // 进入第四屏
            if (nextIndex === 4){
                $(".p3").css("transform","translateZ(-200px) translateX(3000px) rotateY(-45deg)");
                $(".title3").css("transform","translateZ(1200px) rotateY(-60deg)");
            }
        }

    });
});
