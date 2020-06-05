<template>
    <Main>
       <Header slot="header"></Header>
       <case-status slot="body"></case-status>
    </Main>
</template>

<script>
import axios from "axios";
import Main from './components/Main.vue'
import Header from './components/Header.vue'
import CaseStatus from './components/CaseStatus.vue'

export default {
    name: "CaseWonen",
    data: () => ({
        'user': {},
    }),  
    methods: {},
    components: {
        Main,
        Header,
        'case-status': CaseStatus,
    },
};
</script>