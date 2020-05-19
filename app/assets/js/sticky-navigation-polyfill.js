(function() {
    "use strict";
    var stickyNav = document.getElementsByClassName("grid__aside--sticky")[0];
    if(stickyNav !== undefined){
        var isIE11 = !!window.MSInputMethodContext && !!document.documentMode;
        if(isIE11){
            window.addEventListener('scroll', function(e) {
                var last_known_scroll_position = window.scrollY;
            
                this.console.log("last_known_scroll_position", last_known_scroll_position);
                stickyNav.style.marginTop = last_known_scroll_position  + "px";
            });
        }
        
    }

})();