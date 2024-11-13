jQuery(function ($) {
    'use strict';

    // EduStudyNav JS
    $.fn.classyNav && $("#EduStudyNav").classyNav({ theme: "light" }),
    $(function () {
        $('a[href="#search"]').on("click", function (o) {
            o.preventDefault(), $("#search-area").addClass("open"), $('#search-area > form > input[type="search"]').focus();
        }),
        $("#search-area, #search-area button.close").on("click keyup", function (o) {
            (o.target != this && "close" != o.target.className && 27 != o.keyCode) || $(this).removeClass("open");
        }),
        $("form").on("submit", function (e) {
            return $.preventDefault(), !1;
        });
    }),

    // home-slides js
    $(".home-slides").owlCarousel({
        items: 1,
        loop: !0,
        autoplay: !0,
        nav: !0,
        responsiveClass: !0,
        dots: !1,
        autoplayHoverPause: !0,
        mouseDrag: !0,
        navText: ["<i class='icofont-rounded-left'></i>", "<i class='icofont-rounded-right'></i>"],
    }),

    // home-slides-two js
    $(".home-slides-two").owlCarousel({
        items: 1,
        loop: !0,
        autoplay: !0,
        nav: !0,
        animateOut: "fadeOut",
        responsiveClass: !0,
        dots: !1,
        autoplayHoverPause: !0,
        mouseDrag: !0,
        navText: ["<i class='icofont-rounded-left'></i>", "<i class='icofont-rounded-right'></i>"],
    }),

    // popup-video js
    $(".popup-video").magnificPopup({ disableOn: 320, type: "iframe", mainClass: "mfp-fade", removalDelay: 160, preloader: !1, fixedContentPos: !1 }),

    // count js
    $(".count").counterUp({ delay: 20, time: 1500 }),

    // news-slider js
    $(".news-slider").owlCarousel({
        nav: !0,
        dots: !1,
        margin: 30,
        center: !1,
        touchDrag: !1,
        mouseDrag: !0,
        autoplay: !0,
        smartSpeed: 750,
        autoplayHoverPause: !0,
        loop: !0,
        navText: ["<i class='icofont-thin-left'></i>", "<i class='icofont-thin-right'></i>"],
        responsive: { 0: { items: 1 }, 768: { items: 2 }, 1200: { items: 3 } },
    }),

    // partner-slider js
    $(".partner-slider").owlCarousel({ nav: !1, dots: !1, mouseDrag: !0, margin: 30, autoplay: !0, smartSpeed: 750, autoplayHoverPause: !0, loop: !0, responsive: { 0: { items: 1 }, 768: { items: 3 }, 1200: { items: 6 } } }),

    // testimonials-slider js
    $(".testimonials-slider").owlCarousel({
        nav: !0,
        dots: !1,
        center: !0,
        margin: 30,
        touchDrag: !1,
        items: 4,
        mouseDrag: !0,
        autoplay: false,
        smartSpeed: 750,
        autoplayHoverPause: !0,
        loop: !0,
        navText: ["<i class='icofont-rounded-left'></i>", "<i class='icofont-rounded-right'></i>"],
        responsive: { 0: { items: 1 }, 768: { items: 2 } },
    }),

    // about-slider js
    $(".about-slider").owlCarousel({
        items: 1,
        loop: !0,
        autoplay: false,
        margin: 30,
        nav: !0,
        responsiveClass: !0,
        dots: !1,
        autoplayHoverPause: !0,
        mouseDrag: !0,
        navText: ["<i class='icofont-rounded-left'></i>", "<i class='icofont-rounded-right'></i>"],
    }),

    // tabs js
    $("#tabs li").on("click", function () {
        var o = $(this).attr("id");
        $(this).hasClass("inactive") &&
        ($(this).removeClass("inactive"),
        $(this).addClass("active"),
        $(this).siblings().removeClass("active").addClass("inactive"),
        $("#" + o + "_content").addClass("show"),
        $("#" + o + "_content")
        .siblings("div")
        .removeClass("show"));
    }),

    // scroll js
    $(window).on("scroll", function () {
        $(this).scrollTop() > 300 ? $(".scrolltop").fadeIn() : $(".scrolltop").fadeOut();
    }),
    $(".scrolltop").on("click", function () {
        return $("html, body").animate({ scrollTop: 0 }, 1e1), !1;
    }),
    $(".scroll-down a, .slide-inner-content a, .cta-area a").on("click", function (o) {
        var a = $(this);
        $("html, body")
        .stop()
        .animate({ scrollTop: $(a.attr("href")).offset().top - 10 }, 50),
        o.preventDefault();
    });

    // preloader-area js
    jQuery(window).on("load", function () {
        $(".preloader-area").fadeOut();
    });

}(jQuery));