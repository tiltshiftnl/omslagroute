<template>

</template>

<script>
import axios from "axios";

export default {
    name: "CaseStatus",
    data: () => ({
        loading: false,
        currentCase: {},
        message: null,
        newCase: {
            'status': null,
            'status_comment': null,
            'form': null,
            'case': null,
            'caseversion': null,
            'profile': null,
        },
    }),
    created() {
        // shows empty array
        console.log(this.cases)
        this.getCaseStatus();
        $("#addCaseModal").modal('show');
    },
    methods: {
        getCaseStatus: function (caseId, form) {
            this.loading = true;
            axios.get(`/api/casestatus/${caseId}/`)
                .then((response) => {
                    console.log(response.data);
                    this.currentCaseStatus = response.data;
                    $("#addCaseStatusModal").modal('show');
                    this.loading = false;
                })
                .catch((err) => {
                    this.loading = false;
                    console.log(err);
                })
        },
        addCaseStatus: function () {
            this.loading = true;
            axios.post(`/api/casestatus/`, this.newCaseStatus)
                .then((response) => {
                    this.loading = false;
                    this.addCaseStatus();
                })
                .catch((err) => {
                    this.loading = false;
                    console.log(err);
                })
        },
    }
};
</script>

<style lang="css">

</style>