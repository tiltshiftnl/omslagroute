import ComponentA from './ComponentA.vue'

<template>
<div class="site-container">
    <header></header>
    <menu></menu>
    <messages></messages>



    <main role="main" class="site-main">
        <div class="print-only print-header" aria-hidden="true">
            <img src="{% static 'images/logo.svg' %}" class="print-logo">
        </div>
        <breadcrumb></breadcrumb>


        <feedback></feedback>

    </main>
    
</div>
</template>

<script>
import axios from "axios";

export default {
    name: "Main",
    data: () => ({ }),
    methods: {}
};
</script>