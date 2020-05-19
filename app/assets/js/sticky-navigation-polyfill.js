(function() {
    "use strict";
    var stickyNav = document.getElementsByClassName("grid__aside--sticky")[0];
    if(stickyNav !== undefined){
        var isIE11 = !!window.MSInputMethodContext && !!document.documentMode;
        if(isIE11){
            window.addEventListener('scroll', function(e) {
                var last_known_scroll_position = window.pageYOffset;
                stickyNav.style.marginTop = last_known_scroll_position  + "px";
            });
        }
    }
})();
