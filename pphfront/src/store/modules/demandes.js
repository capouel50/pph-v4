import api from '../../../api';

const state = {
  demandes: [],
};

const getters = {
  demandesAll: state => state.demandes,
  demandesDates: state => {
    // Retourner un tableau contenant uniquement les dates des demandes
    return state.demandes.map(demande => demande.date_prevu);
  },
  nombreDemandes: (state) => state.demandes.length,
  demandeProche: (state) => {
    const demandesTriees = [...state.demandes].sort((a, b) => {
      return new Date(a.date_prevu) - new Date(b.dat_prevu);
    });

    if (demandesTriees.length > 0) {
      const demandeProche = demandesTriees[0];
      const datePrevu = new Date(demandeProche.date_prevu);

      // Obtenir les composants de la date
      const jour = ('0' + datePrevu.getDate()).slice(-2);
      const mois = ('0' + (datePrevu.getMonth() + 1)).slice(-2);
      const annee = datePrevu.getFullYear();

      // Créer la chaîne de date au format jour/mois/année
      const dateFormatee = `${jour}/${mois}/${annee}`;

      // Ajouter la propriété formatée à la demande
      demandeProche.dateFormatee = dateFormatee;

      return demandeProche;
    } else {
      return null;
    }
  },

  nombreDemandesProche: (state, getters) => {
    const demandeProche = getters.demandeProche;

    if (!demandeProche) {
      return 0; // Aucune demande proche, donc le nombre est zéro
    }

    const demandesProche = state.demandes.filter((demande) => {
      return new Date(demande.date_prevu).getTime() === new Date(demandeProche.date_prevu).getTime();
    });

    return demandesProche.length;
  },
};

const mutations = {
  setDemandes: (state, demandes) => {
    state.demandes = demandes;
  },
};

const actions = {
  async loadDemandes({ commit }) {
    try {
      const response = await api.get('/demandes');
      commit('setDemandes', response.data);

    } catch (error) {
      console.error('Erreur lors du chargement des demandes :', error);
    }
  },
};

export default {
  namespaced: true,
  state,
  getters,
  mutations,
  actions,
};
