// store/modules/spinner.js

const state = {
  isLoading: false,
};

const mutations = {
  SET_LOADING(state, payload) {
    state.isLoading = payload;
  },
};

const actions = {
  showSpinner({ commit }) {
    commit('SET_LOADING', true);
  },
  hideSpinner({ commit }) {
    commit('SET_LOADING', false);
  },
};

const getters = {
  isLoading: state => state.isLoading,
};

export default {
  namespaced: true,
  state,
  mutations,
  actions,
  getters,
};
