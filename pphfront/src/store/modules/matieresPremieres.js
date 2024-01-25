import api from '../../../api';

const state = () => ({
  cdts: [],
  formes: [],
  types: [],
  unites: [],
  matieres: [],
  matieresCatalogue: [],
  showMenu: {},
  expanded: {},
  currentMatiere: null,
});

const getters = {
  allCdts: (state) => state.cdts,
  allFormes: (state) => state.formes,
  allUnites: (state) => state.unites,
  allTypes: (state) => state.types,
  allMatieres: (state) => state.matieres,
  allMatieresCatalogue: (state) => state.matieresCatalogue,
  showMenu: (state) => state.showMenu,
  expanded: (state) => state.expanded,
  currentMatiere: state => {
    return state.currentMatiere;
  },
  matieresCdeCount: (state) => {
    const matieresWithCde = state.matieres.filter((matiere) => matiere.cde);
    return matieresWithCde.length;
  },
  matieresLivraisonCount: (state) => {
    return state.matieres.filter((matiere) => matiere.attente_livraison).length;
  },
};

const actions = {

    async addMatiere({ dispatch }, formData) {
      try {
        await api.post('PPH/matieres-premieres/', formData);
        dispatch('notifications/showNotification', {
          message: 'Matière première ajoutée avec succès',
          type: 'success'
        }, { root: true });
        return Promise.resolve();
      } catch (error) {
        dispatch('notifications/showNotification', {
          message: 'Erreur lors de l\'ajout de la matière première',
          type: 'error'
        }, { root: true });
        return Promise.reject(error);
      }
    },

  async addType({ dispatch }, formData) {
      try {
        await api.post('PPH/types-matieres/', formData);
        dispatch('notifications/showNotification', {
          message: 'Type ajouté avec succès',
          type: 'success'
        }, { root: true });
        return Promise.resolve();
      } catch (error) {
        dispatch('notifications/showNotification', {
          message: 'Erreur lors de l\'ajout du type de matière première',
          type: 'error'
        }, { root: true });
        return Promise.reject(error);
      }
    },

  async addCdt({ dispatch }, formData) {
      try {
        await api.post('PPH/conditionnement/', formData);
        dispatch('notifications/showNotification', {
          message: 'Conditionnement ajouté avec succès',
          type: 'success'
        }, { root: true });
        return Promise.resolve();
      } catch (error) {
        dispatch('notifications/showNotification', {
          message: 'Erreur lors de l\'ajout du conditionnement',
          type: 'error'
        }, { root: true });
        return Promise.reject(error);
      }
    },

  async addForme({ dispatch }, formData) {
      try {
        await api.post('PPH/formes/', formData);
        dispatch('notifications/showNotification', {
          message: 'Forme ajoutée avec succès',
          type: 'success'
        }, { root: true });
        return Promise.resolve();
      } catch (error) {
        dispatch('notifications/showNotification', {
          message: 'Erreur lors de l\'ajout de la forme de matière première',
          type: 'error'
        }, { root: true });
        return Promise.reject(error);
      }
    },

  async fetchMatierePremiereById(id) {
    try {
      const response = await api.get(`PPH/matieres-premieres/${id}`);
      return response;
    } catch (error) {
      console.error("Erreur lors de la récupération de la matière première:", error);
      throw error; // pour pouvoir le gérer dans le composant
    }
  },

  async loadMatieresPremieres({ commit, dispatch }) {
    try {
      console.log("Chargement des matières premières");
      const response = await api.get('/PPH/matieres-premieres');
      commit('SET_MATIERES', response.data);
      console.log(response.data);
    } catch (error) {
      dispatch('notifications/showNotification', {
        message: 'Erreur lors du chargement des matières premières',
        type: 'error'
      }, { root: true });
      console.error(error);
    }
  },

  async loadMatieresPremieresCatalogue({ commit, dispatch }) {
    try {
      console.log("Chargement des matières premières");
      const response = await api.get('/PPH/catalogue');
      commit('SET_MATIERES_CATALOGUE', response.data);
      console.log(response.data);
    } catch (error) {
      dispatch('notifications/showNotification', {
        message: 'Erreur lors du chargement des matières premières',
        type: 'error'
      }, { root: true });
      console.error(error);
    }
  },

  async loadUnites({ commit, dispatch }) {
    try {
      const response = await api.get('/PPH/unites-mesure');
      commit('SET_UNITES', response.data);
      console.log('unites', response.data);
    } catch (error) {
      dispatch('notifications/showNotification', {
        message: 'Erreur lors du chargement des unités',
        type: 'error'
      }, { root: true });
      console.error(error);
    }
  },

  async loadFormes({ commit, dispatch }) {
    try {
      const response = await api.get('/PPH/formes');
      commit('SET_FORMES', response.data);
      console.log('formes', response.data);
    } catch (error) {
      dispatch('notifications/showNotification', {
        message: 'Erreur lors du chargement des unités',
        type: 'error'
      }, { root: true });
      console.error(error);
    }
  },

  async loadTypes({ commit, dispatch }) {
    try {
      const response = await api.get('/PPH/types-matieres');
      commit('SET_TYPES', response.data);
      console.log('types', response.data);
    } catch (error) {
      dispatch('notifications/showNotification', {
        message: 'Erreur lors du chargement des unités',
        type: 'error'
      }, { root: true });
      console.error(error);
    }
  },

  async loadCdt({ commit, dispatch }) {
    try {
      const response = await api.get('/PPH/conditionnement');
      commit('SET_CDT', response.data);
      console.log('cdt', response.data);
    } catch (error) {
      dispatch('notifications/showNotification', {
        message: 'Erreur lors du chargement des conditionnements',
        type: 'error'
      }, { root: true });
      console.error(error);
    }
  },

  async toggleActivation({ dispatch }, payload) {
    const { matiereId, isStockee } = payload;
    try {
      if (isStockee) {
        await api.patch(`/PPH/matieres-premieres/${matiereId}/`, { stockee: false });
        dispatch('notifications/showNotification', {
          message: 'Matière première rétirée du stock',
          type: 'success'
        }, { root: true });
      } else {
        await api.patch(`/PPH/matieres-premieres/${matiereId}/`, { stockee: true });
        dispatch('notifications/showNotification', {
          message: 'Matière première stockée',
          type: 'success'
        }, { root: true });
      }
      dispatch('loadMatieresPremieres');
    } catch (error) {
      dispatch('notifications/showNotification', {
        message: 'Erreur lors du changement d\'état',
        type: 'error'
      }, { root: true });
      console.error(error);
    }
  },

  async deleteMatiere({ dispatch }, matiereId) {
      console.log("deleteMatiere appelée avec l'ID :", matiereId);
    try {
      await api.delete(`/PPH/matieres-premieres/${matiereId}`);
      dispatch('notifications/showNotification', {
        message: 'Matière première supprimée',
        type: 'success'
      }, { root: true });
      dispatch('loadMatieresPremieres');
    } catch (error) {
      dispatch('notifications/showNotification', {
        message: 'Erreur lors de la suppression',
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

  getMatiere({ commit }, id) {
    return api.get(`/PPH/matieres-premieres/${id}`)
    .then((response) => {
      commit('SET_CURRENT_MATIERE', response.data);
      return response.data;
    });
  },
};


const mutations = {
  ADD_CDT(state, cdt) {
    state.cdts.push(cdt);
  },
  ADD_MATIERE(state, matiere) {
    state.matieres.push(matiere);
  },
  ADD_TYPE(state, type) {
    state.type.push(type);
  },
  ADD_FORME(state, forme) {
    state.forme.push(forme);
  },
  SET_MATIERES(state, matieres) {
    state.matieres = matieres;
  },
  SET_MATIERES_CATALOGUE(state, matieresCatalogue) {
    state.matieresCatalogue = matieresCatalogue;
  },
  SET_UNITES(state, unites) {
    state.unites = unites;
  },
  SET_TYPES(state, types) {
    state.types = types;
  },
  SET_CDT(state, cdts) {
    state.cdts = cdts;
  },
  SET_FORMES(state, formes) {
    state.formes = formes;
  },
  TOGGLE_MENU(state, id) {
    state.showMenu[id] = !state.showMenu[id];
  },
  TOGGLE_INFO(state, id) {
    state.expanded[id] = !state.expanded[id];
  },
  SET_CURRENT_MATIERE(state, matiere) {
    state.currentMatiere = matiere;
  }
};

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
};