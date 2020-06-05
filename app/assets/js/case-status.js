'use strict';

import Vue from "vue";
import Vuex from 'vuex';
import CaseWonen from "./vue/CaseWonen.vue";
import axios from "axios";
import { store } from './store.js';

const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').getAttribute('value');

axios.defaults.headers.post['X-CSRFToken'] = csrfToken;
axios.defaults.headers.put['X-CSRFToken'] = csrfToken;
axios.defaults.headers.delete['X-CSRFToken'] = csrfToken;

Vue.use(Vuex)

new Vue({
    store,
    el: "#app",
    render: h => h(CaseWonen)
});