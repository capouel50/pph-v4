const state = {
  userFormData: {
    last_name: '',
    first_name: '',
    user_name: '',
    email: '',
  },
  anotherFormData: {
    field1: '',
    field2: ''
    // autres champs
  }
};

const mutations = {
  UPDATE_FIELD(state, { formName, field, value }) {
    if (state[formName]) {
      state[formName][field] = value;
    }
  }
};

const actions = {
  updateField({ commit }, { formName, field, value }) {
    commit('UPDATE_FIELD', { formName, field, value });
  }
};

export default {
  namespaced: true,
  state,
  mutations,
  actions,
};
