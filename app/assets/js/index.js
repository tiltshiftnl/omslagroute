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
          const moment = _closest(e.target, '[data-id]');
         _closest(e.target, '[data-edit-timeline]').order(-1, moment);
      },
      'moment-down': function (e) {
          e.preventDefault();
          const moment = _closest(e.target, '[data-id]');
         _closest(e.target, '[data-edit-timeline]').order(1, moment);

      },
      'new-moment': function (e) {
          e.preventDefault();
          const self = _closest(e.target, '[data-handler="new-moment"]');
          const moment = _closest(e.target, '[data-id]'),
              proto = d.querySelector('[data-new-moment-proto]').cloneNode(true);
          _insertAfter(proto, moment);
          self.style.display = 'none';
          proto.style.display = 'block';
          proto.dataset.decorator = 'new-moment';
          _decorate();
      },
      'exit-new-moment': function (e) {
          e.preventDefault();
          const self = _closest(e.target, '[data-handler="exit-new-moment"]'),
              container = _closest(self, '[data-new-moment-proto]');
          container.parentElement.removeChild(container);

      },
    'save-new-moment': function(e){
        e.preventDefault();
          const self = _closest(e.target, '[data-handler="save-new-moment"]'),
            container = _closest(self, '[data-new-moment-proto]');
          container.save();

      },
      'save-moment': function(e){
         e.preventDefault();
         _closest(e.target, '[data-edit-moment]').submit();
      }
  };
    const decorators = {
        'new-moment': function () {
            const self = this,
                _getFormData = function () {
                    var data = {},
                        i,
                        fields = self.querySelectorAll('input[type="text"], input[type="hidden"], textarea');
                    for (i = 0; i < fields.length; i++){
                        data[fields[i].getAttribute('name')] = fields[i].value;
                    }
                    return data;
                },
                _save = function(data){
                    var xhr = new XMLHttpRequest();
                    xhr.open('POST', '/timeline/create-moment', true);
                    xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
                    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
                    xhr.setRequestHeader("X-CSRFToken", d.querySelector('input[name="csrfmiddlewaretoken"]').value);
                    xhr.send(JSON.stringify(_getFormData()));
                    xhr.onreadystatechange = function() {
                      if (this.readyState === XMLHttpRequest.DONE) {
                        const response = JSON.parse(this.response);
                        if (this.status === 201) {
                            self.dataset.id = response.message.id;
                            d.querySelector('[data-edit-timeline]').save();
                        }
                        else if (this.status === 200){
                            for (var k in response.message){
                                if (response.message.hasOwnProperty(k)){
                                self.querySelector('[name="'+ k +'"]').dataset.errorMessage = response.message[k]
                                }
                            }
                        } else {
                          alert('Er ging iets mis.');
                        }
                      }
                    }
                },
                _init = function(){

                };
            _init();
            self.save = _save;
        },
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
                  return _toArray(momentContainer.querySelectorAll(savedMomentQ)).map(function(e){return {"id": e.dataset.id, "order": e.dataset.order}});
                },
                _getFormInitialData = function(){
                  return _toArray(momentContainer.querySelectorAll(savedMomentQ)).map(function(e, index){return {"id": e.dataset.id, "order": index}});
                },
                _save = function(){
                    const data = _toArray(momentContainer.querySelectorAll(savedMomentQ)).map(function(e, index){return {"id": e.dataset.id, "order": index}});
                    _submit(data);
                },
                _submit = function (data) {
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
                    const items = _toArray(momentContainer.querySelectorAll(savedMomentQ));
                    var i;
                    items.sortOnData('order');
                    const index = items.indexOf(momentElem),
                        currentOrder = momentElem.dataset.order,
                        nextElem = items[index + direction];
                    if (nextElem){
                        momentElem.dataset.order = nextElem.dataset.order;
                        nextElem.dataset.order = currentOrder;
                        items.sortOnData('order');
                        for (i = 0; i < items.length; ++i) {
                          momentContainer.appendChild(items[i]);
                        }
                        console.log(items.map(function(e){return {'id': e.dataset.id, 'order': e.dataset.order}}));
                        _submit(items.map(function(e){return {'id': e.dataset.id, 'order': e.dataset.order}}));
                    }
                    // const data = _getFormData();
                },
                _init = function () {
                    const items = momentContainer.querySelectorAll(savedMomentQ),
                        data = _getFormInitialData();
                    var i;
                    for (i = 0; i < items.length; i++) {
                        items[i].dataset.order = i;
                    }
                    console.log(_toArray(items).map(function(e){return {'id': e.dataset.id, 'order': e.dataset.order}}));

                    _submit(data);
                };

            self.dataset.editTimeline = self;
            self.save = _save;
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
    var _toArray = function(a){return Array.prototype.slice.call(a);};
    var _insertAfter = function (newNode, referenceNode) {
        referenceNode.parentNode.insertBefore(newNode, referenceNode.nextSibling);
    }
var helpers = {
    'ajax': function (options) {
      var request = new XMLHttpRequest(),
        headers = options.headers || [],
        i;
      request.open(options.type, options.url, true);
      for (i = 0; i < headers.length; i++){
        request.setRequestHeader(headers[i][0], headers[i][1]);
      }
      request.onreadystatechange = function () {
        if (request.readyState == 4) {
          if (request.status >= 200 && request.status < 400) {
            if (options.callback && typeof (options.callback) == 'function') {
              options.callback.call(request, request.responseText);
            }
          } else {
            if (options.error && typeof (options.error) == 'function') {
              options.error.call(request, request.responseText);
            }
          }
          _decorate();
        }
      };

      request.send(options.data);

      return request;
    }
    }

   _decorate();

}(window, document.documentElement);
