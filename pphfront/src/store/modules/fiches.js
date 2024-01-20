import api from '../../../api';

const state = {
  fiches: [],
  fichesSemaine: [],
};

const getters = {
  fichesControlCount: (state) => {
    return state.fiches.filter((fiche) => fiche.attente_controle).length;
  },
  fichesAll: (state) => {
    return state.fiches;
  },
  fichesSemaine: (state) => {
    return state.fichesSemaine.map(fiche => {
      return {
        week: fiche.week,
        count: fiche.count
      };
    });
  },
};

const mutations = {
  setFiches: (state, fiches) => {
    state.fiches = fiches;
  },

  setFichesSemaine: (state, fichesSemaine) => {
    state.fichesSemaine= fichesSemaine;
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

  async loadFichesSemaine({ commit }) {
    try {
      const response = await api.get('/PPH/fiches-semaine');
      commit('setFichesSemaine', response.data);
    } catch (error) {
      console.error('Erreur lors du chargement des fiches par semaine :', error);
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
