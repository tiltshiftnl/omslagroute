import ComponentA from './ComponentA.vue'

<template>
<div class="site-container">
    <slot name="header"/>
    <!-- <menu></menu> -->
    <!-- <messages></messages> -->



    <main role="main" class="site-main">
        <div class="print-only print-header" aria-hidden="true">
            <img src="{% static 'images/logo.svg' %}" class="print-logo">
        </div>
        <!-- <breadcrumb></breadcrumb> -->
        <slot name="breadcrumb"/>
        <slot name="body"/>
        <slot name="feedback"/>

        <!-- <feedback></feedback> -->

    </main>
    
</div>
</template>

<script>
import axios from "axios";
import { mapGetters } from 'vuex';

export default {
    name: "Main",
    data: () => ({ }),
    computed: {
        ...mapGetters([
        // 'user'
        ])
    },
    methods: {}
};
</script>