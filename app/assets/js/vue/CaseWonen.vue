<template>
    <main-component>
       <header-component slot="header"></header-component>
       <section-case slot="body"></section-case>
    </main-component>
</template>

<script>
import axios from "axios";
import Main from './components/Main.vue'
import Header from './components/Header.vue'
import SectionCase from './components/SectionCase.vue'



export default {
    name: "CaseWonen",
    // data: () => ({}), 
    mounted(){
        // this.$store.dispatch('GET_USER')
        // this.$store.dispatch('GET_CASE')
        // this.$store.dispatch('GET_STATUS_OPTIONS')
        // this.$store.dispatch('GET_FORM')
        // this.$store.dispatch('GET_EMAIL_LIST')
    } ,
    methods: {},
    components: {
        'main-component': Main,
        'header-component': Header,
        'section-case': SectionCase,
    },
};
</script>