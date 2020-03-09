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
              proto = d.querySelector('[data-moment-proto]').cloneNode(true);
          _insertAfter(proto, moment);
          self.style.visibility = 'hidden';
          proto.style.display = 'block';
          proto.dataset.decorator = 'edit-moment';
          _decorate();
      },
      'exit-new-moment': function (e) {
          e.preventDefault();
          const self = _closest(e.target, '[data-handler="exit-new-moment"]'),
              container = _closest(self, '[data-moment-proto]');
          container.parentElement.removeChild(container);
      },
      'delete-moment': function(e){
          e.preventDefault();
          const self = _closest(e.target, '[data-handler="delete-moment"]'),
              container = _closest(self, '[data-edit-moment]');
          if (confirm("Weet je zeker dat je het timeline item met naam '"+container.querySelector('[name$="name"]').value+"' wil verwijderen")) {
            container.delete();
          }
      },
      'save-moment': function(e){
          e.preventDefault();
          const self = _closest(e.target, '[data-handler="save-moment"]'),
            container = _closest(self, '[data-moment]');
         container.submit();
          container.parentElement.removeChild(container);
          location.reload();
      },
      'save-and-exit-new-moment': function(e){
        e.preventDefault();
        const self = _closest(e.target, '[data-handler="save-and-exit-new-moment"]'),
          container = _closest(self, '[data-moment-proto]');
        container.submit();
          container.parentElement.removeChild(container);
          location.reload();
    }
  };
    const decorators = {
        'edit-moment': function () {
            var savedTimeout;
            const self = this,
                id = this.dataset.id,
                _getFormData = function () {
                    var data = {},
                        i,
                        fields = self.querySelectorAll('input[type="text"], input[type="hidden"], textarea');
                    for (i = 0; i < fields.length; i++){
                        const nameSplit = fields[i].getAttribute('name').split('-');
                        data[nameSplit[nameSplit.length-1]] = fields[i].value;
                    }
                    if (self.dataset.id){
                        data['id'] = self.dataset.id;
                    }
                    return data;
                },

                _init = function(){
                    const data = _getFormData();
                },
                _delete = function() {
                    helpers.ajax({
                        'type': 'POST',
                        'url': '/timeline/delete-moment',
                        'data': JSON.stringify({"id": self.dataset.id}),
                        'callback': function(){
                            if (this.status === 200){
                                self.parentNode.removeChild(self);
                                d.querySelector('[data-edit-timeline]').save();
                            }
                        }
                    });
                },
                _submit = function () {
                    const data = _getFormData();
                    helpers.ajax({
                        'type': 'POST',
                        'url': '/timeline/update-moment',
                        'data': JSON.stringify(data),
                        'callback': function(responseText){
                            const response = JSON.parse(responseText);
                            if (this.status === 201){
                                self.dataset.id = response.message.id;
                                d.querySelector('[data-edit-timeline]').save();
                            }
                            self.dataset.saved = 'saved';
                            clearTimeout(savedTimeout);
                            savedTimeout = setTimeout(function(){
                                delete self.dataset.saved;
                            }, 2000);
                        },
                        'error': function (responseText) {
                            const response = JSON.parse(responseText);
                            if (this.status === 422){
                                for (var k in response.message){
                                    if (response.message.hasOwnProperty(k)){
                                    self.querySelector('[name$="'+ k +'"]').dataset.errorMessage = response.message[k]
                                    }
                                }
                            }

                        }
                    });
                };
            _init();
            self.dataset.editMoment = self;
            self.submit = _submit;
            self.delete = _delete;

        },
        'edit-timeline': function () {
            const self = this,
                momentContainer = self.querySelector('[data-moment-container]'),
                savedMomentQ = '[data-id]',
                momentQ = '[data-moment]',
                _submit = function (data) {
                    helpers.ajax({
                        'type': 'POST',
                        'url': '/timeline/order',
                        'data': JSON.stringify(data)
                    })
                },
                _save = function(){
                    const data = _toArray(momentContainer.querySelectorAll(savedMomentQ)).map(function(e, i){return {'id': e.dataset.id, 'order': i}});
                    _submit(data);
                },
                _order = function(direction, momentElem){
                    const items = _toArray(momentContainer.querySelectorAll(momentQ)),
                        index = items.indexOf(momentElem),
                        nextElem = items[index + direction];
                    if (nextElem){
                        if (direction < 0){
                            _insertAfter(nextElem, momentElem);
                        }else {
                            _insertAfter(momentElem, nextElem);
                        }
                        _save();
                    }
                };
            self.dataset.editTimeline = self;
            self.order = _order;
            self.save = _save;
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
        defaultHeaders = {
          'X-Requested-With': 'XMLHttpRequest',
          'Content-Type': 'application/x-www-form-urlencoded',
          'X-CSRFToken': d.querySelector('input[name="csrfmiddlewaretoken"]').value
        },
        headers = helpers.merge_options(defaultHeaders, options.headers || {});
      request.open(options.type || 'GET', options.url, true);
      for (const k in  headers){
          if (headers.hasOwnProperty(k)){
            request.setRequestHeader(k, headers[k]);
          }
      }
      request.onreadystatechange = function () {
        if (request.readyState === XMLHttpRequest.DONE) {
          if (request.status >= 200 && request.status < 400) {
            if (options.callback && typeof (options.callback) === 'function') {
              options.callback.call(request, request.responseText);
            }

          } else if (request.status === 400) {
                alert('Er ging iets mis.');
          } else {
            if (options.error && typeof (options.error) === 'function') {
              options.error.call(request, request.responseText);
            }
          }
        }
      };
      request.send(options.data);
      return request;
    },
    'merge_options': function(obj1,obj2){
        var obj3 = {};
        for (const attrname1 in obj1) {
            if(obj1.hasOwnProperty(attrname1)){
                obj3[attrname1] = obj1[attrname1];
            }
        }
        for (const attrname2 in obj2) {
            if(obj1.hasOwnProperty(attrname1)) {
                obj3[attrname2] = obj2[attrname2];
            }
        }
        return obj3;
    }
    };

   _decorate();

}(window, document.documentElement);
