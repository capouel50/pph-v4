import serverURL from "../../../server-config";

const state = {
  socket: null, // La connexion WebSocket
};

const mutations = {
  SET_SOCKET(state, payload) {
    state.socket = payload;
  },
};

const actions = {
  // Initialiser la connexion WebSocket
  initWebSocket({ commit, dispatch }) {
    const socket = new WebSocket(serverURL);

    socket.onopen = () => {
      console.log('WebSocket connecté');
      // Gérer l'ouverture de WebSocket ici
    };

    socket.onerror = (error) => {
      console.error('WebSocket Erreur: ', error);
    };

    socket.onmessage = (event) => {
      const data = JSON.parse(event.data);
      // Dispatch d'autres actions ou commit de mutations en fonction des messages reçus
      if (data.notification) {
        dispatch('notifications/showNotification', {
          message: data.notification.message,
          type: data.notification.notification_type
        }, { root: true });
      }
    };

    socket.onclose = () => {
      console.log('WebSocket déconnecté');
      // Gérer la fermeture de WebSocket ici
    };

    commit('SET_SOCKET', socket);
  },

  // Envoyer un message via WebSocket
  sendMessage({ state }, message) {
    if (state.socket) {
      state.socket.send(JSON.stringify(message));
    }
  },

  // Fermer la connexion WebSocket
  closeWebSocket({ commit, state }) {
    if (state.socket) {
      state.socket.close();
      commit('SET_SOCKET', null);
    }
  },
};

export default {
  namespaced: true,
  state,
  mutations,
  actions,
};
