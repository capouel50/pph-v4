import api from '../../../api';

const state = {};

const getters = {};

const actions = {
    async resetData({ dispatch }) {
        try {
            // Appelez votre fonction pour réinitialiser les données depuis votre API
            await api.post('/PPH/reset-data/');

            dispatch('notifications/showNotification', {
                message: 'Données réinitialisées avec succès',
                type: 'success'
            }, { root: true });
        } catch (error) {
            dispatch('notifications/showNotification', {
                message: 'Erreur lors de la réinitialisation des données',
                type: 'error'
            }, { root: true });
            console.error(error);
        }
    }
};

const mutations = {};

export default {
    namespaced: true,
    state,
    getters,
    actions,
    mutations
};
