(function ($) {
    "use strict"
    $(document).ready(function () {

        // Mobile Menu
        $('#mobile-menu').meanmenu({
            meanMenuContainer: '.mobile-menu',
            meanScreenWidth: "991.99",
            onePage: false
        });

        // Video Play Button
        $('.video-play-button a').magnificPopup({
            type: 'iframe'
        });

        // MouseHover Animation
        var hoverLayer = $(".hero-area");
        var heroImgOne = $(".hero-shape.shape-01");
        var heroImgTwo = $(".hero-shape.shape-02");
        var heroImgThree = $(".hero-shape.shape-03");
        hoverLayer.mousemove(function (e) {
            var valueX = (e.pageX * -1) / 100;
            var valueY = (e.pageY * -1) / 120;
            heroImgOne.css({
                transform: "translate3d(" + valueX + "px," + valueY + "px, 0)"
            });
        });
        hoverLayer.mousemove(function (e) {
            var valueX = (e.pageX * -1) / 80;
            var valueY = (e.pageY * -1) / 100;
            heroImgTwo.css({
                transform: "translate3d(" + valueX + "px," + valueY + "px, 0)"
            });
        });
        hoverLayer.mousemove(function (e) {
            var valueX = (e.pageX * -1) / 60;
            var valueY = (e.pageY * -1) / 80;
            heroImgThree.css({
                transform: "translate3d(" + valueX + "px," + valueY + "px, 0)"
            });
        });

        // CounterUp 
        $('.counter').counterUp({
            delay: 10,
            time: 1500
        });

        // Feedback Slider
        $('.feedback-slider').slick({
            dots: false,
            infinite: true,
            speed: 1000,
            autoplay: true,
            autoplaySpeed: 2000,
            slidesToShow: 2,
            slidesToScroll: 1,
            arrows: false,
            responsive: [{
                breakpoint: 1200,
                settings: {
                    slidesToShow: 2,
                    slidesToScroll: 1,
                    arrows: false,
                }
            },
            {
                breakpoint: 992,
                settings: {
                    slidesToShow: 1,
                    slidesToScroll: 1,
                    arrows: false,
                }
            }, {
                breakpoint: 768,
                settings: {
                    slidesToShow: 1,
                    slidesToScroll: 1,
                    arrows: false,
                }
            },
            ]
        });

        // Blog Slider
        $('.blog-slider').slick({
            dots: false,
            infinite: true,
            speed: 1000,
            autoplay: true,
            autoplaySpeed: 2000,
            slidesToShow: 3,
            slidesToScroll: 1,
            arrows: false,
            responsive: [{
                breakpoint: 1200,
                settings: {
                    slidesToShow: 2,
                    slidesToScroll: 1,
                    arrows: false,
                }
            },
            {
                breakpoint: 992,
                settings: {
                    slidesToShow: 2,
                    slidesToScroll: 1,
                    arrows: false,
                }
            }, {
                breakpoint: 768,
                settings: {
                    slidesToShow: 1,
                    slidesToScroll: 1,
                    arrows: false,
                }
            },
            ]
        });

        // Category Slider
        $('.category-slider').slick({
            dots: false,
            infinite: true,
            speed: 1000,
            autoplay: true,
            autoplaySpeed: 2000,
            slidesToShow: 4,
            slidesToScroll: 1,
            arrows: true,
            prevArrow: '<i class="prev-arrow fa fa-long-arrow-left"></i>',
            nextArrow: '<i class="next-arrow fa fa-long-arrow-right"></i>',
            responsive: [{
                breakpoint: 1200,
                settings: {
                    slidesToShow: 3,
                    slidesToScroll: 1,
                    arrows: false,
                }
            },
            {
                breakpoint: 992,
                settings: {
                    slidesToShow: 2,
                    slidesToScroll: 1,
                    arrows: false,
                }
            }, {
                breakpoint: 768,
                settings: {
                    slidesToShow: 1,
                    slidesToScroll: 1,
                    arrows: false,
                }
            },
            ]
        });

        // Course Details Tab
        $(".tab-accordion ul li").on('click', function () {
            var tabClass = $(this).attr("class");
            $(this).addClass("active").siblings().removeClass("active");
            $("." + tabClass + "-content").addClass("active").siblings().removeClass("active");
        });


    });

    $(window).on('scroll', function () {

        // Back Top
        var ScrollTop = $('.back-to-top');

        if ($(window).scrollTop() > 1000) {
            ScrollTop.fadeIn(1000);
        } else {
            ScrollTop.fadeOut(1000);
        }

    });

    $(window).on('load', function () {

        // WOW JS
        new WOW().init();

        // Preloader
        var preLoder = $("#preloader");
        preLoder.fadeOut(0);

        // Back Top
        $(".back-to-top").on('click', function () {
            $("html").animate({
                "scrollTop": "0"
            }, 1000);
        });

    });
})(jQuery);

document.querySelector(".fullname").textContent = " " + localStorage.getItem("name")
console.log(localStorage.getItem("name"))

if(localStorage.is_authenticated == "true") {
    document.querySelector(".login").textContent = "logout"
}
else{
    document.querySelector(".login").textContent = "login"
}

const login = document.querySelector(".login")
login.addEventListener("click",function(){
    if(this.textContent == "logout"){
        localStorage.removeItem("token")
        localStorage.setItem("is_authenticated", "false")
        localStorage.setItem("name","")
        window.location.href = "/login.html"
    }
})