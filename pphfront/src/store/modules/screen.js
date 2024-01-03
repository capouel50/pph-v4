// store/modules/screen.js

const state = {
  isFullscreen: false
};

const mutations = {
  SET_FULLSCREEN(state, value) {
    state.isFullscreen = value;
  }
};

const actions = {
  toggleFullscreen({ commit, state }) {
    if (state.isFullscreen) {
      document.exitFullscreen();
      commit('SET_FULLSCREEN', false);
    } else {
      document.documentElement.requestFullscreen();
      commit('SET_FULLSCREEN', true);
    }
  }
};

export default {
  namespaced: true,
  state,
  mutations,
  actions
};
