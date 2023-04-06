/*

=========================================================
* Volt Pro - Premium Bootstrap 5 Dashboard
=========================================================

* Product Page: https://themesberg.com/product/admin-dashboard/volt-bootstrap-5-dashboard
* Copyright 2021 Themesberg (https://www.themesberg.com)

* Designed and coded by https://themesberg.com

=========================================================

* The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software. Please contact us to request a removal. Contact us if you want to remove it.

*/
 
"use strict";
const dd = document;
dd.addEventListener("DOMContentLoaded", function(event) {

    

    // const swalWithBootstrapButtons = Swal.mixin({
    //     customClass: {
    //         confirmButton: 'btn btn-primary me-3',
    //         cancelButton: 'btn btn-gray'
    //     },
    //     buttonsStyling: false
    // });

    var themeSettingsEl = document.getElementById('theme-settings');
    var themeSettingsExpandEl = document.getElementById('theme-settings-expand');

    if(themeSettingsEl) {

        var themeSettingsCollapse = new bootstrap.Collapse(themeSettingsEl, {
            show: true,
            toggle: false
        });

        if (window.localStorage.getItem('settings_expanded') === 'true') {
            themeSettingsCollapse.show();
            themeSettingsExpandEl.classList.remove('show');
        } else {
            themeSettingsCollapse.hide();
            themeSettingsExpandEl.classList.add('show');
        }
        
        themeSettingsEl.addEventListener('hidden.bs.collapse', function () {
            themeSettingsExpandEl.classList.add('show');
            window.localStorage.setItem('settings_expanded', false);
        });

        themeSettingsExpandEl.addEventListener('click', function () {
            themeSettingsExpandEl.classList.remove('show');
            window.localStorage.setItem('settings_expanded', true);
            setTimeout(function() {
                themeSettingsCollapse.show();
            }, 300);
        });
    }

    // options
    const breakpoints = {
        sm: 540,
        md: 720,
        lg: 960,
        xl: 1140
    };

    var sidebar = document.getElementById('sidebarMenu')
    if(sidebar && dd.body.clientWidth < breakpoints.lg) {
        sidebar.addEventListener('shown.bs.collapse', function () {
            document.querySelector('body').style.position = 'fixed';
        });
        sidebar.addEventListener('hidden.bs.collapse', function () {
            document.querySelector('body').style.position = 'relative';
        });
    }

    var topbar = document.getElementById('topbarMenu')
    if(topbar && dd.body.clientWidth < breakpoints.lg) {
        topbar.addEventListener('shown.bs.collapse', function () {
            document.querySelector('body').style.position = 'fixed';
        });
        topbar.addEventListener('hidden.bs.collapse', function () {
            document.querySelector('body').style.position = 'relative';
        });
    }

    var iconNotifications = dd.querySelector('.notification-bell');
    if (iconNotifications) {
        iconNotifications.addEventListener('shown.bs.dropdown', function () {
            iconNotifications.classList.remove('unread');
        });
    }

    [].slice.call(dd.querySelectorAll('[data-background]')).map(function(el) {
        el.style.background = 'url(' + el.getAttribute('data-background') + ')';
    });

    [].slice.call(dd.querySelectorAll('[data-background-lg]')).map(function(el) {
        if(document.body.clientWidth > breakpoints.lg) {
            el.style.background = 'url(' + el.getAttribute('data-background-lg') + ')';
        }
    });

    [].slice.call(dd.querySelectorAll('[data-background-color]')).map(function(el) {
        el.style.background = 'url(' + el.getAttribute('data-background-color') + ')';
    });

    [].slice.call(dd.querySelectorAll('[data-color]')).map(function(el) {
        el.style.color = 'url(' + el.getAttribute('data-color') + ')';
    });

    //Tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
    return new bootstrap.Tooltip(tooltipTriggerEl)
    })


    // Popovers
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'))
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
      return new bootstrap.Popover(popoverTriggerEl)
    })
    

    // Datepicker
    var datepickers = [].slice.call(dd.querySelectorAll('[data-datepicker]'))
    var datepickersList = datepickers.map(function (el) {
        return new Datepicker(el, {
            buttonClass: 'btn'
          });
    })

    if(dd.querySelector('.input-slider-container')) {
        [].slice.call(dd.querySelectorAll('.input-slider-container')).map(function(el) {
            var slider = el.querySelector(':scope .input-slider');
            var sliderId = slider.getAttribute('id');
            var minValue = slider.getAttribute('data-range-value-min');
            var maxValue = slider.getAttribute('data-range-value-max');

            var sliderValue = el.querySelector(':scope .range-slider-value');
            var sliderValueId = sliderValue.getAttribute('id');
            var startValue = sliderValue.getAttribute('data-range-value-low');

            var c = dd.getElementById(sliderId),
                id = dd.getElementById(sliderValueId);

            noUiSlider.create(c, {
                start: [parseInt(startValue)],
                connect: [true, false],
                //step: 1000,
                range: {
                    'min': [parseInt(minValue)],
                    'max': [parseInt(maxValue)]
                }
            });
        });
    }

    if (dd.getElementById('input-slider-range')) {
        var c = dd.getElementById("input-slider-range"),
            low = dd.getElementById("input-slider-range-value-low"),
            e = dd.getElementById("input-slider-range-value-high"),
            f = [dd, e];

        noUiSlider.create(c, {
            start: [parseInt(low.getAttribute('data-range-value-low')), parseInt(e.getAttribute('data-range-value-high'))],
            connect: !0,
            tooltips: true,
            range: {
                min: parseInt(c.getAttribute('data-range-value-min')),
                max: parseInt(c.getAttribute('data-range-value-max'))
            }
        }), c.noUiSlider.on("update", function (a, b) {
            f[b].textContent = a[b]
        });
    }

    //Chartist

     
    
    if(dd.querySelector('.ct-chart-sales-value')) {
        //Chart 5
          new Chartist.Line('.ct-chart-sales-value',          
          {
            labels: day_of_week,
            series: [
                total_of_day
            ]
          }, {
            low: 0,
            showArea: true,
            fullWidth: false,
            plugins: [
              Chartist.plugins.tooltip()
            ],
            axisX: {
                // On the x-axis start means top and end means bottom
                position: 'end',
                showGrid: true,
                
            },
            axisY: {
                // On the y-axis start means left and end means right
                showGrid: false,
                showLabel: false,
                            

            }
        });
    }

    if(document.querySelector('.ct-chart-compjs')) {
    for (var df in dfh){
        var xxxx;
        xxxx = dfh[df];            
        for (var xx in xxxx){
            var yyyy, label, series;
            yyyy = xxxx[xx];
            label = yyyy[0];
            series = yyyy[1];
            if(document.querySelector('.ct-chart-compare' + xx)) {
                var compchart = new Chartist.Bar('.ct-chart-compare' + xx, {
                    labels: label,
                    series: series
                  }, {           
                    
                    seriesBarDistance: 10,
                    plugins: [
                      Chartist.plugins.tooltip()
                    ],
                    
                    axisX: {                        
                        offset: 100,                        
                      },
                    axisY: {
                        offset: 100,
                        labelInterpolationFnc: function(value) {
                            return value + ' %'
                            },
                            scaleMinSpace: 15    
                    }                    
                    });                  
                  compchart.on('draw', function(data) {
                    if(data.type === 'bar') {
                        data.element.attr({
                          style: 'stroke-width: 10px;stroke-linecap: square; width:auto;height:auto;'
                        });
                    }                     
                });
            }
        } 
    }
}







    if(dd.querySelector('.ct-chart-traffic-share')) {
        var data = {
            series: [70, 20, 10]
          };
          
          var sum = function(a, b) { return a + b };
          
          new Chartist.Pie('.ct-chart-traffic-share', data, {
            labelInterpolationFnc: function(value) {
              return Math.round(value / data.series.reduce(sum) * 100) + '%';
            },            
            low: 0,
            high: 8,
            donut: true,
            donutWidth: 20,
            donutSolid: true,
            fullWidth: false,
            showLabel: false,
            plugins: [
              Chartist.plugins.tooltip()
            ],
        });         
    }

    if (dd.getElementById('loadOnClick')) {
        dd.getElementById('loadOnClick').addEventListener('click', function () {
            var button = this;
            var loadContent = dd.getElementById('extraContent');
            var allLoaded = dd.getElementById('allLoadedText');
    
            button.classList.add('btn-loading');
            button.setAttribute('disabled', 'true');
    
            setTimeout(function () {
                loadContent.style.display = 'block';
                button.style.display = 'none';
                allLoaded.style.display = 'block';
            }, 1500);
        });
    }

    // var scroll = new SmoothScroll('a[href*="#"]', {
    //     speed: 500,
    //     speedAsDuration: true
    // });

    if(dd.querySelector('.current-year')){
        dd.querySelector('.current-year').textContent = new Date().getFullYear();
    }

    // Glide JS

    // if (d.querySelector('.glide')) {
    //     new Glide('.glide', {
    //         type: 'carousel',
    //         startAt: 0,
    //         perView: 3
    //       }).mount();
    // }

    // if (d.querySelector('.glide-testimonials')) {
    //     new Glide('.glide-testimonials', {
    //         type: 'carousel',
    //         startAt: 0,
    //         perView: 1,
    //         autoplay: 2000
    //       }).mount();
    // }

    // if (d.querySelector('.glide-clients')) {
    //     new Glide('.glide-clients', {
    //         type: 'carousel',
    //         startAt: 0,
    //         perView: 5,
    //         autoplay: 2000
    //       }).mount();
    // }

    // if (d.querySelector('.glide-news-widget')) {
    //     new Glide('.glide-news-widget', {
    //         type: 'carousel',
    //         startAt: 0,
    //         perView: 1,
    //         autoplay: 2000
    //       }).mount();
    // }

    // if (d.querySelector('.glide-autoplay')) {
    //     new Glide('.glide-autoplay', {
    //         type: 'carousel',
    //         startAt: 0,
    //         perView: 3,
    //         autoplay: 2000
    //       }).mount();
    // }

    // Pricing countup
    // var billingSwitchEl = d.getElementById('billingSwitch');
    // if(billingSwitchEl) {
    //     const countUpStandard = new countUp.CountUp('priceStandard', 99, { startVal: 199 });
    //     const countUpPremium = new countUp.CountUp('pricePremium', 199, { startVal: 299 });
        
    //     billingSwitchEl.addEventListener('change', function() {
    //         if(billingSwitch.checked) {
    //             countUpStandard.start();
    //             countUpPremium.start();
    //         } else {
    //             countUpStandard.reset();
    //             countUpPremium.reset();
    //         }
    //     });
    // }

});


///controlling popover for feedback button
var popoverTriggerEl = document.getElementById('feedbackbutton');
var popoverContent = '<div class="popover-content">If you have any suggestions about this page, please let us know by clicking this button. We will be grateful to you.<br>\
We record the page from which you provide your feedback. So while giving feedback write about this particular page only.</div>';
var popover = new bootstrap.Popover(popoverTriggerEl, {
trigger: 'manual',
html: true,
content: popoverContent
});
popover.show();
var offcanvasEl = document.getElementById('feedbackcanvas');
offcanvasEl.addEventListener('shown.bs.offcanvas', function () {
  popover.hide();
});
offcanvasEl.addEventListener('hidden.bs.offcanvas', function () {
    popover.show();
});


  
