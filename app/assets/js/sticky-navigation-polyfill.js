(function() {
    "use strict";
    var stickyNav = document.getElementsByClassName("grid__aside--sticky")[0];
    if(stickyNav !== undefined){
        var isIE11 = !!window.MSInputMethodContext && !!document.documentMode;
        if(isIE11){
            var viewportOffsetTop = 0;
        
            function setMarginTop(){
                var last_known_scroll_position = window.pageYOffset;
                        var marginTop = (viewportOffsetTop-last_known_scroll_position) < 0 ? -(viewportOffsetTop-last_known_scroll_position) : 0;
                        stickyNav.style.marginTop =  marginTop+78+ "px";
            }
            
            viewportOffsetTop = stickyNav.getBoundingClientRect().top + window.pageYOffset;
            window.addEventListener('load', function(e) {
                setMarginTop();
            });
            window.addEventListener('scroll', function(e) {
                setMarginTop();
            });
        }
    }
})();
