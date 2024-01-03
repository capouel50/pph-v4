import api from '../../../api';

const getDefaultState = () => {
  return {
    showForm: false,
    contactData: {
      name: '',
      email: '',
      message: ''
    }
  };
};

const state = getDefaultState();

const mutations = {
  SET_SHOW_FORM(state, payload) {
    state.showForm = payload;
  },
  SET_CONTACT_DATA(state, payload) {
    console.log('Updating contactData with payload:', payload);
    state.contactData = payload;
  }
};

const actions = {
  toggleForm({ commit }, value) {
    commit('SET_SHOW_FORM', value);
  },
  async submitContactForm({ commit, dispatch }, formData) {
    try {
      let response = await api.post('PPH/contact/', formData);

      // Handle successful submission
      commit('SET_CONTACT_DATA', getDefaultState().contactData); // Reset contactData


      // Show success notification
      dispatch('notifications/showNotification', {
        type: 'success',
        message: 'Votre message a bien été envoyé !'
      }, { root: true }); // Notez `{ root: true }` car c'est un module namespaced

      return response;
    } catch (error) {
      // Handle error during submission
      console.error('There was an error submitting the contact form:', error);

      // Show error notification
      dispatch('notifications/showNotification', {
        type: 'error',
        message: 'Une erreur est survenue lors de l\'envoi de votre message. Veuillez réessayer plus tard.'
      }, { root: true });

    }
  }
};

export default {
  namespaced: true,
  state,
  mutations,
  actions
};
