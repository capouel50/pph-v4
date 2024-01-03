import api from '../../../api';

const state = {
  error: null
};

const mutations = {
  SET_ERROR(state, errorMessage) {
    state.error = errorMessage;
  },
};

const actions = {
  async fetchData({ commit, dispatch }, endpoint) {
    try {
      await api.get(endpoint);

    } catch (error) {
      let errorMessage = error.response?.data?.detail || 'Une erreur est survenue.';
      commit('SET_ERROR', errorMessage);
      dispatch('notifications/showNotification', {
        message: errorMessage,
        type: 'error'
      }, { root: true });
    }
  },
};

export default {
  namespaced: true,
  state,
  mutations,
  actions
};

