<template>
    <header class="site-header screen-only">
        <div class="site-header-wrapper">
            <a href="/" title="Ga terug naar de homepage">
                <img src="/static/images/logo.svg" alt="Gemeente Amsterdam" class="logo">
            </a>
            <h1 class="site-title">
                <a href="/" title="Ga terug naar de homepage">
                    Omslagroute
                </a>
            </h1>

            <div class="site-userinfo">
                <p>
                    <a href="" class="site-userinfo__username">
                        Ingelogd als: {{ user.username }}
                    </a> |
                </p>
                <a href="/">Uitloggen</a>
            </div>
        </div>
    </header>
</template>

<script>
import axios from "axios";
import { mapGetters, mapActions, mapState } from 'vuex'

export default {
    name: "Header",
    // data: () => ({ }),
    computed: {
        ...mapState([
        'user'
        ]),
    },
    methods: {}
};
</script>