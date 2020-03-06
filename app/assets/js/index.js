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
  const handlers = {
      'moment-up': function (e) {
          e.preventDefault();
          const moment = _closest(e.target, '[data-moment]');
          d.querySelector('form').moveMoment(-1, moment);
         _closest(e.target, '[data-edit-timeline]').save();
      },
      'moment-down': function (e) {
          e.preventDefault();
          const moment = _closest(e.target, '[data-moment]');
          d.querySelector('form').moveMoment(1, moment);
         _closest(e.target, '[data-edit-timeline]').save();

      },
      'save-moment': function(e){
         e.preventDefault();
         _closest(e.target, '[data-edit-moment]').submit();
      }
  };
    const decorators = {
        'edit-moment': function () {
            const self = this,
                id = this.dataset.id,
                csrfToken = d.querySelector('input[name="csrfmiddlewaretoken"]').value,
                _getFormData = function () {
                    var data = {},
                        i,
                        fields = self.querySelectorAll('input[type="text"], input[type="hidden"], textarea');
                    for (i = 0; i < fields.length; i++){
                        const nameSplit = fields[i].getAttribute('name').split('-');
                        data[nameSplit[nameSplit.length-1]] = fields[i].value;
                    }
                    data['csrfmiddlewaretoken'] = csrfToken;
                    return data;
                },
                _init = function(){
                    const data = _getFormData();
                },
                _submit = function () {
                    const data = _getFormData();
                    console.log(data);
                     var xhr = new XMLHttpRequest();
                    xhr.open('POST', '/timeline/update-moment/' + id, true);
                    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
                    xhr.send(_formDataToQueryString(data));
                    xhr.onreadystatechange = function() {
                        console.log(this);
                      if (this.readyState === XMLHttpRequest.DONE) {
                        if (this.status === 200) {

                        } else {
                          alert('Er ging iets mis.');
                        }
                      }
                    }
                }
            _init();
            self.dataset.editMoment = self;
            self.submit = _submit;

        },
        'edit-timeline': function () {
            const self = this,
                momentContainer = self.querySelector('[data-moment-container]'),
                savedMomentQ = '[data-id]',
                _getFormData = function(){
                  return Array.prototype.slice.call(momentContainer.querySelectorAll(savedMomentQ)).map(function(e, index){return {"id": e.dataset.id, "order": index}});
                },
                _submit = function () {
                    const data = _getFormData();
                     var xhr = new XMLHttpRequest();
                    xhr.open('POST', '/timeline/order', true);
                    xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
                    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
                    xhr.setRequestHeader("X-CSRFToken", d.querySelector('input[name="csrfmiddlewaretoken"]').value);
                    xhr.send(JSON.stringify(data));
                    xhr.onreadystatechange = function() {
                      if (this.readyState === XMLHttpRequest.DONE) {
                        if (this.status === 200) {

                        } else {
                          alert('Er ging iets mis.');
                        }
                      }
                    }
                },
                _order = function(direction, momentElem){
                    const items = momentContainer.querySelectorAll(savedMomentQ);
                },
                _init = function () {
                    const items = momentContainer.querySelectorAll(savedMomentQ);
                    var i;
                    momentContainer.style.display = 'flex';
                    momentContainer.style.flexDirection = 'column';
                    for (i = 0; i < items.length; i++) {
                        items[i].dataset.order = i;
                        items[i].style.order = i;
                    }
                    _submit();
                };

            self.dataset.editTimeline = self;
            self.save = _submit;
            self.order = _order;
            _init();
        },
        'timeline-sort': function () {
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
    var decoratorsElements = {};

  d.addEventListener('click',function(t){var k,e,a=t&&t.target;if(a=_closest(a,'[data-handler]')){var r=a.getAttribute('data-handler').split(/\s+/);if('A'==a.tagName&&(t.metaKey||t.shiftKey||t.ctrlKey||t.altKey))return;for(e=0;e<r.length;e++){k=r[e].split(/[\(\)]/);handlers[k[0]]&&handlers[k[0]].call(a,t,k[1])}}});
  var _decorate = function(){var k,i,j,decoratorString,el,els=d.querySelectorAll('[data-decorator]');for(i=0;i<els.length;i++){for(decoratorString=(el=els[i]).getAttribute('data-decorator').split(/\s+/),j=0;j<decoratorString.length;j++){k=decoratorString[j].split(/[\(\)]/);decorators[k[0]]&&decorators[k[0]].call(el,k[1]);el.removeAttribute('data-decorator')}}};
  var _closest=function(e,t){var ms='MatchesSelector',c;['matches','webkit'+ms,'moz'+ms,'ms'+ms,'o'+ms].some(function(e){return'function'==typeof document.body[e]&&(c=e,!0)});var r=e;try{for(;e;){if(r&&r[c](t))return r;e=r=e.parentElement}}catch(e){}return null};
    var _formDataToQueryString = function(data){
                    var out = '', i;
                    for (var k in data){
                        if (data.hasOwnProperty(k)){
                            out += encodeURIComponent(k) + '=' + encodeURIComponent(data[k]) + '&';
                        }
                    }
                    return out;
                };

  _decorate();

}(window, document.documentElement);
