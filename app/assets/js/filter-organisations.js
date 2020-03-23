document.addEventListener('click', function (e) {
    var button = e.target;
    console.log(button);

    if (!button.hasAttribute('data-highlight-org')) return;

    button.classList.toggle("button--tag--selected");
    var filter = button.getAttribute('data-highlight-org');
    console.log('clicked button and filtering for ' + filter);
    filterTag(filter);

    function filterTag(filter) {

        // each step which this organisation is involved in
        var steps = document.querySelectorAll('[data-tags*="' + filter + '"]');
        console.table(steps);

        // find all tags buttons and highlight them too
        var tags = document.querySelectorAll('[data-select-targetgroup*="' + filter + '"]');
        console.table(tags);

        for (var i = 0; i < steps.length; i++) {
            steps[i].classList.toggle("detail-wrapper--highlighted");
        }

        for (var i = 0; i < tags.length; i++) {
            tags[i].classList.toggle("button--tag--selected");
        }

        var stepsContainer = document.querySelectorAll(".details-wrapper");

        for (var i = 0; i < stepsContainer.length; i++) {
            if (!stepsContainer[i].classList.contains("detail-wrapper--highlighted")) {
                stepsContainer[i].classList.toggle("detail-wrapper--passive");
            }
        }
    }

    // Reset filters
    function resetFilter(filter) {
        // each step which this organisation is involved in
        var steps = document.querySelectorAll('[data-tags*="' + filter + '"]');

        // find all tags buttons and highlight them too
        var tags = document.querySelectorAll('[data-highlight-org*="' + filter + '"]');

        for (var i = 0; i < steps.length; i++) {
            steps[i].classList.remove("detail-wrapper--highlighted");
        }

        for (var i = 0; i < tags.length; i++) {
            tags[i].classList.remove("button--tag--selected");
        }
    }
});