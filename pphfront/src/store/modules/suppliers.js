import api from '../../../api';

const state = () => ({
  suppliers: [],
  showMenu: {},
  expanded: {},
  currentSupplier: null,
});

const getters = {
  allSuppliers: (state) => state.suppliers,
  showMenu: (state) => state.showMenu,
  expanded: (state) => state.expanded,
  currentSupplier: state => {
    return state.currentSupplier;
  }
};

const actions = {

    async addSupplier({ dispatch }, formData) {
      try {
        await api.post('PPH/suppliers/', formData);
        dispatch('notifications/showNotification', {
          message: 'Fournisseur ajouté avec succès',
          type: 'success'
        }, { root: true });
        return Promise.resolve();
      } catch (error) {
        dispatch('notifications/showNotification', {
          message: 'Erreur lors de l\'ajout du fournisseur',
          type: 'error'
        }, { root: true });
        return Promise.reject(error);
      }
    },

  async getSupplierById(id) {
    let supplier = null;
      await api.get(`PPH/suppliers/${id}`)
        .then(response => {
          supplier = response.data;
        })
        .catch(e => console.error(e));
      return supplier;
  },

  async fetchSupplierById(id) {
    try {
      const response = await api.get(`PPH/suppliers/${id}`);
      return response;
    } catch (error) {
      console.error("Erreur lors de la récupération du fournisseur:", error);
      throw error; // pour pouvoir le gérer dans le composant
    }
  },

  async loadSuppliers({ commit, dispatch }) {
    try {
      const response = await api.get('/PPH/suppliers');
      commit('SET_SUPPLIERS', response.data);
    } catch (error) {
      dispatch('notifications/showNotification', {
        message: 'Erreur lors du chargement des fournisseurs',
        type: 'error'
      }, { root: true });
      console.error(error);
    }
  },

  async toggleActivation({ dispatch }, payload) {
    const { supplierId, isActive } = payload;
    try {
      if (isActive) {
        await api.patch(`/PPH/suppliers/${supplierId}/`, { is_activate: false });
        dispatch('notifications/showNotification', {
          message: 'Fournisseur désactivé',
          type: 'success'
        }, { root: true });
      } else {
        await api.patch(`/PPH/suppliers/${supplierId}/`, { is_activate: true });
        dispatch('notifications/showNotification', {
          message: 'Fournisseur activé',
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

  async deleteSupplier({ dispatch }, supplierId) {
    try {
      await api.delete(`/PPH/suppliers/${supplierId}`);
      dispatch('notifications/showNotification', {
        message: 'Fournisseur supprimé',
        type: 'success'
      }, { root: true });
      dispatch('loadSuppliers');
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

  getSupplier({ commit }, id) {
    return api.get(`/PPH/suppliers/${id}`)
    .then((response) => {
      commit('SET_CURRENT_SUPPLIER', response.data);
      return response.data;
    });
  },
};


const mutations = {
  ADD_SUPPLIER(state, supplier) {
    state.suppliers.push(supplier);  // Ajoute le nouveau fournisseur à la liste des fournisseurs dans le state
  },
  SET_SUPPLIERS(state, suppliers) {
    state.suppliers = suppliers;
  },
  TOGGLE_MENU(state, id) {
    state.showMenu[id] = !state.showMenu[id];
  },
  TOGGLE_INFO(state, id) {
    state.expanded[id] = !state.expanded[id];
  },
  SET_CURRENT_SUPPLIER(state, supplier) {
    state.currentSupplier = supplier;
  }
};

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
};
