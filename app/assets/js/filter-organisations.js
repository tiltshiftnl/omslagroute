var selectedTags = new Array();
document.addEventListener('click', function (e) {
var button = e.target; // if we clicked something that is not a tag button, get out

if (!button.hasAttribute('data-highlight-org')) return;
var filter = button.getAttribute('data-highlight-org');
filterTag(filter);
button.blur();

    function filterTag(filter) {
        var stepsContainer = document.querySelector(".section--timeline");
        // if the filter appears in the array, add classes and highlight all occurrences

        if (selectedTags.indexOf(filter) == -1) {
            button.classList.add("button--tag--selected");
            selectedTags.push(filter);
            stepsContainer.classList.add("section--timeline--filtering");
            var steps = document.querySelectorAll('[data-tags*="' + filter + '"]');

            for (var i = 0; i < steps.length; i++) {
                steps[i].classList.add("detail-wrapper--highlighted");
            }

            var tags = document.querySelectorAll('[data-select-targetgroup*="' + filter + '"]');

            for (var i = 0; i < tags.length; i++) {
                tags[i].classList.add("button--tag--selected");
            }
        } else {
            button.classList.remove("button--tag--selected");
            // remove the search term from the array, and clean up associated classes

            var found = selectedTags.indexOf(filter);

            while (found !== -1) {
                selectedTags.splice(found, 1);
                found = selectedTags.indexOf(filter);
            } // if this was the last filter to be toggled off, stop subdueing the other dots

            if (selectedTags.length == 0) {
                stepsContainer.classList.remove("section--timeline--filtering");
            }

            var tags = document.querySelectorAll('[data-select-targetgroup*="' + filter + '"]');

            for (var i = 0; i < tags.length; i++) {
                tags[i].classList.remove("button--tag--selected");
            }
    
            var steps = document.querySelectorAll('[data-tags*="' + filter + '"]');

            for (var i = 0; i < steps.length; i++) {
                // loop through every step which has the organisation in the data-attribute
                // and create an array out of the organisations linked to the step
                var dataTags = steps[i].getAttribute("data-tags").split(" ");
                // remove empty strings from the array
                dataTags = dataTags.filter(Boolean);

                if (dataTags.length == 1) {
                    // if this is step has only one organisation
                    steps[i].classList.remove("detail-wrapper--highlighted");
                } else {
                    var findOne = function (dataTags, selectedTags) {
                        return selectedTags.some(function (v) {
                            return dataTags.indexOf(v) >= 0;
                        });
                    };

                    if (findOne) {
                        // if we find a match between both arrays, keep the highlight, because there are still organisations that should keep the step highlighted
                    } else {
                        steps[i].classList.remove("detail-wrapper--highlighted");
                    }
                }
            }
        }
    }
});