import axios from 'axios'
import NProgress from 'nprogress'
import 'nprogress/nprogress.css'

const api = axios.create({
  baseURL: 'https://pph-67ad92a79bdd.herokuapp.com',
  withCredentials: true,
})

export const getRefreshTokenFromCookie = () => {
  const refreshTokenRow = document.cookie.split('; ').find(row => row.startsWith('refresh_token'));
  if (refreshTokenRow) {
    return refreshTokenRow.split('=')[1];
  }
  return null;
};


const setCookie = (name, value, days) => {
  var expires = "";
  if (days) {
      var date = new Date();
      date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
      expires = "; expires=" + date.toUTCString();
  }
  document.cookie = name + "=" + (value || "") + expires + "; path=/";
}

const logoutUser = () => {
  // Effacer le token de l'utilisateur et le déconnecter ici.
  // Supprimez également les cookies.
  setCookie("access_token", "", -1);
  setCookie("refresh_token", "", -1);
  // Vous pouvez ajouter d'autres logiques de déconnexion si nécessaire.
};

const refreshAccessToken = async (refreshToken) => {
  try {
    const response = await api.post('/api/token/refresh/', {
      refresh: refreshToken
    });
    if (response.data && response.data.access) {
      document.cookie = `access_token=${response.data.access}`;
      return response.data.access;
    }
  } catch (err) {
    return null;
  }
};

api.interceptors.response.use(
  (response) => {
    return response;
  },
  async (error) => {
    if (error.response && error.response.status === 401) {
      const originalRequest = error.config;
      const refreshToken = getRefreshTokenFromCookie();

      if (!originalRequest._retry && refreshToken) {
        originalRequest._retry = true;
        const newAccessToken = await refreshAccessToken(refreshToken);

        if (newAccessToken) {
          originalRequest.headers['Authorization'] = `Bearer ${newAccessToken}`;
          return api(originalRequest);
        }
      }
      logoutUser();
    }
    return Promise.reject(error);
  }
);

api.interceptors.request.use(config => {
    if (config.data && config.data.isTrusted) {
        return new Promise(() => {
            // eslint-disable-next-line no-unused-vars
        });
    }
    return config;
});


api.getUserData = function() {
  return this.get('PPH/current_user/');
}

// Avant de faire la requête
api.interceptors.request.use(config => {
  NProgress.start()
  return config
})

// Lors de la réception de la réponse
api.interceptors.response.use(response => {
  NProgress.done()
  return response
}, error => {
  NProgress.done()
  return Promise.reject(error)
})

export default api

