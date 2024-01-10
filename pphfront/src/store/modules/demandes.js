import api from '../../../api';

const state = {
  demandes: [],
};

const getters = {
  nombreDemandes: (state) => state.demandes.length,
};

const mutations = {
  setDemandes: (state, demandes) => {
    state.demandes = demandes;
  },
};

const actions = {
  async loadDemandes({ commit }) {
    try {
      const response = await api.get('/demandes');
      commit('setDemandes', response.data);
    } catch (error) {
      console.error('Erreur lors du chargement des demandes :', error);
    }
  },
};

export default {
  namespaced: true,
  state,
  getters,
  mutations,
  actions,
};
