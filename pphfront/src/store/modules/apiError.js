
const state = {
  error: null
};

const mutations = {
  SET_ERROR(state, errorMessage) {
    state.error = errorMessage;
  },
};

const actions = {
  ApiError({ commit, dispatch }, error) {
    let errorMessage = error.response?.data?.detail;
    if (errorMessage) {
      // Supprimer les parties [ErrorDetail(string= et )]
      errorMessage = errorMessage.replace(/\[ErrorDetail\(string=/g, '').replace(/\)\s*\]/g, '');
      errorMessage = errorMessage.replace(/code='invalid',/g, '');
      errorMessage = errorMessage.replace(/code='invalid'/g, '');
    }
    commit('SET_ERROR', errorMessage);
    dispatch('notifications/showNotification', {
      message: errorMessage,
      type: 'error'
    }, { root: true });
  },

};

export default {
  namespaced: true,
  state,
  mutations,
  actions
};

