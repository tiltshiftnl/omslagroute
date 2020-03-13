var fileUpload = document.getElementById('file-upload');
var filesUploaded = document.getElementById( 'file-upload-filename' );

if (fileUpload && fileUpload.addEventListener) {
    fileUpload.addEventListener('change', showFileName);
}

function showFileName( event ) {
    var input = event.srcElement;
    var fileName = input.files[0].name;
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
          var moment = _closest(e.target, '[data-moment]');
         _closest(e.target, '[data-edit-timeline]').order(-1, moment);
      },
      'moment-down': function (e) {
          e.preventDefault();
          var moment = _closest(e.target, '[data-moment]');
         _closest(e.target, '[data-edit-timeline]').order(1, moment);

      },
      'new-moment': function (e) {
          e.preventDefault();
          var self = _closest(e.target, '[data-handler="new-moment"]');
          var moment = _closest(e.target, '[data-id]'),
              momentListContainer = moment.parentNode,
              proto = d.querySelector('[data-moment-proto]').cloneNode(true);
          _insertAfter(proto, moment);
          momentListContainer.classList.add('edit-mode');
          self.style.display = 'none';
          proto.style.display = 'block';
          proto.dataset.decorator = 'edit-moment';
          proto.querySelector('input').focus();
          _decorate();
      },
      'exit-new-moment': function (e) {
          e.preventDefault();
          var self = _closest(e.target, '[data-handler="exit-new-moment"]'),
              moment = _closest(self, '[data-moment]'),
              prevMoment  = moment.previousSibling,
              momentListContainer = moment.parentNode,
              new_moment_button = moment.previousSibling.querySelector('[data-handler="new-moment"]');
          prevMoment.querySelector('[data-handler="new-moment"]').style.display = 'block';
          moment.parentElement.removeChild(moment);
          momentListContainer.classList.remove('edit-mode');
      },
      'delete-moment': function(e){
          e.preventDefault();
          var self = _closest(e.target, '[data-handler="delete-moment"]'),
              container = _closest(self, '[data-edit-moment]');

          if (confirm("Weet je zeker dat je het timeline item met naam '"+container.querySelector('[name$="name"]').value+"' wil verwijderen")) {
              if (!container.dataset.id) {
                  container.parentNode.removeChild(container);
              } else {
                  container.delete();
              }
          }
      },
      'exit-edit-moment': function(e){
          e.preventDefault();
          var self = _closest(e.target, '[data-handler="exit-edit-moment"]'),
              moment = _closest(e.target, '[data-moment]'),
              momentListContainer = moment.parentNode;
          momentListContainer.classList.remove('edit-mode');
          moment.classList.remove('edit-mode');

      },
      'enter-edit-moment': function(e){
          e.preventDefault();
          var self = _closest(e.target, '[data-handler="enter-edit-moment"]'),
              moment = _closest(e.target, '[data-moment]'),
              momentListContainer = moment.parentNode;
          momentListContainer.classList.add('edit-mode');
          moment.classList.add('edit-mode');
          moment.querySelector('input').focus();
      },
      'open-moment': function(e){
          var self = _closest(e.target, '[data-handler="open-moment"]'),
            moment = _closest(self, '[data-moment]'),
            details = moment.querySelector('details'),
            momentListContainer = moment.parentNode,
            buttons = momentListContainer.querySelectorAll('.change-order button, .new-moment__add');
          //momentListContainer.classList[details.hasAttribute('open') ? 'remove' : 'add']('edit-mode');
          if (momentListContainer.classList.contains('edit-mode')){
              e.preventDefault();
          }

      },
      'save-moment': function(e){
          e.preventDefault();
          var self = _closest(e.target, '[data-handler="save-moment"]'),
            moment = _closest(self, '[data-moment]'),
            exitEditElem = moment.querySelector('[data-handler="exit-edit-moment"]');
          moment.submit(function(){
              exitEditElem.click();
          });

    }
  };
    var decorators = {
        'edit-moment': function () {
            var savedTimeout;
            var savingTimeout;
            var self = this,
                id = this.dataset.id,
                _getFormData = function () {
                    var data = {},
                        i,
                        fields = self.querySelectorAll('input[type="text"], input[type="hidden"], textarea');
                    for (i = 0; i < fields.length; i++){
                        var nameSplit = fields[i].getAttribute('name').split('-');
                        data[nameSplit[nameSplit.length-1]] = fields[i].value;
                    }
                    if (self.dataset.id){
                        data['id'] = self.dataset.id;
                    }
                    return data;
                },
                _updateView = function(data){
                    for (var k in data){
                        if (data.hasOwnProperty(k)) {
                            var elem = self.querySelectorAll('[data-moment-'+k+']');
                            for (var i = 0; i < elem.length; i++){
                                elem[i].innerHTML = data[k].replace(/(?:\r\n|\r|\n)/g, '<br>');
                            }
                        }
                    }
                },
                _clearErrorMessages = function(){
                    var elems = self.querySelectorAll('[data-error-message]');
                    for (var i = 0; i < elems.length; i++){
                        delete elems[i].dataset.errorMessage;
                    }
                },
                _init = function(){
                    var isNewElement = self.classList.contains('details-wrapper--new-moment'),
                        firstElement = self.querySelector('input[name$="name"]'),
                        lastElement = isNewElement ? self.querySelector('button[data-handler="exit-new-moment"]') : self.querySelector('button[data-handler="exit-edit-moment"]');

                    lastElement.addEventListener('keydown', function(e){
                        if( e.keyCode === 9 ) {
                            firstElement.focus();
                            e.preventDefault();
                        }
                    });
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
                _submit = function (_callback) {
                    var data = _getFormData();
                    self.dataset.saving = 'saving';
                    clearTimeout(savingTimeout);
                    savingTimeout = setTimeout(function(){
                        delete self.dataset.saving;
                    }, 2000);
                    helpers.ajax({
                        'type': 'POST',
                        'url': '/timeline/update-moment',
                        'data': JSON.stringify(data),
                        'callback': function(responseText){
                            var response = JSON.parse(responseText);
                            if (this.status === 201){
                                self.dataset.id = response.message.id;
                                self.classList.remove('details-wrapper--new-moment');
                                delete self.dataset.momentProto;
                                d.querySelector('[data-edit-timeline]').save();
                            }
                            if (self.previousSibling.classList) {
                                self.previousSibling.querySelector('[data-handler="new-moment"]').style.display = 'block';
                            }
                            self.dataset.saved = 'saved';
                            _updateView(response.message);
                            _clearErrorMessages();
                            clearTimeout(savedTimeout);
                            if (_callback && typeof (_callback) === 'function'){
                              _callback();
                            }
                            savedTimeout = setTimeout(function(){
                                delete self.dataset.saved;
                            }, 2000);
                        },
                        'error': function (responseText) {
                            var response = JSON.parse(responseText);
                            if (this.status === 422) {
                                for (var k in response.message) {
                                    if (response.message.hasOwnProperty(k)) {
                                        self.querySelector('[name$="' + k + '"]').dataset.errorMessage = response.message[k]
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
            var self = this,
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
                    var data = _toArray(momentContainer.querySelectorAll(savedMomentQ)).map(function(e, i){return {'id': e.dataset.id, 'order': i}});
                    _submit(data);
                },
                _order = function(direction, momentElem){
                    var items = _toArray(momentContainer.querySelectorAll(momentQ)),
                        index = items.indexOf(momentElem),
                        nextElem = items[index + direction];
                    if (nextElem) {
                        var currentClone = momentElem.cloneNode(true);
                        var nextClone = nextElem.cloneNode(true);
                        var currentRect = momentElem.getBoundingClientRect();
                        var nextRect = nextElem.getBoundingClientRect();
                        var parentRect = nextElem.parentNode.getBoundingClientRect();
                        nextElem.style.opacity = 0;
                        momentElem.style.opacity = 0;
                        currentClone.style.position = 'absolute';
                        currentClone.style.width = momentElem.offsetWidth + 'px';
                        currentClone.style.height = momentElem.offsetHeight + 'px';
                        currentClone.style.top = (currentRect.top - parentRect.top) + 'px';
                        currentClone.style.transition = 'all .5s cubic-bezier(0.165, 0.84, 0.44, 1)';
                        currentClone.style.zIndex = 1001;

                        nextClone.style.position = 'absolute';
                        nextClone.style.width = momentElem.offsetWidth + 'px';
                        nextClone.style.height = momentElem.offsetHeight + 'px';
                        nextClone.style.top = (nextRect.top - parentRect.top) + 'px';
                        nextClone.style.transition = 'all .5s cubic-bezier(0.165, 0.84, 0.44, 1)';
                        nextClone.style.zIndex = 1000;

                        momentElem.parentNode.appendChild(currentClone);
                        momentElem.parentNode.appendChild(nextClone);

                        setTimeout(function () {
                            currentClone.style.transform = 'translate(0, ' + (direction * nextElem.offsetHeight) + 'px)';
                            nextClone.style.transform = 'translate(0, ' + (-direction * momentElem.offsetHeight) + 'px)';
                        }, 1);
                        setTimeout(function () {
                            currentClone.parentNode.removeChild(currentClone);
                            nextClone.parentNode.removeChild(nextClone);
                            nextElem.style.opacity = 1;
                            momentElem.style.opacity = 1;
                            if (direction < 0) {
                                _insertAfter(nextElem, momentElem);
                            } else {
                                _insertAfter(momentElem, nextElem);
                            }
                            _save();
                        }, 500);
                    }
                };
            self.dataset.editTimeline = self;
            self.order = _order;
            self.save = _save;
        },
        'timeline-sort': function () {
            var self = this,
                momentFormList = self.querySelectorAll('[data-moment]'),
                _init = function (items) {
                    var momentContainer = items[0].parentNode;
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
                    var index = items.indexOf(momentElem),
                        currentOrder = momentElem.dataset.order,
                        nextElem = items[index + direction];
                    if (nextElem){
                        momentElem.dataset.order = nextElem.dataset.order;
                        nextElem.dataset.order = currentOrder;
                        momentElem.style.order = momentElem.dataset.order;
                        nextElem.style.order = nextElem.dataset.order;
                    }
                },
                _submit = function(){
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
      for (var k in  headers){
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
        for (var attrname1 in obj1) {
            if(obj1.hasOwnProperty(attrname1)){
                obj3[attrname1] = obj1[attrname1];
            }
        }
        for (var attrname2 in obj2) {
            if(obj1.hasOwnProperty(attrname1)) {
                obj3[attrname2] = obj2[attrname2];
            }
        }
        return obj3;
    }
    };

   _decorate();

}(window, document.documentElement);
