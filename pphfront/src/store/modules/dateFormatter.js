// dateFormatter.js

// Actions
const actions = {
  formatDate({ commit }, date) {
    const formattedDate = formatDate(date);
    commit('SET_FORMATTED_DATE', formattedDate);
  },
};

// Mutations
const mutations = {
  SET_FORMATTED_DATE(state, formattedDate) {
    state.formattedDate = formattedDate;
  },
};

// Getters
const getters = {
  getFormattedDate: state => state.formattedDate,
};

// Helper function to format date
function formatDate(date) {
  const [year, month, day] = date.split('-');
  return `${day}/${month}/${year}`;
}

// State
const state = {
  formattedDate: null,
};

export default {
  state,
  actions,
  mutations,
  getters,
};
