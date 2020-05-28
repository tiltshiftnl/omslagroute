<template>
    <div>
            <header>
                <h2 class="h3">Status aanvraag</h2>
            </header>
        <p>
            <span v-if="currentCaseStatus.status === 2">
                <svg class="close__icon" width="16" height="16">
                    <use href="#close" xlink:href="#close" width="16" height="16"></use>
                </svg>
            </span>
            <span v-if="currentCaseStatus.status === 3">
                <svg class="check__icon" width="20" height="16">
                    <use href="#check" xlink:href="#alert" width="20" height="18"></use>
                </svg>
            </span>
            <span>{{ caseStatusOptions[currentCaseStatus.status].current }}</span>
        </p>
        <div class="form-field">
            <button v-if="currentCaseStatus.status === 1 || currentCaseStatus.status === 2 || currentCaseStatus.status === 4" 
            v-on:click="setNextStatus(3)"  v-bind:class="setButtonClass(3)">
                <svg class="check__icon" width="20" height="16">
                    <use href="#check" xlink:href="#alert" width="20" height="18"></use>
                </svg>
                Goedkeuren
            </button>
            <button v-if="currentCaseStatus.status === 1 || currentCaseStatus.status === 3 || currentCaseStatus.status === 4" 
                v-on:click="setNextStatus(2)" v-bind:class="setButtonClass(2)">
                <svg class="close__icon" width="16" height="16">
                    <use href="#close" xlink:href="#close" width="16" height="16"></use>
                </svg>
                Afkeuren
            </button>
            <button v-if="currentCaseStatus.status === 1 || currentCaseStatus.status === 2 || currentCaseStatus.status === 3" 
                v-on:click="setNextStatus(4)" v-bind:class="setButtonClass(4)">
                <svg class="close__icon" width="16" height="16">
                    <use href="#pause" xlink:href="#pause" width="16" height="16"></use>
                </svg>
                Wacht op GGD
            </button>
        </div>
         <div v-if="nextCaseStatus.status">
            <div class="prompt-container show-prompt-approve" data-handler="prompt-approve">
                <div class="prompt-approve">
                    <p v-if="nextCaseStatus.status === 2">Weet je zeker dat je deze <strong>{{ title }}</strong> wilt afkeuren?</p>
                    <p v-if="nextCaseStatus.status === 3">Weet je zeker dat je deze <strong>{{ title }}</strong> wilt goedkeuren?</p>
                    <p v-if="nextCaseStatus.status === 4">Weet je zeker dat je de status van deze <strong>{{ title }}</strong> op 'Wacht op GGD' wilt zetten?</p>
                    <p><strong>{{ emailList }}</strong> ontvangt hiervan een bevestiging per e-mail.</p>
                    <form>
                        <button type="button" class="button button--primary"  v-on:click="addCaseStatus()">{{ buttonText[nextCaseStatus.status] }}</button>
                        <button type="button" class="button button--secondary" v-on:click="setNextStatus(null)">Annuleren</button>
                    </form>
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
        emailList: null,
        newCaseStatus: {
            'status': null,
            'status_comment': null,
            'form': null,
            'case': null,
            'caseversion': null,
            'profile': null,
        },
        buttonText: {
            2: "Aanvraag afkeuren",
            3: "Aanvraag goedkeuren",
            4: "Wachten op GGD",
        },
        buttonClass: {
            2: "button button--danger",
            3: "button button--success",
            4: "button button--warning",
        }
        
    }),
    computed: {
    },
    beforeMount(){
        this.getInitialData();
    },
    created() {
        this.getCaseStatusList();
    },
    methods: {
        setButtonClass: function(status){
            return this.buttonClass[status] + (status === 1 ? ' button--secondary': '');
        },
        setNextStatus: function(status){
            this.nextCaseStatus.status = status;
        },
        getInitialData: function(){
            this.caseId = document.querySelector('[data-case-id]').dataset.caseId;
            this.form = document.querySelector('[data-form]').dataset.form;
            this.title = document.querySelector('[data-title]').dataset.title;
            this.emailList = document.querySelector('[data-email-list]').dataset.emailList;
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