<template>
    <div>
        <header>
            <h2 class="h3">Bijlagen <small>({{ documentList.length }})</small></h2>
        </header>
        <ul class="list-as-table">
            <li v-for="document in documentList" :key="document.id">
                <div>
                    <a :href="document.url" target="_blank">
                        <span>{{ document.name }}</span>
                    </a>
                    <span>{{ document.extension }}</span>
                    <span>{{ document.uploaded }}</span>
                </div>
            </li>
        </ul>
    </div>
</template>

<script>
import axios from "axios";
import { mapState } from 'vuex'

export default {
    name: "DocumentList",
    computed: {
        ...mapState([
        'documentList'
        ]),
    },
    methods: {}
};
</script>