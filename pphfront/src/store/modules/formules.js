import api from '../../../api';

const state = () => ({
  types: [],
  parametres: [],
  parametresFormules: [],
  compositions: [],
  formules: [],
  listes: [],
  showMenu: {},
  expanded: {},
  currentFormuleId: null,
});

const getters = {
  expanded: (state) => state.expanded,
  showMenu: (state) => state.showMenu,
  allTypes: (state) => state.types,
  allCompositions: (state) => state.compositions,
  allParametres: (state) => state.parametres,
  allParametresFormules: (state) => state.parametresFormules,
  allFormules: (state) => state.formules,
  allListes: (state) => state.listes,
};

const actions = {

  async addParametres({dispatch}, formData) {
    try {
      console.log("Envoi de formData:", formData);
        // Assurez-vous que 'formData' est directement le tableau d'objets
        await api.post('PPH/parametres-formules/', formData, {
          headers: {
          'Content-Type': 'application/json'
          }
        })
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

  async loadCompositions({commit, dispatch}) {
    try {
      const response = await api.get('/PPH/composition');
      commit('SET_COMPOSITIONS', response.data);
      console.log(response.data);
    } catch (error) {
      dispatch('notifications/showNotification', {
        message: 'Erreur lors du chargement des compositions',
        type: 'error'
      }, {root: true});
      console.error(error);
    }
  },

  async loadFormules({commit, dispatch}) {
    try {
      const response = await api.get('/PPH/formules');
      commit('SET_FORMULES', response.data);
      console.log(response.data);
    } catch (error) {
      dispatch('notifications/showNotification', {
        message: 'Erreur lors du chargement des formules',
        type: 'error'
      }, {root: true});
      console.error(error);
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

  async loadParametresFormules({commit, dispatch}) {
    try {
      const response = await api.get('/PPH/parametres-formules');
      commit('SET_PARAMETRE_FORMULES', response.data);
      console.log(response.data);
    } catch (error) {
      dispatch('notifications/showNotification', {
        message: 'Erreur lors du chargement des paramètres',
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

  async toggleActivation({ dispatch }, payload) {
    const { formuleId, isActive } = payload;
    try {
      if (isActive) {
        await api.patch(`/PPH/formules/${formuleId}/`, { is_activate: false });
        dispatch('notifications/showNotification', {
          message: 'Formule désactivée',
          type: 'success'
        }, { root: true });
      } else {
        await api.patch(`/PPH/formules/${formuleId}/`, { is_activate: true });
        dispatch('notifications/showNotification', {
          message: 'Formule activée',
          type: 'success'
        }, { root: true });
      }
      dispatch('loadFormules');
    } catch (error) {
      dispatch('notifications/showNotification', {
        message: 'Erreur lors du changement d\'état',
        type: 'error'
      }, { root: true });
      console.error(error);
    }
  },

  async validFormule({ dispatch }, payload) {
    const { formuleId, isValid } = payload;
    try {
      if (isValid) {
        await api.patch(`/PPH/formules/${formuleId}/`, { is_valid: false });
        dispatch('notifications/showNotification', {
          message: 'Formule non-validée',
          type: 'success'
        }, { root: true });
      } else {
        await api.patch(`/PPH/formules/${formuleId}/`, { is_valid: true });
        dispatch('notifications/showNotification', {
          message: 'Formule validée',
          type: 'success'
        }, { root: true });
      }
      dispatch('loadformules');
    } catch (error) {
      dispatch('notifications/showNotification', {
        message: 'Erreur lors du changement d\'état',
        type: 'error'
      }, { root: true });
      console.error(error);
    }
  },

  toggleMenu({ commit }, id) {
    commit('TOGGLE_MENU', id);
  },

  toggleInfo({ commit }, id) {
    commit('TOGGLE_INFO', id);
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
  SET_COMPOSITIONS(state, compositions) {
    state.compositions = compositions;
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
  SET_PARAMETRE_FORMULES(state, parametres) {
    state.parametresFormules = parametres;
  },
  SET_FORMULES(state, formules) {
    state.formules = formules;
  },
  TOGGLE_MENU(state, id) {
    state.showMenu[id] = !state.showMenu[id];
  },
  TOGGLE_INFO(state, id) {
    state.expanded[id] = !state.expanded[id];
  },
};

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
};