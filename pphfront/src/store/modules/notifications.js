// store/modules/notifications.js

import { Notify } from 'quasar';

const actions = {
  showNotification(_, payload) {
    let config = {};

    switch(payload.type) {
      case 'success':
        config = {
          color: 'green-3',
          icon: 'announcement'
        };
        break;
      case 'error':
        config = {
          color: 'red-3',
          icon: 'warning'
        };
        break;
      case 'info':
        config = {
          color: 'blue-3',
          icon: 'info'
        };
        break;
    }

    Notify.create({
      message: payload.message,
      ...config,
      timeout: 5000,
      position: 'top-right',
      ...payload.options // Pour les options supplémentaires si nécessaire
    });
  }
};

export default {
  namespaced: true,
  actions
};
