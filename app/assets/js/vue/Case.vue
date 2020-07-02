<template>
    <div v-bind:class="setFormClass()">
        <!-- <div class="u-padding-top u-clearfix">
            <a href="#" role="button" data-handler="show-target" class="u-float-right u-underline--none screen-only" title="Voeg een nieuwe bijlage toe">
                + <span class="u-underline">Dossier nr</span>
            </a>
        </div> -->
        <!-- wonen && dossiernummer -->
        <div v-if="!enableUpdate && !initial" class="u-padding-top u-clearfix">
            <span>Dossier nr: <strong>{{ caseDossierNr }}</strong>&nbsp;</span>
            <a v-on:click="setEnableUpdate(true)" href="#" role="button" class="u-float-right u-underline--none screen-only" title="Voeg een nieuwe bijlage toe">
                (wijzig)
            </a>
        </div>
        <div v-if="enableUpdate && !initial" class="case-number">
            <form>
                <div>
                    <label for="input_casenumber">Dossier nr</label>
                    <input v-model="caseDossierNr" type="text" placeholder="123456" id="input_casenumber" />
                    <button v-on:click="updateCaseDossierNr()" type="submit" class="button button--primary">Sla op</button>
                </div>
            </form>
        </div>
    </div>  
</template>

<script>
import axios from "axios";

export default {
    name: "Case",
    data: () => ({
        caseDossierNr: null,
        caseId: null,
        enableUpdate: false,
        error: false,
        initial: true,
    }),
    created() {
        this.getInitialData();
        this.getCaseDossierNr(true);
    },
    beforeMount(){
    },
    methods: {
        setFormClass: function(){
            return this.error && 'error';
        },
        setEnableUpdate: function(enable){
            this.enableUpdate = enable;
        },
        getInitialData: function(){
            this.caseId = document.querySelector('[data-case-id]').dataset.caseId;
        },
        getCaseDossierNr: function () {
            axios.get(`/api/case-dossier-nr/${this.caseId}/`)
                .then((response) => {
                    this.caseDossierNr = response.data.wonen_dossier_nr;
                    this.enableUpdate = !this.caseDossierNr;
                    this.initial = false;
                })
                .catch((err) => {
                    console.log(err);
                })
        },
        updateCaseDossierNr: function () {
            axios.put(`/api/case-dossier-nr/${this.caseId}/`, {'wonen_dossier_nr': this.caseDossierNr})
                .then((response) => {
                    this.getCaseDossierNr();
                    this.error = !this.caseDossierNr;
                })
                .catch((err) => {
                    console.log(err);
                })
        },
    }
};
</script>