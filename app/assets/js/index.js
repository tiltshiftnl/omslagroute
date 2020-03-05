const fileUpload = document.getElementById('file-upload');
const filesUploaded = document.getElementById( 'file-upload-filename' );

if (fileUpload && fileUpload.addEventListener) {
    fileUpload.addEventListener('change', showFileName);
}

function showFileName( event ) {
    const input = event.srcElement;
    const fileName = input.files[0].name;
    filesUploaded.textContent = 'Geselecteerd bestand: ' + fileName;
}

if (document.addEventListener){
    document.addEventListener('invalid', function(e){
        e.target.className += ' invalid';
    }, true);
}

Array.prototype.sortOnData = function(key){
    this.sort(function(a, b){
        if(a.dataset[key] < b.dataset[key]){
            return -1;
        }else if(a.dataset[key] > b.dataset[key]){
            return 1;
        }
        return 0;
    });
};

!function (w, d) {
  var handlers = {
      'moment-up': function (e) {
          e.preventDefault();
          const moment = _closest(e.target, '[data-moment]');
          d.querySelector('form').moveMoment(-1, moment);
      },
      'moment-down': function (e) {
          e.preventDefault();
          const moment = _closest(e.target, '[data-moment]');
          d.querySelector('form').moveMoment(1, moment);

      }
  };
    var decorators = {
        'timeline-form': function () {
            const self = this,
                momentFormList = self.querySelectorAll('[data-moment]'),
                _init = function (items) {
                    const momentContainer = items[0].parentNode;
                    var i;
                    momentContainer.style.display = 'flex';
                    momentContainer.style.flexDirection = 'column';
                    for (i = 0; i < items.length; i++) {
                        items[i].dataset.order = i;
                        items[i].style.order = i;
                    }
                },
                _moveMoment = function (direction, momentElem) {
                    var items = Array.prototype.slice.call(momentElem.parentNode.children);
                    items.sortOnData('order');
                    const index = items.indexOf(momentElem),
                        currentOrder = momentElem.dataset.order,
                        nextElem = items[index + direction];
                    if (nextElem){
                        momentElem.dataset.order = nextElem.dataset.order;
                        nextElem.dataset.order = currentOrder;
                        momentElem.style.order = momentElem.dataset.order;
                        nextElem.style.order = nextElem.dataset.order;
                    }
                },
                _submit = function(e){
                    console.log('submit');
                    for (var i = 0; i < momentFormList.length; i++){
                        if (!momentFormList[i].hasAttribute('data-new-moment')){
                            momentFormList[i].querySelector('input[name$="-order"]').value = momentFormList[i].dataset.order;
                        }
                    }
                };

            _init(momentFormList);
            this.moveMoment = _moveMoment;
            this.addEventListener('submit', _submit);
        }
    };

  d.addEventListener('click',function(t){var k,e,a=t&&t.target;if(a=_closest(a,'[data-handler]')){var r=a.getAttribute('data-handler').split(/\s+/);if('A'==a.tagName&&(t.metaKey||t.shiftKey||t.ctrlKey||t.altKey))return;for(e=0;e<r.length;e++){k=r[e].split(/[\(\)]/);handlers[k[0]]&&handlers[k[0]].call(a,t,k[1])}}});
  var _decorate = function(){var k,i,j,decoratorString,el,els=d.querySelectorAll('[data-decorator]');for(i=0;i<els.length;i++){for(decoratorString=(el=els[i]).getAttribute('data-decorator').split(/\s+/),j=0;j<decoratorString.length;j++){k=decoratorString[j].split(/[\(\)]/);decorators[k[0]]&&decorators[k[0]].call(el,k[1]);el.removeAttribute('data-decorator')}}};
  var _closest=function(e,t){var ms='MatchesSelector',c;['matches','webkit'+ms,'moz'+ms,'ms'+ms,'o'+ms].some(function(e){return'function'==typeof document.body[e]&&(c=e,!0)});var r=e;try{for(;e;){if(r&&r[c](t))return r;e=r=e.parentElement}}catch(e){}return null};

  _decorate();

}(window, document.documentElement);
