'use strict';

import Vue from "vue";
import CaseStatus from "./vue/CaseStatus.vue";
import axios from "axios";
import VueLuxon from "vue-luxon";

const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').getAttribute('value');

axios.defaults.headers.post['X-CSRFToken'] = csrfToken;
axios.defaults.headers.put['X-CSRFToken'] = csrfToken;
axios.defaults.headers.delete['X-CSRFToken'] = csrfToken;

Vue.use(VueLuxon, {
    serverZone: 'utc',
    serverFormat: 'iso',
    clientZone: 'Europe/Amsterdam',
    clientFormat: 'locale',
    localeLang: 'nl-NL',
    localeFormat: {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: 'numeric',
        minute: 'numeric'
    }, // see localeFormat below
    diffForHumans: {}, // see diffForHumans below
    i18n: {
        lang: "nl-NL",
        year: "[one]jaar|[other]jaren",
        month: "[one]maand|[other]maanden",
        week: "[one]week|[other]weken",
        day: "[one]dag|[other]dagen",
        hour: "[one]uur|[other]uren",
        minute: "[one]minuut|[other]minuten",
        second: "[one]seconde|[other]seconden",
        ago: 'geleden',
        in: 'over',
    } // see i18n below
});

new Vue({
 el: "#app",
 render: h => h(CaseStatus)
});