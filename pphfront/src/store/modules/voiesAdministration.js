import api from '../../../api';

const state = () => ({
  voies: [],
});

const getters = {
  allVoies: (state) => state.voies,
};

const actions = {

  async addVoie({dispatch}, formData) {
    try {
      await api.post('PPH/voie/', formData);
      dispatch('notifications/showNotification', {
        message: 'Voie d\'administration ajoutée avec succès',
        type: 'success'
      }, {root: true});
      return Promise.resolve();
    } catch (error) {
      dispatch('notifications/showNotification', {
        message: 'Erreur lors de l\'ajout de la voie d\'administration',
        type: 'error'
      }, {root: true});
      return Promise.reject(error);
    }
  },

  async loadVoies({commit, dispatch}) {
    try {
      const response = await api.get('/PPH/voie');
      commit('SET_VOIE', response.data);
      console.log(response.data);
    } catch (error) {
      dispatch('notifications/showNotification', {
        message: 'Erreur lors du chargement des voies',
        type: 'error'
      }, {root: true});
      console.error(error);
    }
  },
};

const mutations = {
  ADD_VOIE(state, voie) {
    state.voies.push(voie);
  },
  SET_VOIE(state, voies) {
    state.voies = voies;
  },
};

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
};