import api from '../../../api';

const state = () => ({
  users: [],
  showMenu: {},
  expanded: {},
  currentUser: null,
});

const getters = {
  allUsers: (state) => state.users,
  showMenu: (state) => state.showMenu,
  expanded: (state) => state.expanded,
  currentUser: state => {
    return state.currentUser;
  }
};

const actions = {

    async addUser({ dispatch }, formData) {
  try {
    await api.post('PPH/users/', formData);
    dispatch('notifications/showNotification', {
      message: 'Utilisateur ajouté avec succès',
      type: 'success'
    }, { root: true });
    return Promise.resolve();
  } catch (error) {
    dispatch('notifications/showNotification', {
      message: 'Erreur lors de l\'ajout de l\'utilisateur.',
      type: 'error'
    }, { root: true });
    return Promise.reject(error);
  }
},

  async fetchUserById(id) {
    try {
      const response = await api.get(`PPH/users/${id}`);
      return response;
    } catch (error) {
      console.error("Erreur lors de la récupération de l'utilisateur:", error);
      throw error; // pour pouvoir le gérer dans le composant
    }
  },

  async loadUsers({ commit, dispatch }) {
    try {
      const response = await api.get('/PPH/users');
      const users = response.data;
      const showMenu = {};
      const expanded = {};

      users.forEach(user => {
        showMenu[user.id] = false;
        expanded[user.id] = false;
      });

      commit('SET_USERS', users);
      commit('INIT_MENU', showMenu);
      commit('INIT_INFO', expanded);
    } catch (error) {
      dispatch('notifications/showNotification', {
        message: 'Erreur lors du chargement des utilisateurs',
        type: 'error'
      }, { root: true });
      console.error(error);
    }
  },

  async toggleActivation({ dispatch }, payload) {
    const { userId, isActive } = payload;
    try {
      if (isActive) {
        await api.patch(`/PPH/users/${userId}/`, { is_active: false });
        dispatch('notifications/showNotification', {
          message: 'Utilisateur désactivé',
          type: 'success'
        }, { root: true });
      } else {
        await api.patch(`/PPH/users/${userId}/`, { is_active: true });
        dispatch('notifications/showNotification', {
          message: 'Utiliisateur activé',
          type: 'success'
        }, { root: true });
      }
      dispatch('loadUsers');
    } catch (error) {
      dispatch('notifications/showNotification', {
        message: 'Erreur lors du changement d\'état',
        type: 'error'
      }, { root: true });
      console.error(error);
    }
  },

  async deleteUser({ dispatch }, userId) {
    try {
      await api.delete(`/PPH/users/${userId}`);
      dispatch('notifications/showNotification', {
        message: 'Utilisateur supprimé',
        type: 'success'
      }, { root: true });
      dispatch('loadUsers');
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

  getUser({ commit }, id) {
    return api.get(`/PPH/users/${id}`)
    .then((response) => {
      commit('SET_CURRENT_USER', response.data);
      return response.data;
    });
  },
};


const mutations = {
  ADD_USER(state, user) {
    state.users.push(user);  // Ajoute le nouvel utilisateur à la liste des utilisateurs dans le state
  },
  SET_USERS(state, users) {
  state.users = users;
  users.forEach(user => {
    state.showMenu = { ...state.showMenu, [user.id]: false };
    state.expanded = { ...state.expanded, [user.id]: false };
  });
  },
  TOGGLE_MENU(state, id) {
    state.showMenu[id] = !state.showMenu[id];
  },

  TOGGLE_INFO(state, id) {
    state.expanded[id] = !state.expanded[id];
  },

  SET_CURRENT_USER(state, user) {
    state.currentUser = user;
  },

  INIT_MENU(state, showMenu) {
    state.showMenu = showMenu;
  },

  INIT_INFO(state, expanded) {
    state.expanded = expanded;
  },

};

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
};
