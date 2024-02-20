import api from '../../../api';

const state = {
  fiches: [],
  parametresFiches: [],
  fichesSemaine: [],
  showMenu: {},
  settings: {},
  compo: {},
  info: {},
};

const getters = {
  showMenu: (state) => state.showMenu,

  settings: (state) => state.settings,

  compo: (state) => state.compo,

  info: (state) => state.info,

  allParametresFiches: state => state.parametresFiches,

  fichesControlCount: (state) => {
    return state.fiches.filter((fiche) => fiche.attente_controle).length;
  },
  fichesControl: (state) => {
    return state.fiches.filter((fiche) => fiche.attente_controle === true);
  },
  allFiches: (state) => {
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

const actions = {

  async addParametresValues({dispatch}, jsonData) {
    try {
      await api.post('PPH/parametres-fiches/', jsonData, {
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
      return Promise.reject(error);
    }
  },

  async loadParametresFiches({ commit }) {
    try {
      const response = await api.get('/parametres-fiches');
      commit('SET_PARAMETRES_FICHES', response.data);

    } catch (error) {
      console.error('Erreur lors du chargement des fiches :', error);
    }
  },

  async addFiche({dispatch}, ficheData) {
    try {
      await api.post('PPH/fiches/', ficheData);
      dispatch('notifications/showNotification', {
        message: 'Fiche enregistrée avec succès',
        type: 'success'
      }, {root: true});
      return Promise.resolve();
    } catch (error) {
      dispatch('notifications/showNotification', {
        message: 'Erreur lors de l\'ajout de la fiche',
        type: 'error'
      }, {root: true});
      return Promise.reject(error);
    }
  },

  async loadFiches({ commit }) {
    try {
      const response = await api.get('/fiches');
      commit('SET_FICHES', response.data);
    } catch (error) {
      console.error('Erreur lors du chargement des fiches :', error);
    }
  },

  async loadFichesSemaine({ commit }) {
    try {
      const response = await api.get('/PPH/fiches-semaine');
      commit('SET_FICHES_SEMAINES', response.data);
    } catch (error) {
      console.error('Erreur lors du chargement des fiches par semaine :', error);
    }
  },

  async toggleControle({ dispatch }, payload) {
    const { ficheId, isControl } = payload;
    try {
      if (isControl) {
        await api.patch(`/PPH/fiches/${ficheId}/`, {
          controle_valide: false,
          destruction: true,
        });
        dispatch('notifications/showNotification', {
          message: 'Contrôle non validé',
          type: 'success'
        }, { root: true });
      } else {
        await api.patch(`/PPH/fiches/${ficheId}/`, {
          controle_valide: true,
          attente_controle: false,
        });
        dispatch('notifications/showNotification', {
          message: 'Contrôle validé',
          type: 'success'
        }, { root: true });
      }
      dispatch('loadFiches');
    } catch (error) {
      dispatch('notifications/showNotification', {
        message: 'Erreur lors du changement d\'état',
        type: 'error'
      }, { root: true });
      console.error(error);
    }
  },

  toggleInfo({ commit }, id) {
    commit('TOGGLE_INFO', id);
  },

  toggleMenu({ commit }, id) {
    commit('TOGGLE_MENU', id);
  },

  toggleSettings({ commit }, id) {
    commit('TOGGLE_SETTINGS', id);
  },
  toggleCompo({ commit }, id) {
    commit('TOGGLE_COMPO', id);
  },
};

const mutations = {
  SET_FICHES: (state, fiches) => {
    state.fiches = fiches;
  },
  SET_PARAMETRES_FICHES: (state, parametresFiches) => {
    state.parametresFiches = parametresFiches;
  },
  SET_FICHES_SEMAINES: (state, fichesSemaine) => {
    state.fichesSemaine= fichesSemaine;
  },
  TOGGLE_MENU(state, id) {
    state.showMenu[id] = !state.showMenu[id];
  },
  TOGGLE_INFO(state, id) {
    state.info[id] = !state.info[id];
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
