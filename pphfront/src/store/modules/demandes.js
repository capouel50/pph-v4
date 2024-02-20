import api from '../../../api';

const state = {
  demandes: [],
  parametresDemandes: [],
  showMenu: {},
  expanded: {},
  settings: {},
  compo: {},
};

const getters = {
  compo: (state) => state.compo,

  settings: (state) => state.settings,

  expanded: (state) => state.expanded,

  showMenu: (state) => state.showMenu,

  allParametresDemandes: state => state.parametresDemandes,

  allDemandes: state => state.demandes,

  demandesDates: state => {
    // Retourner un tableau contenant uniquement les dates des demandes
    return state.demandes.map(demande => demande.date_prevu);
  },

  nombreDemandes: (state) => state.demandes.length,

  demandeProche: (state) => {
    const demandesTriees = [...state.demandes].sort((a, b) => {
      return new Date(a.date_prevu) - new Date(b.dat_prevu);
    });

    if (demandesTriees.length > 0) {
      const demandeProche = demandesTriees[0];
      const datePrevu = new Date(demandeProche.date_prevu);

      // Obtenir les composants de la date
      const jour = ('0' + datePrevu.getDate()).slice(-2);
      const mois = ('0' + (datePrevu.getMonth() + 1)).slice(-2);
      const annee = datePrevu.getFullYear();

      // Créer la chaîne de date au format jour/mois/année
      const dateFormatee = `${jour}/${mois}/${annee}`;

      // Ajouter la propriété formatée à la demande
      demandeProche.dateFormatee = dateFormatee;

      return demandeProche;
    } else {
      return null;
    }
  },

  nombreDemandesProche: (state, getters) => {
    const demandeProche = getters.demandeProche;

    if (!demandeProche) {
      return 0; // Aucune demande proche, donc le nombre est zéro
    }

    const demandesProche = state.demandes.filter((demande) => {
      return new Date(demande.date_prevu).getTime() === new Date(demandeProche.date_prevu).getTime();
    });

    return demandesProche.length;
  },
};

const actions = {

  ApiError({ dispatch }, error) {
    let errorMessage = error.response?.data?.detail;
    if (errorMessage) {
      // Supprimer les parties [ErrorDetail(string= et )]
      errorMessage = errorMessage.replace(/\[ErrorDetail\(string=/g, '').replace(/\)\s*\]/g, '');
      errorMessage = errorMessage.replace(/code='invalid',/g, '');
      errorMessage = errorMessage.replace(/code='invalid'/g, '');
    }
    dispatch('notifications/showNotification', {
      message: errorMessage,
      type: 'error'
    }, { root: true });
  },

  async addParametresValues({dispatch}, jsonData) {
    try {
      await api.post('PPH/parametres-demandes/', jsonData, {
        headers: {
          'Content-Type': 'application/json'
        }
      });
      dispatch('notifications/showNotification', {
        message: 'Paramètres enregistrés avec succès',
        type: 'success'
      }, {root: true});
      return Promise.resolve();
    } catch (error) {
      dispatch('notifications/showNotification', {
        message: 'Erreur lors de l\'ajout des paramètres',
        type: 'error'
      }, {root: true});
      dispatch('ApiError', error);
      return Promise.reject(error);
    }
  },

  async loadParametresDemandes({ commit, dispatch }) {
    try {
      const response = await api.get('/parametres-demandes');
      commit('SET_PARAMETRES_DEMANDES', response.data);

    } catch (error) {
      dispatch('ApiError', error);
    }
  },

  async addDemande({dispatch}, demandeData) {
    try {
      await api.post('PPH/demandes/', demandeData);
      dispatch('notifications/showNotification', {
        message: 'Demande enregistrée avec succès',
        type: 'success'
      }, {root: true});
      return Promise.resolve();
    } catch (error) {
      dispatch('notifications/showNotification', {
        message: 'Erreur lors de l\'ajout de la demande',
        type: 'error'
      }, {root: true});
      dispatch('ApiError', error);
      return Promise.reject(error);
    }
  },

  async loadDemandes({ commit, dispatch }) {
    try {
      const response = await api.get('/demandes');
      commit('SET_DEMANDES', response.data);

    } catch (error) {
      dispatch('ApiError', error);
    }
  },

  async deleteDemande({ dispatch }, demandeId) {
    try {
      await api.delete(`/PPH/demandes/${demandeId}`);
      dispatch('notifications/showNotification', {
        message: 'Demande supprimée',
        type: 'success'
      }, { root: true });
      dispatch('loadDemandes');
    } catch (error) {
      dispatch('notifications/showNotification', {
        message: 'Erreur lors de la suppression',
        type: 'error'
      }, { root: true });
      dispatch('ApiError', error);
    }
  },

  async toggleProduction({ dispatch }, payload) {
    const { demandeId, isProduction } = payload;
    try {
      if (isProduction) {
        await api.patch(`/PPH/demandes/${demandeId}/`, { production: false });
        dispatch('notifications/showNotification', {
          message: 'Demande mise en attente',
          type: 'success'
        }, { root: true });
      } else {
        await api.patch(`/PPH/demandes/${demandeId}/`, { production: true });
        dispatch('notifications/showNotification', {
          message: 'Demande mise en production',
          type: 'success'
        }, { root: true });
      }
      dispatch('loadDemandes');
    } catch (error) {
      dispatch('notifications/showNotification', {
        message: 'Erreur lors du changement d\'état',
        type: 'error'
      }, { root: true });
      dispatch('ApiError', error);
    }
  },

  async stopRepeat({ dispatch }, payload) {

  const { demandeId } = payload;
  try {
    await api.patch(`/PPH/demandes/${demandeId}/`, { recurence: null, delai: null });
    dispatch('notifications/showNotification', {
      message: 'Demande mise en attente',
      type: 'success'
    }, { root: true });
    dispatch('loadDemandes');
  } catch (error) {
    dispatch('notifications/showNotification', {
      message: 'Erreur lors du changement d\'état',
      type: 'error'
    }, { root: true });
    dispatch('ApiError', error);
  }
},

  toggleMenu({ commit }, id) {
    commit('TOGGLE_MENU', id);
  },

  toggleInfo({ commit }, id) {
    commit('TOGGLE_INFO', id);
  },
  toggleSettings({ commit }, id) {
    commit('TOGGLE_SETTINGS', id);
  },
  toggleCompo({ commit }, id) {
    commit('TOGGLE_COMPO', id);
  },
};

const mutations = {
  SET_DEMANDES: (state, demandes) => {
    state.demandes = demandes;
  },

  SET_PARAMETRES_DEMANDES: (state, parametresDemandes) => {
    state.parametresDemandes = parametresDemandes;
  },

  TOGGLE_MENU(state, id) {
    state.showMenu[id] = !state.showMenu[id];
  },
  TOGGLE_INFO(state, id) {
    state.expanded[id] = !state.expanded[id];
  },
  TOGGLE_SETTINGS(state, id) {
    state.settings[id] = !state.settings[id];
  },
  TOGGLE_COMPO(state, id) {
    state.compo[id] = !state.compo[id];
  },
};
export default {
  namespaced: true,
  state,
  getters,
  mutations,
  actions,
};
