<template>
    <div>
            <p>
                {{ caseStatusOptions[currentCaseStatus.status].current }}
            </p>
        <div v-if="currentCaseStatus.status === 1">

            <div class="form-field">
                <button v-on:click="setNextStatus(3)" class="button button--success">
                    <svg class="check__icon" width="20" height="16">
                        <use href="#check" xlink:href="#alert" width="20" height="18"></use>
                    </svg>
                    Goedkeuren
                </button>
                <button data-handler="form-disapprove" class="button button--danger">
                    <svg class="close__icon" width="16" height="16">
                        <use href="#close" xlink:href="#close" width="16" height="16"></use>
                    </svg>
                    Afkeuren
                </button>
                <button data-handler="form-pending" class="button button--warning">
                    <svg class="close__icon" width="16" height="16">
                        <use href="#pause" xlink:href="#pause" width="16" height="16"></use>
                    </svg>
                    Wacht op GGD
                </button>
            </div>

        </div>
        <div v-else-if="currentCaseStatus.status === 2">
            <p>
                <svg class="close__icon" width="16" height="16">
                    <use href="#close" xlink:href="#close" width="16" height="16"></use>
                </svg>
                Afgekeurd

            </p>
            <div class="form-field">
                <button data-handler="form-approve" class="button button--secondary button--success">
                    <svg class="check__icon" width="20" height="16">
                        <use href="#check" xlink:href="#alert" width="20" height="18"></use>
                    </svg>
                    Goedkeuren
                </button>
                <button data-handler="form-pending" class="button  button--secondary button--warning">
                    <svg class="pause__icon" width="16" height="16">
                        <use href="#pause" xlink:href="#pause" width="16" height="16"></use>
                    </svg>
                    Wacht op GGD
                </button>
            </div>
        </div>
        <div v-else-if="currentCaseStatus.status === 3">
            <p>
                <svg class="check__icon" width="20" height="16">
                    <use href="#check" xlink:href="#alert" width="20" height="18"></use>
                </svg>
                Goedgekeurd
            </p>
            <div class="form-field">
                <button data-handler="form-disapprove" class="button button--secondary button--danger">
                    <svg class="close__icon" width="16" height="16">
                        <use href="#close" xlink:href="#close" width="16" height="16"></use>
                    </svg>
                    Afkeuren
                </button>
                <button data-handler="form-pending" class="button  button--secondary button--warning">
                    <svg class="close__icon" width="16" height="16">
                        <use href="#pause" xlink:href="#pause" width="16" height="16"></use>
                    </svg>
                    Wacht op GGD
                </button>
            </div>
        </div>
         <div v-if="nextCaseStatus.status">
            <div class="prompt-container show-prompt-approve" data-handler="prompt-approve">
                <div v-if="nextCaseStatus.status === 3">
                    <div class="prompt-approve">
                        <p>Weet je zeker dat je deze <strong>{{ title }}</strong> wilt goedkeuren?</p>
                        <p><strong>[e-mail]</strong> ontvangt hiervan een bevestiging per e-mail.</p>
                        <form>
                            <button type="button" class="button button--primary"  v-on:click="addCaseStatus()">Aanvraag goedkeuren</button>
                            <button type="button" class="button button--secondary" v-on:click="setNextStatus(null)">Annuleren</button>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import axios from "axios";

export default {
    name: "CaseStatus",
    data: () => ({
        loading: false,
        currentCaseStatus: {'status': 1},
        nextCaseStatus: {
            'status': 0,
            'form': null,
            'case': null,
        },
        caseStatusOptions: {},
        title: null,
        caseId: null,
        form: null,
        message: null,
        newCaseStatus: {
            'status': null,
            'status_comment': null,
            'form': null,
            'case': null,
            'caseversion': null,
            'profile': null,
        },
        statusText: {
            2: "Weet je zeker dat je deze <strong>Title</strong> wilt afkeuren?",
            3: "Weet je zeker dat je deze <strong>Title</strong> wilt goedkeuren?",
            4: "Weet je zeker dat je de status van deze <strong>Title</strong> op 'Wacht op GGD' wilt zetten?",
        }
        
    }),
    computed: {
        promptClass: function () {
            const classes = {0: 'hide', 2: 'disapprove', 3: 'approve', 4: 'pending'}
            return 'prompt-container show-prompt-' + this.nextCaseStatus.status
        }
    },
    beforeMount(){
        this.getInitialData()
    },
    created() {
        // shows empty array
        console.log(this.cases)
        this.getCaseStatusList();
    },
    methods: {
        setNextStatus: function(status){
            this.nextCaseStatus.status = status;
        },
        getInitialData: function(){
            this.caseId = document.querySelector('[data-case-id]').dataset.caseId;
            this.form = document.querySelector('[data-form]').dataset.form;
            this.title = document.querySelector('[data-title]').dataset.title;
            this.caseStatusOptions = JSON.parse(document.querySelector('[data-case-status-options]').dataset.caseStatusOptions);
            this.nextCaseStatus.case = this.caseId;
            this.nextCaseStatus.form = this.form;
        },
        getCaseStatusList: function (caseId, form) {
            this.loading = true;
            this.nextCaseStatus.status = null;
            axios.get(`/api/casestatus/`)
                .then((response) => {
                    let filtered = response.data.results.filter(status => 
                        Number(status.case) === Number(this.caseId) && 
                        status.form === this.form
                    )
                    this.currentCaseStatus = filtered[0] || {'status': 1};
                    this.loading = false;
                })
                .catch((err) => {
                    this.loading = false;
                    console.log(err);
                })
        },
        addCaseStatus: function () {
            this.loading = true;
            console.log(this.nextCaseStatus);
            axios.post(`/api/casestatus/`, this.nextCaseStatus)
                .then((response) => {
                    this.loading = false;
                    this.getCaseStatusList();
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