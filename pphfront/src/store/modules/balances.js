import api from '../../../api';

const state = () => ({
  balances: [],
  instructionsBalances: [],
  showMenu: {},
  expanded: {},
});

const getters = {
  allBalances: (state) => state.balances,
  allInstructionsBalances: (state) => state.instructionsBalances,
  showMenu: (state) => state.showMenu,
  expanded: (state) => state.expanded,
};

const actions = {

  async addBalance({dispatch}, formData) {
    try {
      await api.post('PPH/balances/', formData);
      dispatch('notifications/showNotification', {
        message: 'Balance ajouté avec succès',
        type: 'success'
      }, {root: true});
      return Promise.resolve();
    } catch (error) {
      dispatch('notifications/showNotification', {
        message: 'Erreur lors de l\'ajout de la balance',
        type: 'error'
      }, {root: true});
      return Promise.reject(error);
    }
  },

  async loadBalances({commit, dispatch}) {
    try {
      const response = await api.get('/PPH/balances');
      commit('SET_BALANCES', response.data);
      console.log(response.data);
    } catch (error) {
      dispatch('notifications/showNotification', {
        message: 'Erreur lors du chargement des balance',
        type: 'error'
      }, {root: true});
      console.error(error);
    }
  },

  async loadInstructionsBalances({ commit, dispatch }) {
    try {
      const response = await api.get('/instructions-balances');
      commit('SET_INSTRUCTIONS_BALANCES', response.data);

    } catch (error) {
      dispatch('notifications/showNotification', {
        message: 'Erreur lors du chargement de instructions',
        type: 'error'
      }, {root: true});
      console.error('Erreur lors du chargement des instructions :', error);
    }
  },

  async getCalibration({dispatch}, balance) {
    try {
      console.log('balance', balance)
      const response = await api.get(`PPH/balances/${balance.id}/`);
      const calibrationDate = new Date(response.data.calibration);
      const currentDate = new Date();
      currentDate.setDate(currentDate.getDate() + 30);
      const daysRemaining = Math.floor((calibrationDate.getTime() - currentDate.getTime()) / (1000*60*60*24));
      if (calibrationDate < currentDate) {
        dispatch('notifications/showNotification', {
          message: `La calibration expire dans ${daysRemaining} jours`,  // Insertion du nombre de jours restants dans le message
          type: 'error'
        }, {root: true});
      }
      return Promise.resolve();
    } catch (error) {
      dispatch('notifications/showNotification', {
        message: 'Erreur lors de l\'obtention de la date de calibration',
        type: 'error'
      }, {root: true});
      return Promise.reject(error);
    }
  },

  async toggleActivation({ dispatch }, payload) {
    const { balanceId, isActive, balanceName } = payload;
    try {
      if (isActive) {
        await api.patch(`/PPH/balances/${balanceId}/`, { is_activate: false });
        dispatch('notifications/showNotification', {
          message: `${balanceName} désactivée`,
          type: 'success'
        }, { root: true });
      } else {
        await api.patch(`/PPH/balances/${balanceId}/`, { is_activate: true });
        dispatch('notifications/showNotification', {
          message: `${balanceName} activée`,
          type: 'success'
        }, { root: true });
      }
      dispatch('loadSuppliers');
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
  TOGGLE_MENU(state, id) {
    state.showMenu[id] = !state.showMenu[id];
  },
  TOGGLE_INFO(state, id) {
    state.expanded[id] = !state.expanded[id];
  },
  ADD_BALANCE(state, balance) {
    state.balances.push(balance);
  },
  SET_BALANCES(state, balances) {
    state.balances = balances;
  },
  SET_INSTRUCTIONS_BALANCES(state, instructionsBalances) {
    state.instructionsBalances = instructionsBalances;
  },
};

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
};