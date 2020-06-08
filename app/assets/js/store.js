import Vuex from 'vuex';

export const store = new Vuex.Store({
    state,
    getters: {},
    mutations: {
        SET_USER : (state,payload) => {
           state.user = payload
        },
        SET_CASE : (state,payload) => {
           state.caseObject = payload
        },
        SET_STATUS_OPTIONS : (state,payload) => {
            state.caseStatusOptions = payload
        },
        SET_FORM : (state,payload) => {
            state.form = payload
        },
        SET_EMAIL_LIST : (state,payload) => {
            state.emailList = payload
        },
      },
      actions: {
        GET_USER : () => data.user,
        GET_CASE : () => data.caseObject,
        GET_STATUS_OPTIONS : () => data.caseStatusOptions,
        GET_FORM : () => data.form,
        GET_EMAIL_LIST : () => data.emailList,
      }
  });