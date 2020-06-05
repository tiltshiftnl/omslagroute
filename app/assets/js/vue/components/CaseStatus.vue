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
                Wacht op GGD
            </button>
        </div>
        <!-- <div role="dialog" class="modal" id="modalStatus"> -->
            <div v-if="nextCaseStatus.status">
                <div class="prompt-container show-prompt-approve">
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
        <!-- </div> -->
    </div>
</template>

<script>
import axios from "axios";
import { mapState } from 'vuex';

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
        statusText: {
            2: "Afkeuren",
            3: "Goedkeuren",
            4: "Wachten op GGD",
        },
        buttonText: {
            2: "Aanvraag afkeuren",
            3: "Aanvraag goedkeuren",
            4: "Wachten op GGD",
        },
        buttonClass: {
            2: "u-margin-bottom button button--danger",
            3: "u-margin-bottom button button--success",
            4: "u-margin-bottom button button--warning",
        }
    }),
    computed: {
        ...mapState([
            'case',
            'form',
            'title',
            'caseStatusOptions',
            'emailList',
        ])
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
            this.nextCaseStatus.case = this.$store.state.case.id;
            this.nextCaseStatus.form = this.$store.state.form;
        },
        getCaseStatusList: function () {
            this.loading = true;
            this.nextCaseStatus.status = null;
            axios.get(`/api/casestatus/`)
                .then((response) => {
                    let filtered = response.data.results.filter(status => 
                        Number(status.case) === Number(this.case.id) && 
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
            console.log("nextCaseStatus", this.nextCaseStatus);
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