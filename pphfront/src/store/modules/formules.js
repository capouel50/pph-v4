import api from '../../../api';

const state = () => ({
  types: [],
  parametres: [],
  listes: [],
  currentFormuleId: null,
});

const getters = {
  allTypes: (state) => state.types,
  allParametres: (state) => state.parametres,
  allListes: (state) => state.listes,
};

const actions = {

  async addParametres({dispatch}, formData) {
    try {
      await api.post('PPH/parametres-formules/', formData);
      dispatch('notifications/showNotification', {
        message: 'Paramètres ajoutés avec succès',
        type: 'success'
      }, {root: true});
      return Promise.resolve();
    } catch (error) {
      dispatch('notifications/showNotification', {
        message: 'Erreur lors de l\'ajout des paramètres',
        type: 'error'
      }, {root: true});
      return Promise.reject(error);
    }
  },

  async addFormule({dispatch}, formData) {
    try {
      await api.post('PPH/nouvelle-formule/', formData);
      dispatch('notifications/showNotification', {
        message: 'Formule ajouté avec succès',
        type: 'success'
      }, {root: true});
      return Promise.resolve();
    } catch (error) {
      dispatch('notifications/showNotification', {
        message: 'Erreur lors de l\'ajout de la formule',
        type: 'error'
      }, {root: true});
      return Promise.reject(error);
    }
  },

  async addComposition({dispatch}, formData) {
    try {
      await api.post('PPH/composition/', formData);
      dispatch('notifications/showNotification', {
        message: 'Composition ajoutée avec succès',
        type: 'success'
      }, {root: true});
      return Promise.resolve();
    } catch (error) {
      dispatch('notifications/showNotification', {
        message: 'Erreur lors de l\'ajout de la composition',
        type: 'error'
      }, {root: true});
      return Promise.reject(error);
    }
  },

  async getCompositionsForFormule({ dispatch }, num_formule) {
    try {
      const response = await api.get(`PPH/composition/filter/${num_formule}`);
      return Promise.resolve(response.data);
    } catch (error) {
      dispatch('notifications/showNotification', {
        message: 'Erreur lors de la récupération des compositions existantes',
        type: 'error',
      }, { root: true });
      return Promise.reject(error);
    }
  },

  async addParametre({dispatch}, formData) {
    try {
      await api.post('PPH/parametres-formules/', formData);
      dispatch('notifications/showNotification', {
        message: 'Paramètres ajoutés avec succès',
        type: 'success'
      }, {root: true});
      return Promise.resolve();
    } catch (error) {
      dispatch('notifications/showNotification', {
        message: 'Erreur lors de l\'ajout des paramètres',
        type: 'error'
      }, {root: true});
      return Promise.reject(error);
    }
  },

  async loadListes({commit, dispatch}) {
    try {
      const response = await api.get('/PPH/liste');
      commit('SET_LISTE', response.data);
      console.log(response.data);
    } catch (error) {
      dispatch('notifications/showNotification', {
        message: 'Erreur lors du chargement des listes',
        type: 'error'
      }, {root: true});
      console.error(error);
    }
  },

  async loadTypes({commit, dispatch}) {
    try {
      const response = await api.get('/PPH/type-prep');
      commit('SET_TYPE', response.data);
      console.log(response.data);
    } catch (error) {
      dispatch('notifications/showNotification', {
        message: 'Erreur lors du chargement des types de préparations',
        type: 'error'
      }, {root: true});
      console.error(error);
    }
  },

  async loadParametres({commit, dispatch}) {
    try {
      const response = await api.get('/PPH/parametres-prep');
      commit('SET_PARAMETRE', response.data);
      console.log(response.data);
    } catch (error) {
      dispatch('notifications/showNotification', {
        message: 'Erreur lors du chargement des paramètres',
        type: 'error'
      }, {root: true});
      console.error(error);
    }
  },
};

const mutations = {
  updateName(state, newName) {
    state.name = newName;
  },
  updateTypePrep(state, newTypePrep) {
    state.typePrep = newTypePrep;
  },
  
  ADD_TYPE(state, type) {
    state.types.push(type);
  },
  SET_TYPE(state, types) {
    state.types = types;
  },
  SET_LISTE(state, listes) {
    state.listes = listes;
  },
  ADD_PARAMETRE(state, parametres) {
    state.parametres.push(parametres);
  },
  SET_PARAMETRE(state, parametres) {
    state.parametres = parametres;
  },
};

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
};