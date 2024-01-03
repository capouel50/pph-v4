import api from '../../../api';

const state = {
    user: {
        firstName: null,
        lastName: null,
        email: null,
        userName: null,
        function: null
    },
    isSubmitting: false,
};

const mutations = {
    SET_USER_DATA(state, payload) {
        state.user = payload;
    },
    UPDATE_FIELD(state, { field, value }) {
    state.user[field] = value;
    },
    SET_SUBMITTING(state, value) {
        state.isSubmitting = value;
    },
};

const actions = {
    async fetchUserData({ commit, dispatch }) {
        try {
            // Récupérer les données de l'utilisateur depuis votre API
            let response = await api.getUserData();
            commit('SET_USER_DATA', response.data);
        } catch (error) {
            console.error('Erreur lors de la récupération des données de l\'utilisateur :', error);

            // Afficher une notification d'erreur
            dispatch('notifications/showNotification', {
                type: 'error',
                message: 'Une erreur est survenue lors de la récupération de vos données. Veuillez réessayer plus tard.'
            }, { root: true });
        }
    },
    async updateUser({ commit, state, dispatch }) {
        commit('SET_SUBMITTING', true);
        try {
            await api.post('PPH/user/update/', state.user);
                dispatch('notifications/showNotification', {
                    message: 'Utilisateur enregistré !',
                    type: 'success'
                    }, { root: true });
        } catch (error) {
            // Gérez l'erreur
        } finally {
            commit('SET_SUBMITTING', false);
        }
    },
};

const getters = {
    user: state => state.user
};

export default {
    state,
    mutations,
    actions,
    getters
};

