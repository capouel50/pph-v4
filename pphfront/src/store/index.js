import { createStore } from 'vuex';
import suppliers from './modules/suppliers';
import users from './modules/users';
import notifications from './modules/notifications';
import contact from './modules/contact';
import auth from './modules/auth';
import user from './modules/user';
import error from './modules/errorModule';
import screen from './modules/screen';
import forms from './modules/forms';
import matieresPremieres from './modules/matieresPremieres';
import formules from './modules/formules';
import voiesAdministration from './modules/voiesAdministration';
import demandes from './modules/demandes';
import fiches from './modules/fiches';

const store = createStore({
  modules: {
    fiches,
    demandes,
    voiesAdministration,
    formules,
    matieresPremieres,
    suppliers,
    users,
    notifications,
    contact,
    user,
    auth,
    error,
    screen,
    forms,
  }
});

export default store;

