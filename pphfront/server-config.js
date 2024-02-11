// server-config.js

const isProduction = process.env.NODE_ENV === 'production';

let serverURL;
if (isProduction) {
  // URL du serveur en production
  serverURL = 'wss://pph-67ad92a79bdd.herokuapp.com/ws/notifications/';
} else {
  // URL du serveur en développement local
  serverURL = 'ws://localhost:8001/ws/notifications/';
}

export default serverURL;
