import router from '@/router';
import api from '../../../api';

const state = {
  isLoggedIn: false,
  user: {
    firstName: null,
    lastName: null,
    email: null,
    function: null
  },
  tokenStatus: null // 'valid', 'expiring', 'invalid'
};

const mutations = {
  SET_IS_LOGGED_IN(state, payload) {
    state.isLoggedIn = payload;
  },
  SET_USER_DATA(state, payload) {
    state.user = payload;
  },
  LOGOUT(state) {
    state.isLoggedIn = false;
    state.user = {
      firstName: null,
      lastName: null,
      email: null,
      function: null
    };
  },
  SET_TOKEN_STATUS(state, status) {
    state.tokenStatus = status;
  }
};

const actions = {

  async login({ commit, dispatch }, user) {
    try {
      this.intentionalLogout = false;
      let response = await api.post('/api/token/', user);
      console.log(response.data);

      // Récupérer les données utilisateur et les stocker dans le state
      let userDataResponse = await api.get('/PPH/current_user/');
      commit('SET_USER_DATA', userDataResponse.data);

      commit('SET_IS_LOGGED_IN', true);

      try {
        await document.documentElement.requestFullscreen();
      } catch (err) {
        console.error('Erreur lors de la demande de mode plein écran:', err);
      }

      return true;
    } catch (error) {
        if (error.response && error.response.status === 401) {
          dispatch('notifications/showNotification', {
          message: 'Aucun compte actif pour ces identifiants.',
          type: 'error'
        }, { root: true });
        } else {
          dispatch('notifications/showNotification', {
          message: 'Une erreur est survenue. Veuillez réessayer plus tard ou contatez un administrateur.',
          type: 'error'
        }, { root: true });
        }
      console.error(error);
      let errorMessage = error.response?.data?.detail || 'Échec de la connexion. Veuillez vérifier vos identifiants et réessayer.';
      throw errorMessage;
    }
  },

  async logout({ commit, dispatch }) {
  try {
    // Nous n'avons pas besoin du refreshToken directement ici, car le serveur sait quel utilisateur est connecté.
    // La requête API suivante informe simplement le serveur que nous souhaitons nous déconnecter.
    const response = await api.post('/logout/');
    this.intentionalLogout = true;
    if (response.status !== 200) {
      throw new Error("Erreur lors de la déconnexion.");
    }

    // Commit les mutations pour mettre à jour l'état
    commit('LOGOUT');
    commit('SET_IS_LOGGED_IN', false);

    // Montrer la notification
    dispatch('notifications/showNotification', {
      message: 'Vous êtes déconnecté !',
      type: 'success'
    }, { root: true });

    // Rediriger vers la page de connexion
    router.push({ name: 'Login' });


    // Quitter le mode plein écran si actif
    if (document.fullscreenElement || document.webkitFullscreenElement || document.mozFullScreenElement) {
      if (document.exitFullscreen) {
        document.exitFullscreen();
      } else if (document.webkitExitFullscreen) {
        document.webkitExitFullscreen();
      } else if (document.mozCancelFullScreen) {
        document.mozCancelFullScreen();
      }
    }
  } catch (error) {
    console.error("Une erreur s'est produite lors de la déconnexion :", error);

    // Montrer la notification d'erreur
    dispatch('notifications/showNotification', {
      message: `Erreur lors de la déconnexion : ${error.message}`,
      type: 'error'
    }, { root: true });
  }
},


  async checkAuthentication({ commit, dispatch }) {
      if (this.intentionalLogout) {
        return; // Ne faites rien si l'utilisateur s'est déconnecté intentionnellement
    }
    try {
        // Vérifier la validité du token avec le serveur et récupérer les données de l'utilisateur
        const response = await api.get('PPH/current_user/');
        const userData = response.data;

        if (userData) {
            // Mise à jour des données utilisateur et connexion
            commit('SET_USER_DATA', userData);
            commit('SET_IS_LOGGED_IN', true);

            // Si tokenExpiry est fourni, vérifiez combien de temps il reste
            if (userData.tokenExpiry !== undefined && userData.tokenExpiry !== null) {

                const timeRemaining = userData.tokenExpiry;

                if (timeRemaining <= 600 && timeRemaining > 540) {
                    commit('SET_TOKEN_STATUS', 'nearExpiry');
                    dispatch('notifications/showNotification', {
                      message: 'Votre session expirera dans 10 minutes !',
                      type: 'info'
                    }, { root: true });
                } else if (timeRemaining <= 540 && timeRemaining > 60) {
                    commit('SET_TOKEN_STATUS', 'nearExpiry');
                } else if (timeRemaining <= 300 && timeRemaining > 240) {
                    commit('SET_TOKEN_STATUS', 'nearInvalid');
                    dispatch('notifications/showNotification', {
                      message: 'Votre session expirera dans 5 minutes !',
                      type: 'info'
                    }, { root: true });
                } else if (timeRemaining <= 240 && timeRemaining > 60) {
                    commit('SET_TOKEN_STATUS', 'nearInvalid');
                } else if (timeRemaining <= 60) {
                    commit('SET_TOKEN_STATUS', 'invalid');
                    commit('LOGOUT');
                    // Rediriger vers la page de connexion
                    router.push({ name: 'Login' });

                    dispatch('notifications/showNotification', {
                      message: 'Votre session a expiré !',
                      type: 'info'
                    }, { root: true });

                    // Quittez le mode plein écran si actif
                    if (document.fullscreenElement || document.webkitFullscreenElement || document.mozFullScreenElement) {
                        if (document.exitFullscreen) {
                            document.exitFullscreen();
                        } else if (document.webkitExitFullscreen) {
                            document.webkitExitFullscreen();
                        } else if (document.mozCancelFullScreen) {
                            document.mozCancelFullScreen();
                        }
                    }
                } else {
                    commit('SET_TOKEN_STATUS', 'valid');
                }
            } else {
                // Si tokenExpiry n'est pas fourni, considérez simplement le token comme valide
                commit('SET_TOKEN_STATUS', 'valid');
            }
        } else {
            // Si les données de l'utilisateur ne sont pas présentes, considérez que le token est invalide
            commit('SET_TOKEN_STATUS', 'invalid');
            commit('SET_IS_LOGGED_IN', false);
        }

    } catch (error) {
        if (error.response && error.response.status === 401) {
            // Le token est invalide ou a expiré
            commit('SET_TOKEN_STATUS', 'invalid');
            commit('SET_IS_LOGGED_IN', false);
            dispatch('notifications/showNotification', {
                      message: 'L\'authentification est invalide ou a expiré !',
                      type: 'error'
                    }, { root: true });
        } else {
            console.error('Erreur lors de la vérification du token:', error);
            dispatch('notifications/showNotification', {
                      message: 'Erreur lors de la vérification du token !',
                      type: 'error'
                    }, { root: true });
        }
    }
  },
};

export default {
  namespaced: true,
  state,
  mutations,
  actions,
};
