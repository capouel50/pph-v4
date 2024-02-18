import api from '../../../api';

const state = () => ({
  services: [],
});

const getters = {
  allServices: (state) => state.services,
};

const actions = {

  async addService({dispatch}, formData) {
    try {
      await api.post('PPH/service/', formData);
      dispatch('notifications/showNotification', {
        message: 'Service ajouté avec succès',
        type: 'success'
      }, {root: true});
      return Promise.resolve();
    } catch (error) {
      dispatch('notifications/showNotification', {
        message: 'Erreur lors de l\'ajout du service',
        type: 'error'
      }, {root: true});
      return Promise.reject(error);
    }
  },

  async loadServices({commit, dispatch}) {
    try {
      const response = await api.get('/PPH/service');
      commit('SET_SERVICE', response.data);
      console.log(response.data);
    } catch (error) {
      dispatch('notifications/showNotification', {
        message: 'Erreur lors du chargement des services',
        type: 'error'
      }, {root: true});
      console.error(error);
    }
  },
};

const mutations = {
  ADD_SERVICE(state, service) {
    state.services.push(service);
  },
  SET_SERVICE(state, services) {
    state.services = services;
  },
};

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
};