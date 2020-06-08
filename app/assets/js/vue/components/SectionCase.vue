<template>
<section class="section section--client">
    <h1>{{ caseObject.client_name }}</h1>
    <h2 class="h3">{{ form }}</h2>
    <p class="print-only">
    </p>


    <section class="section-details-client">

        <!-- START BIJLAGE -->
        <div class="details-client details-client--appendix u-width-50">
            <document-list></document-list>
        </div>

        <div class="details-client details-client--approve u-width-50">
            <case-status></case-status>
        </div>
        <!-- END BIJLAGE -->
        

    </section>
    <section class="section section--forms">
        <!-- START Client basis gegevens -->
        <div class="details-client">
            <header>
                <h2 class="h3">Gegevens</h2>
            </header>

            <dl>

            </dl>
        </div>
        <!-- END Client basis gegevens -->

    </section>
</section>
</template>

<script>
import CaseStatus from './CaseStatus.vue'
import DocumentList from './DocumentList.vue'
import { mapState } from 'vuex';

export default {
    name: "SectionCase",
    data: () => ({}),
    computed: {
        ...mapState([
            'caseObject',
            'form',
        ])
    },
    components: {
        'document-list': DocumentList,
        'case-status': CaseStatus,
    },
    methods: {}
};
</script>