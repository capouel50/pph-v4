import api from '../../../api';

const state = {
  fiches: [],
};

const getters = {
  fichesControlCount: (state) => {
    return state.fiches.filter((fiche) => fiche.attente_controle).length;
  },
};

const mutations = {
  setFiches: (state, fiches) => {
    state.fiches = fiches;
  },
};

const actions = {
  async loadFiches({ commit }) {
    try {
      const response = await api.get('/fiches');
      commit('setFiches', response.data);
    } catch (error) {
      console.error('Erreur lors du chargement des fiches :', error);
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
