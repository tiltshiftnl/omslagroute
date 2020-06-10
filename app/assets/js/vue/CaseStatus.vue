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
                    <use href="#check" xlink:href="#check" width="20" height="18"></use>
                </svg>
            </span>
            <span v-if="currentCaseStatus.status === 4">
                <svg class="pause__icon" width="12" height="16">
                    <use href="#pause" xlink:href="#pause" width="12" height="16"></use>
                </svg>
            </span>
            <span>{{ caseStatusOptions[currentCaseStatus.status].current }}</span>
        </p>
        <div class="form-field">
            <button v-if="currentCaseStatus.status !== 3" 
            v-on:click="setNextStatus(3)"  v-bind:class="setButtonClass(3)">
                <svg class="check__icon" width="20" height="16">
                    <use href="#check" xlink:href="#alert" width="20" height="18"></use>
                </svg>
                Goedkeuren
            </button>
            <button v-if="currentCaseStatus.status !== 2" 
                v-on:click="setNextStatus(2)" v-bind:class="setButtonClass(2)">
                <svg class="close__icon" width="16" height="16">
                    <use href="#close" xlink:href="#close" width="16" height="16"></use>
                </svg>
                Afkeuren
            </button>
            <button v-if="currentCaseStatus.status !== 4" 
                v-on:click="setNextStatus(4)" v-bind:class="setButtonClass(4)">
                <svg class="close__icon" width="12" height="16">
                    <use href="#pause" xlink:href="#pause" width="12" height="16"></use>
                </svg>
                In behandeling
            </button>
        </div>
        <div v-if="nextCaseStatus.status" class="container-modal--vue">
            <a href="#" class="modal-close--bg" v-on:click="setNextStatus(null)" ></a>
            <div class="prompt-container show-prompt-approve" data-handler="prompt-approve">
                <button v-on:click="setNextStatus(null)" class="button button--close">
                    <svg width="20" height="20" title="Sluit venster">
                        <use href="#close" xlink:href="#close" width="20" height="20"></use>
                    </svg>
                    <span class="sr-only">Sluit venster</span>
                </button>
                <h2>Status wijzigen</h2>
                <div class="prompt-approve">
                    <p>Weet je zeker dat je de status voor <strong>{{ title }}</strong> wilt wijzigen naar <strong>{{ statusText[nextCaseStatus.status] }}</strong>?</p>
                    <p><strong>{{ emailList }}</strong> ontvangt hiervan een bevestiging per e-mail.</p>
                    <form>
                        <div class="form-field form-field--textarea screen-only u-margin-top-2x">
                            <label for="status-message">Bericht (optioneel)</label>
                            <textarea v-model="nextCaseStatus.status_comment" id="status-message" name="status-message" cols="40" rows="4"></textarea>
                        </div>
                        <span class="helptext">Als je een bericht wil meesturen met in de bevestings e-mail, dan kun je dat hier doen.</span>
                        <div class="form-field form-field--buttons screen-only u-margin-top-2x">
                            <button type="button" class="button button--primary"  v-on:click="addCaseStatus()">{{ buttonText[nextCaseStatus.status] }}</button>
                            <button type="button" class="button button--secondary" v-on:click="setNextStatus(null)" data-handler="modal-close">Annuleren</button>
                        </div>
                    </form>
                </div>

            </div>
        </div>
        <div class="status-history-container form-field-history">
            <details>
                <summary>Statushistorie<svg class="icon-details--closed" width="14" height="9">
                        <use href="#chevron-down" xlink:href="#chevron-down" width="14" height="9"></use>
                    </svg><svg class="icon-details--open" width="14" height="9">
                        <use href="#chevron-up" xlink:href="#chevron-up" width="14" height="9"></use>
                    </svg>
                </summary>
                <div class="content">
                    <ul class="u-list-style-none">
                        <li v-for="h in statusHistory" :key="h.id">
                            <div>
                                <small class="facts">
                                    {{ h.created | luxon }}<br/>
                                    {{ h.username }}
                                </small>
                                <small class="status">{{caseStatusOptions[h.status].current }}</small>
                            </div>
                        </li>
                    </ul>
                </div>
            </details>
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
            'status_comment': null,
            'caseversion': null,
        },
        statusHistory: [],
        caseStatusOptions: {},
        title: null,
        caseId: null,
        form: null,
        message: null,
        emailList: null,
        statusText: {
            2: "Afkeuren",
            3: "Goedkeuren",
            4: "In behandeling",
        },
        buttonText: {
            2: "Aanvraag afkeuren",
            3: "Aanvraag goedkeuren",
            4: "In behandeling",
        },
        buttonClass: {
            2: "u-margin-bottom button button--danger",
            3: "u-margin-bottom button button--success",
            4: "u-margin-bottom button button--warning",
        },
    }),
    computed: {
    },
    beforeMount(){
        console.log("beforeMount");
        this.getInitialData();
    },
    created() {
        console.log("created");
        this.getCaseStatusList();
    },
    methods: {
        setButtonClass: function(status){
            return (this.buttonClass[status] + (this._data.currentCaseStatus.status !== 1 ? ' button--secondary': ''));
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
                    filtered.shift();
                    this.statusHistory = filtered;
                    this.loading = false;
                })
                .catch((err) => {
                    this.loading = false;
                    console.log(err);
                })
        },
        addCaseStatus: function () {
            this.loading = true;
            axios.post(`/api/casestatus/`, this.nextCaseStatus)
                .then((response) => {
                    this.loading = false;
                    this.nextCaseStatus.status_comment = null;
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