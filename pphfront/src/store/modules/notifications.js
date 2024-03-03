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
      timeout: payload.time ? payload.time : 5000,
      position: payload.position ? payload.position : 'top-right',
      ...payload.options // Pour les options supplémentaires si nécessaire
    });
  },

  async showNotificationsSeq({ dispatch }, notifications) {
    for (const notification of notifications) {
      await new Promise((resolve) => {
        dispatch('showNotification', notification);
        setTimeout(resolve, 2000); // Délai de 2 secondes (ajustez selon vos besoins)
      });
    }
  },

  showNotificationBackend(_, payload) {
    let config = {};

    switch (payload.type) {
      case 'success':
        config = {
          color: 'green-3',
          icon: 'announcement',
        };
        break;
      case 'error':
        config = {
          color: 'red-3',
          icon: 'warning',
        };
        break;
      case 'info':
        config = {
          color: 'blue-3',
          icon: 'info',
        };
        break;
    }

    // Afficher la notification immédiatement
    const notification = Notify.create({
      message: payload.message,
      ...config,
      timeout: 5000,
      position: 'top-right',
      ...payload.options, // Pour les options supplémentaires si nécessaire
    });

    Notify.emitter.$emit('notification-displayed', notification);

    // Continuer le traitement ou effectuer d'autres actions
  },
};

export default {
  namespaced: true,
  actions
};
