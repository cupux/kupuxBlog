$(document).ready(function(){
    
    /* this code is for owl carousel */
    $(".index_one .hero_area_list, .index_two .hero_area_list, .index_five .hero_area_list, .index_six .hero_area_list").owlCarousel({
        items: 1,
        margin: 0,
        autoplay: true,
        nav: true,
        navText: ["<i class='fa fa-angle-left'></i>" , "<i class='fa fa-angle-right'></i>"],
        dots: false,
        loop: true,
    });
    $(".index_three .hero_area_list").owlCarousel({
        margin: 0,
        autoplay: true,
        nav: true,
        navText: ["<i class='fa fa-angle-left'></i>" , "<i class='fa fa-angle-right'></i>"],
        dots: false,
        loop: true,
        responsive : {
            0 : {
                items: 1,
            },
            480 : {
                items: 1,
            },
            768: {
                items: 2,
            },
            992: {
                items: 3,
            }
        },
    });
    $(".index_four .hero_area_list").owlCarousel({
        margin: 0,
        autoplay: true,
        nav: false,
        navText: ["<i class='fa fa-angle-left'></i>" , "<i class='fa fa-angle-right'></i>"],
        dots: false,
        loop: true,
        responsive : {
            0 : {
                items: 1,
            },
            480 : {
                items: 1,
            },
            768: {
                items: 1,
            },
            992: {
                items: 3,
            }
        }
    });
    
    
    //this code is for scroll to top
    $(".scroll_top").click(function(){
        $("html,body").animate({scrollTop:0},2000);
    });
    
    
    //this code is for preloader
    $("body").addClass("preloader_active");
    
    
    // this code is for venobox
    $(".vide_area_venobox").venobox({
        titleattr: 'data-title',
    });
    
    
    // this code is for instafeed jquery
    var userFeed = new Instafeed({
        limit: 6,
        get: 'tagged',
        tagName: 'food',
        accessToken: '1189321718.467ede5.59564e795f3d4cedbd2d5c5a33b03ca1',
        template: '<a target="_blank" href="{{link}}"><img src="{{image}}" /></a>',
    });
    userFeed.run(); 
    
    
    /* this code is for bootstrap Tultip */
    $('[data-toggle="tooltip"]').tooltip()
    
    
});

$(window).load(function() {
// makes sure the whole site is loaded
    $('#preloader').fadeOut(); // will first fade out the loading animation
    $('.preloader_spinner').delay(350).fadeOut('slow'); // will fade out the white DIV that covers the website.
    $("body").removeClass("preloader_active");
})