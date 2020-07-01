'use strict';

import Vue from "vue";
import Case from "./vue/Case.vue";
import axios from "axios";

const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').getAttribute('value');

axios.defaults.headers.post['X-CSRFToken'] = csrfToken;
axios.defaults.headers.put['X-CSRFToken'] = csrfToken;
axios.defaults.headers.delete['X-CSRFToken'] = csrfToken;
Vue.use(require('vue-moment'));

new Vue({
 el: "#app",
 render: h => h(Case)
});