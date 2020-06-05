import Vuex from 'vuex';

export const store = new Vuex.Store({
    state: data2,
    getters: {
        user: state => state.user,
    },
  });