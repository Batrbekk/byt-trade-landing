



(function ($) {
    'use strict';

    var hami_window = $(window);

    // ****************************
    // :: 1.0 Preloader Active Code
    // ****************************

    hami_window.on('load', function () {
        $('#preloader').fadeOut('1000', function () {
            $(this).remove();
        });
    });

    // ****************************
    // :: 2.0 ClassyNav Active Code
    // ****************************
   
    if ($.fn.classyNav) {
        $('#hamiNav').classyNav();
    }
    
    // *********************************
    // :: 3.0 Welcome Slides Active Code
    // *********************************

    if ($.fn.owlCarousel) {
        var welcomeSlider = $('.welcome-slides');
        welcomeSlider.owlCarousel({
            items: 1,
            loop: false,
            autoplay: false,
            smartSpeed: 1500,
            autoplayTimeout: 7000
        })
        welcomeSlider.on('translate.owl.carousel', function () {
            var layer = $("[data-animation]");
            layer.each(function () {
                var anim_name = $(this).data('animation');
                $(this).removeClass('animated ' + anim_name).css('opacity', '0');
            });
        });

        $("[data-delay]").each(function () {
            var anim_del = $(this).data('delay');
            $(this).css('animation-delay', anim_del);
        });

        $("[data-duration]").each(function () {
            var anim_dur = $(this).data('duration');
            $(this).css('animation-duration', anim_dur);
        });

        welcomeSlider.on('translated.owl.carousel', function () {
            var layer = welcomeSlider.find('.owl-item.active').find("[data-animation]");
            layer.each(function () {
                var anim_name = $(this).data('animation');
                $(this).addClass('animated ' + anim_name).css('opacity', '1');
            });
        });
    }
    
    
    // *************************************
    // :: 4.0 Testimonial Slides Active Code
    // *************************************
    if ($.fn.owlCarousel) {
        var testiSlide = $('.testimonial-slide');
        testiSlide.owlCarousel({
            items: 4,
            margin: 50,
            loop: true,
            autoplay: false,
            mouseDrag: true,
            touchDrag: true,
            pullDrag: true,
            smartSpeed: 1500,
            dots: true,
            responsive: {
                0: {
                    items: 1
                },
                768: {
                    items: 2
                },
                992: {
                    items: 3
                },
                1200: {
                    items: 4
                }
            },
            onInitialized: function () {
                var slides = $(".single-testimonial-area .single-testimonial-area .testimonial-content");
                var windowWidth = $(window).width();
                var slideWidth = windowWidth * 2; // задаем ширину слайда
                var slideHeight = slideWidth * 0.5; // задаем высоту слайда
                slides.css({
                    "width": slideWidth + "px",
                    "height": slideHeight + "px"
                });
            }
        });
    }
    
   



    // *********************************
    // :: 5.0 Portfolio Menu Active Code
    // *********************************
    $('.portfolio-menu button.btn').on('click', function () {
        $('.portfolio-menu button.btn').removeClass('active');
        $(this).addClass('active');
    })

    // *********************************
    // :: 6.0 Magnific Popup Active Code
    // *********************************
    if ($.fn.magnificPopup) {
        $('.video-play-btn').magnificPopup({
            type: 'iframe'
        });
    }

    // **************************
    // :: 7.0 Tooltip Active Code
    // **************************
    if ($.fn.tooltip) {
        $('[data-toggle="tooltip"]').tooltip();
    }

    // ***********************
    // :: 8.0 WOW Active Code
    // ***********************
    if (hami_window.width() > 767) {
        new WOW().init();
    }

    // ****************************
    // :: 9.0 Jarallax Active Code
    // ****************************
    if ($.fn.jarallax) {
        $('.jarallax').jarallax({
            speed: 0.2
        });
    }

    // ****************************
    // :: 10.0 Scrollup Active Code
    // ****************************
    if ($.fn.scrollUp) {
        hami_window.scrollUp({
            scrollSpeed: 1500,
            scrollText: '<i class="arrow_carrot-up"</i>'
        });
    }

    // ******************************
    // :: 11.0 Counter Up Active Code
    // ******************************
    if ($.fn.counterUp) {
        $('.counter').counterUp({
            delay: 15,
            time: 1500
        });
    }

    // *********************************
    // :: 12.0 Prevent Default 'a' Click
    // *********************************
    $('a[href="#"]').on('click', function ($) {
        $.preventDefault();
    });

    // ******************************
    // :: 13.0 Countdown Active Code
    // ******************************
    if ($.fn.countdown) {
        $("#clock").countdown("2021/10/10", function (event) {
            $(this).html(event.strftime("<div>%D <span>Days</span></div> <div>%H <span>Hours</span></div> <div>%M <span>Mins</span></div> <div>%S <span>Sec</span></div>"));
        });
    }




    let textIndex = 0;
    const textArray = ["The Best  Automation Trading", "The Best  neural network for trading"];
    let text = textArray[textIndex];
    let p = document.getElementById("text");
    const cursor = document.getElementsByClassName('probel')[0];
    cursor.textContent = '|';

    let i = 0;
    let text1 = '';

    const input = (i) => {
    setTimeout(() => {
        text1 += text[i];
        //console.log(text);
        p.textContent = text1;
        p.append(cursor);
    }, 100 * i);
    }
    var price = document.getElementById('text');
    
    const animateText = async () => {
    while (true) {
        for (let i = 0; i < text.length; i++) {
        input(i);
        await new Promise(resolve => setTimeout(resolve, 100));
        }
        price.style.opacity = 1;
        await new Promise(resolve => setTimeout(resolve, 10000));
        
        for (let i = text.length - 1; i >= 0; i--) {
        text1 = text1.slice(0, -1);
        p.textContent = text1;
        await new Promise(resolve => setTimeout(resolve, 100));
        }
        textIndex = (textIndex + 1) % textArray.length;
        text = textArray[textIndex];
    }
    }

    animateText();
    let pad1 = document.getElementById("pad1"); 
    let pad2 = document.getElementById("pad2"); 
    let pad3 = document.getElementById("pad3"); 
    const tablets = document.querySelectorAll('.Tablet');
    document.querySelector('.Tablet:first-of-type').classList.add('active');
    pad2.setAttribute('hidden', true);
    pad3.setAttribute('hidden', true);
    //pad1.setAttribute('hidden', false);
    
    tablets.forEach((tablet, index) => {
      tablet.addEventListener('click', () => {
        // удаляем класс active у всех элементов
        tablets.forEach(i => i.classList.remove('active'));
        // добавляем класс active к текущему элементу
        tablet.classList.add('active');
        
        if (index === 0) {
        pad1.removeAttribute('hidden');
        pad2.setAttribute('hidden', true);
        pad3.setAttribute('hidden', true);
        } else if (index === 1) {
        pad1.setAttribute('hidden', true);
        pad2.removeAttribute('hidden');
        pad3.setAttribute('hidden', true);
        } else if (index === 2) {
        pad1.setAttribute('hidden', true);
        pad2.setAttribute('hidden', true);
        pad3.removeAttribute('hidden');
        }
      });
    });

    //SCROLLER Overall Features


    let tablet1 = document.getElementById("tablet1"); 
    let tablet2 = document.getElementById("tablet2"); 
    let tablet3 = document.getElementById("tablet3"); 
    const mobiletablets = document.querySelectorAll('.mobile-Tablet');
    document.querySelector('.mobile-Tablet:first-of-type').classList.add('active');
    tablet2.setAttribute('hidden', true);
    tablet3.setAttribute('hidden', true);
    //pad1.setAttribute('hidden', false);
    
    mobiletablets.forEach((mobiletablet, index) => {
        mobiletablet.addEventListener('click', () => {
        // удаляем класс active у всех элементов
        mobiletablets.forEach(i => i.classList.remove('active'));
        // добавляем класс active к текущему элементу
        mobiletablet.classList.add('active');
        
        if (index === 0) {
        tablet1.removeAttribute('hidden');
        tablet2.setAttribute('hidden', true);
        tablet3.setAttribute('hidden', true);
        } else if (index === 1) {
        tablet1.setAttribute('hidden', true);
        tablet2.removeAttribute('hidden');
        tablet3.setAttribute('hidden', true);
        } else if (index === 2) {
        tablet1.setAttribute('hidden', true);
        tablet2.setAttribute('hidden', true);
        tablet3.removeAttribute('hidden');
        }
      });
    });

    //Accordeon 1

    const tabletItems = document.querySelectorAll('.Tablet_item');

    tabletItems.forEach(item => {
    const title = item.querySelector('.Tablet-title');
    const text = item.querySelector('.Mobile_tablet_text');
    
    title.addEventListener('click', () => {
        text.classList.toggle('opened');
        item.classList.toggle('opened');
        title.classList.toggle('opened');
    });


    });

    //Accordeon FAQ

    const tabletItemsFAQ = document.querySelectorAll('.Tablet_item_FAQ');

    tabletItemsFAQ.forEach(itemFAQ => {
    const titleFAQ = item.querySelector('.Tablet-title_FAQ');
    const textFAQ = item.querySelector('.Mobile_tablet_text_FAQ');
    
    titleFAQ.addEventListener('click', () => {
        textFAQ.classList.toggle('opened');
        itemFAQ.classList.toggle('opened');
        titleFAQ.classList.toggle('opened');
    });


    });


    //Investment calculator

    const scrollbar = document.getElementById('scrollbar');
    const inputbar = document.getElementById("inputbar");
    //const investmentAmount = document.getElementById('investment-amount');
    //const investmentDuration = document.querySelectorAll('.investment-duration');
    const profits = document.querySelectorAll('.term-option');
    let percentage = 0;
    profits.forEach((profit, index) => {
      profit.addEventListener('click', () => {

        profits.forEach(i => i.classList.remove('selected'));
        // добавляем класс active к текущему элементу
        profit.classList.add('selected');

        if (index === 0) {
            percentage = 0.013;
        } else if (index === 1) {
            percentage = 0.057;
        } else if (index === 2) {
            percentage = 0.25;
        } else if (index === 3) {
            percentage = 2.7;
        }
        const inputbar = document.getElementById("inputbar");
        const value1 = inputbar.value.replaceAll(',', '');
        const value = value1.replaceAll(' ', '');
        const investment = parseInt(value);
        const profit1 = investment * percentage;
        const total = investment + parseInt(profit1);
        document.querySelector(".investment-profit span").textContent = profit1.toFixed(2).toLocaleString();
        document.querySelector(".investment-result-text").textContent = total.toFixed(2).toLocaleString();
        document.querySelector(".investment-percent span").textContent = percentage * 100 + "%";
      });
    });

    

    function updateValues() {
        const scrollbar = document.getElementById("scrollbar");
        const inputbar = document.getElementById("inputbar");
        //const value = scrollbar.value.replaceAll(' ', ''); // удаляем пробелы
        //console.log(value)
        const investment = parseFloat(scrollbar.value) * 1000000;
        //console.log(investment)
        //const days = document.querySelector(".investment-term.selected").dataset.days;
        const profit = investment * percentage;
        const total = investment + parseFloat(profit);
        //percentage = parseFloat(percentage).toFixed(2);
        document.getElementById('inputbar').value = investment.toLocaleString('en-US');
        document.querySelector(".investment-profit span").textContent = profit.toFixed(2).toLocaleString();
        document.querySelector(".investment-result-text").textContent = total.toFixed(2).toLocaleString();
        document.querySelector(".investment-percent span").textContent = percentage * 100 + "%";
    }


    
    function updateValues2() {
        const scrollbar = document.getElementById("scrollbar");
        const scrollbarthumb = document.querySelector(".investment-scrollbar::-webkit-scrollbar-thumb");
        const inputbar = document.getElementById("inputbar");
        const value = inputbar.value.replaceAll(' ', ''); // удаляем пробелы

        
        // Удаляем все нецифровые символы, кроме пробелов
        inputbar.value = inputbar.value.replace(/[^0-9 ]/g, '');
        // Удаляем все пробелы
        inputbar.value = inputbar.value.replace(/\s/g, '');
        // Добавляем пробелы между разрядами числа
        inputbar.value = inputbar.value.replace(/(\d)(?=(\d{3})+(?!\d))/g, '$1 ');

        if (value == undefined) {
            value = 0;
          }
       
        const investment = parseInt(value);
        
        //const days = document.querySelector(".investment-term.selected").dataset.days;
        const profit = investment * percentage;
        const total = investment + parseFloat(profit);
        //percentage = parseFloat(percentage).toFixed(2);
        //document.querySelector(".investment-amount span").textContent = investment.toLocaleString();
        document.querySelector(".investment-profit span").textContent = profit.toFixed(2).toLocaleString();
        document.querySelector(".investment-result-text").textContent = total.toFixed(2).toLocaleString();
        document.querySelector(".investment-percent span").textContent = percentage * 100 + "%";
        
        if (value > 1000000) {
            document.getElementById('inputbar').value = 1000000;
          } else {
              document.getElementById('inputbar').value = inputbar.value;
          }
        
        if (value == undefined) {
            
            document.getElementById('inputbar').value = 0;
        }  

        document.getElementById('scrollbar').value = investment / 1000000;
        const scrollbarpercent = investment / 1000000;

        // Вычисляем позицию для ползунка
        const position = (scrollbarpercent - scrollbar.min) / (scrollbar.max - scrollbar.min) * 100;

        // Применяем анимированный стиль к ползунку
        //scrollbarthumb.style.transition = 'transform 0.2s ease-in-out';
        //scrollbarthumb.style.transform = `translateX(${position}%)`;
        
        //scrollbarthumb.style.setProperty('transition', `translateX(${position}%)`);
        
        // Убираем анимацию после окончания перетаскивания ползунка
        //scrollbar.addEventListener('mouseup', () => {
        //    scrollbarthumb.style.transition = '';
        //});
    }

    // Обновляем значения на странице при каждом перемещении скроллбара
    scrollbar.addEventListener('input', updateValues);
    
    // Обновляем значения на странице при каждом ввение нового значения
    inputbar.addEventListener('input', updateValues2);


    // Инициализируем Swiper
    const swiper = new Swiper('.swiper-container', {
    direction: 'horizontal',
    loop: true,
    autoplay: {
        delay: 3000,
      },

    
    spaceBetween: 40,
    centeredSlides: false,
    freeMode: false,
    scrollbar: {
        el: '.swiper-scrollbar',
        hide: true,
        draggable: false,
    },
    slidesPerView: 3,
    breakpoints: {
        1024: {
          slidesPerView: 3
        },
        768: {
          slidesPerView: 3
        },
        767: {
          slidesPerView: 1
        }
    }
    });

    // Слушаем изменение прогресс-бара
    swiper.on('scrollbarDragMove', function () {
    const progressBar = document.querySelector('.swiper-scrollbar-drag');
    progressBar.style.width = `${swiper.scrollbar.dragSize}px`;
    });

    

    

    

})(jQuery);