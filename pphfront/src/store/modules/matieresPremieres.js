import api from '../../../api';
import serverURL from '../../../server-config.js';
const state = () => ({
  receptions: [],
  cdts: [],
  formes: [],
  types: [],
  unites: [],
  matieres: [],
  categoriesMatieres: [],
  importsCatalogue: [],
  matieresCatalogue: [],
  showMenu: {},
  expanded: {},
  currentMatiere: null,
  loadingMatieres: false,
});

const getters = {
  loadingMatieres(state) {
    return state.loadingMatieres;
  },
  allCdts: (state) => state.cdts,
  allFormes: (state) => state.formes,
  allUnites: (state) => state.unites,
  allTypes: (state) => state.types,
  allMatieres: (state) => state.matieres,
  allReceptions: (state) => state.receptions,
  allCategories: (state) => state.categoriesMatieres,
  allImports: (state) => state.importsCatalogue,
  allMatieresCatalogue: (state) => state.matieresCatalogue,
  showMenu: (state) => state.showMenu,
  expanded: (state) => state.expanded,
  currentMatiere: state => {
    return state.currentMatiere;
  },
  showMenuMat: state => state.menuMat,
  matieresCdeCount: (state) => {
    const matieresWithCde = state.matieres.filter((matiere) => matiere.cde);
    return matieresWithCde.length;
  },
  matieresLivraisonCount: (state) => {
    return state.matieres.filter((matiere) => matiere.attente_livraison).length;
  },
};

const actions = {

    async addMatiere({ dispatch, commit }, formData) {
      try {
        const response = await api.post('PPH/matieres-premieres/', formData);
        const nouvelleMatiere = response.data; // La nouvelle matière première créée
        commit('ADD_MATIERE', nouvelleMatiere); // Commit pour ajouter la nouvelle matière première à l'état Vuex

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

  async addReception({ dispatch, commit }, formData) {
    try {
    const response = await api.post('PPH/reception/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      }
    });
    const nouvelleReception = response.data; // La nouvelle réception créée
    commit('ADD_RECEPTION', nouvelleReception); // Commit pour ajouter la nouvelle réception à l'état Vuex

    dispatch('notifications/showNotification', {
      message: 'Réception ajoutée avec succès',
      type: 'success'
    }, { root: true });

    return Promise.resolve();
  } catch (error) {
    dispatch('notifications/showNotification', {
      message: 'Erreur lors de l\'ajout de la réception',
      type: 'error'
    }, { root: true });
    return Promise.reject(error);
    }
  },

  async addCertificat({ dispatch }, { formData, id }) {
    try {
    await api.patch(`PPH/reception/${id}/`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      }
    });

    dispatch('notifications/showNotification', {
      message: 'Modifications ajoutée avec succès',
      type: 'success'
    }, { root: true });

    return Promise.resolve();
  } catch (error) {
    dispatch('notifications/showNotification', {
      message: 'Erreur lors de la modification',
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

   async addImport({ dispatch, commit }, formData) {
    return new Promise((resolve, reject) => {
      const socket = new WebSocket(serverURL);
      dispatch('spinner/showSpinner', null, { root: true });

      socket.onopen = () => {
        // La connexion WebSocket est ouverte, maintenant envoyez la requête POST
        api.post('PPH/catalogue-import/', formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
          }
        }).then(() => {
          commit('RESET_MATIERES_CATALOGUE');
          dispatch('notifications/showNotification', {
            message: 'Demande terminée',
            type: 'success'
          }, { root: true });
          dispatch('spinner/hideSpinner', null, { root: true });
          resolve();
        }).catch(error => {
          dispatch('spinner/hideSpinner', null, { root: true });
          dispatch('notifications/showNotification', {
            message: 'Impossible d\'initialiser l\'import',
            type: 'error'
          }, { root: true });
          reject(error);
        });

        // Ajout de l'écouteur pour les messages WebSocket
        socket.addEventListener('message', event => {
          const data = JSON.parse(event.data);
          if (data.notification && data.notification.message) {
            dispatch('notifications/showNotification', {
              message: data.notification.message,
              type: data.notification.notification_type
            }, { root: true });
          } else {
            dispatch('notifications/showNotification', {
              message: 'Format de notification inattendu',
              type: 'error'
            }, { root: true });
          }
        });
      };
    });
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

  async loadReceptions({ commit, dispatch }) {
    try {
      console.log("Chargement des réceptions");
      const response = await api.get('/PPH/reception');
      commit('SET_RECEPTIONS', response.data);
      console.log(response.data);
    } catch (error) {
      dispatch('notifications/showNotification', {
        message: 'Erreur lors du chargement des réceptions',
        type: 'error'
      }, { root: true });
      console.error(error);
    }
  },

  async loadCategoriesMatieres({ commit, dispatch }) {
    try {
      console.log("Chargement des catégories de matières premières");
      const response = await api.get('/PPH/categories');
      commit('SET_CATEGORIES', response.data);
      console.log(response.data);
    } catch (error) {
      dispatch('notifications/showNotification', {
        message: 'Erreur lors du chargement des catégories matières premières',
        type: 'error'
      }, { root: true });
      console.error(error);
    }
  },

  async loadMatieresPremieresCatalogue({ commit, dispatch }) {
    try {
      commit('SET_LOADING_MATIERES', true); // Démarre le chargement
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
    } finally {
      commit('SET_LOADING_MATIERES', false); // Termine le chargement (qu'il réussisse ou échoue)
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

  async toggleCde({ dispatch }, payload) {
    const { matiereId, matiereName, isCde } = payload;
    try {
      if (isCde) {
        await api.patch(`/PPH/matieres-premieres/${matiereId}/`, { cde: false });
        dispatch('notifications/showNotification', {
          message: `${matiereName} retirée de la liste de commande`,
          type: 'success'
        }, { root: true });
      } else {
        await api.patch(`/PPH/matieres-premieres/${matiereId}/`, { cde: true });
        dispatch('notifications/showNotification', {
          message: `${matiereName} ajoutée à la liste de commande`,
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
  async toggleLivraison({ dispatch }, payload) {
    const { matiereId, isLivraison } = payload;
    try {
      if (isLivraison) {
        await api.patch(`/PPH/matieres-premieres/${matiereId}/`, {
          attente_livraison: false,
          cde: true
        });
        dispatch('notifications/showNotification', {
          message: 'Matière première en attente de commande',
          type: 'success'
        }, { root: true });
      } else {
        await api.patch(`/PPH/matieres-premieres/${matiereId}/`, {
          attente_livraison: true,
          cde: false
        });
        dispatch('notifications/showNotification', {
          message: 'Matière première en attente de livraison',
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

  toggleMenuMat({ commit }) {
    commit('SET_MENU_MAT', !this.state.menuMat); // Inverse la valeur actuelle de menuMat
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
  ADD_IMPORT(state, importCat) {
    state.importsCatalogue.push(importCat);
  },
  ADD_RECEPTION(state, reception) {
    state.receptions.push(reception);
  },
  SET_LOADING_MATIERES(state, loading) {
    state.loadingMatieres = loading;
  },
  RESET_MATIERES_CATALOGUE(state) {
    state.matieresCatalogue = [];
  },
  SET_MENU_MAT(state, value) {
    state.menuMat = value;
  },
  SET_MATIERES(state, matieres) {
    state.matieres = matieres;
  },
  SET_RECEPTIONS(state, receptions) {
    state.receptions = receptions;
  },
  SET_CATEGORIES(state, categoriesMatieres) {
    state.categoriesMatieres = categoriesMatieres;
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