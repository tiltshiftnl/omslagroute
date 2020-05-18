<template>
<div>
    <div class="container">
        <div class="row">
            <h1>List of Cases
                <button class="btn btn-success" data-toggle="modal" data-target="#addCaseModal">ADD CASE</button>
            </h1>
            <table class="table">
                <thead>
                    <tr>
                        <th scope="col">#</th>
                        <th scope="col">Heading</th>
                        <th scope="col">Action</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="caseItem in cases.results" v-bind:key="caseItem.id">
                        <th scope="row">{{ caseItem.id }}</th>
                        <td>
                            {{ caseItem.client_first_name }}</td>
                        <td>
                            <button class="btn btn-info" v-on:click="getCase(caseItem.id)">Edit</button>
                            <button class="btn btn-danger" v-on:click="deleteCase(caseItem.id)">Delete</button>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
    <div class="loading" v-if="loading===true">Loading&#8230;</div>

    <div class="modal fade" id="addCaseModal" tabindex="-1" role="dialog" aria-labelledby="exampleModalLongTitle" aria-hidden="true">
        <div class="modal-dialog" role="document">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title" id="exampleModalLongTitle">ADD Case</h5>
                    <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                        <span aria-hidden="true">&times;</span>
                    </button>
                </div>
                <form v-on:submit.prevent="addCase()">
                    <div class="modal-body">
                        <div class="form-group">
                            <label for="client_first_name">Case first name</label>
                            <input type="text" class="form-control" id="client_first_name" placeholder="Enter Case first name" v-model="newCase.client_first_name" required="required">
                        </div>
                        <div class="form-group">
                            <label for="client_last_name">Case last name</label>
                            <textarea class="form-control" id="client_last_name" placeholder="Enter Case last name" v-model="newCase.client_last_name" required="required" rows="3"></textarea>
                        </div>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
                        <button type="submit" class="btn btn-primary">Save changes</button>
                    </div>
                </form>
            </div>
        </div>
        <div class="loading" v-if="loading===true">Loading&#8230;</div>
    </div>

    <div class="modal fade" id="editCaseModal" tabindex="-1" role="dialog" aria-labelledby="exampleModalLongTitle" aria-hidden="true">
        <div class="modal-dialog" role="document">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title" id="exampleModalLongTitle">EDIT Case</h5>
                    <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                        <span aria-hidden="true">&times;</span>
                    </button>
                </div>
                <form v-on:submit.prevent="updateCase()">
                    <div class="modal-body">
                        <div class="form-group">
                            <label for="client_first_name">Case first name</label>
                            <input type="text" class="form-control" id="client_first_name" placeholder="Enter Case first name" v-model="currentCase.client_first_name" required="required">
                        </div>
                        <div class="form-group">
                            <label for="client_last_name">Case last name</label>
                            <textarea class="form-control" id="client_last_name" placeholder="Enter Case last name" v-model="currentCase.client_last_name" required="required" rows="3"></textarea>
                        </div>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary m-progress" data-dismiss="modal">Close</button>
                        <button type="submit" class="btn btn-primary">Save changes</button>
                    </div>
                </form>
            </div>
        </div>
        <div class="loading" v-if="loading===true">Loading&#8230;</div>
    </div>
</div>
</template>

<script>
import axios from "axios";

export default {
    name: "App",
    //delimiters: ['${','}'],
    data: () => ({
        cases: [],
        loading: false,
        currentCase: {},
        message: null,
        newCase: {
            'client_first_name': null,
            'client_last_name': null
        },
    }),
    created() {
        // shows empty array
        console.log(this.cases)
        this.getCases();
        $("#addCaseModal").modal('show');
    },
    methods: {
        getCases: function () {
            this.loading = true;
            axios.get('/api/case/')
                .then((response) => {
                    console.log(response.data);
                    this.cases = response.data;
                    this.loading = false;
                })
                .catch((err) => {
                    this.loading = false;
                    console.log(err);
                })
        },
        getCase: function (id) {
            this.loading = true;
            axios.get(`/api/case/${id}/`)
                .then((response) => {
                    console.log(response.data);
                    this.currentCase = response.data;
                    $("#editCaseModal").modal('show');
                    this.loading = false;
                })
                .catch((err) => {
                    this.loading = false;
                    console.log(err);
                })
        },
        addCase: function () {
            this.loading = true;
            axios.post(`/api/case/`, this.newCase)
                .then((response) => {
                    this.loading = false;
                    this.getCases();
                })
                .catch((err) => {
                    this.loading = false;
                    console.log(err);
                })
        },
        updateCase: function () {
            this.loading = true;
            axios.put(`/api/case/${this.currentCase.id}/`, this.currentCase)
                .then((response) => {
                    this.loading = false;
                    this.currentCase = response.data;
                    this.getCases();
                })
                .catch((err) => {
                    this.loading = false;
                    console.log(err);
                })
        },
        deleteCase: function (id) {
            this.loading = true;
            axios.delete(`/api/case/${id}/`)
                .then((response) => {
                    this.loading = false;
                    this.getCases();
                })
                .catch((err) => {
                    this.loading = false;
                    console.log(err);
                })
        }
    }
};
</script>

<style lang="css">

</style>
