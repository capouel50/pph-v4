import { createRouter, createWebHistory } from 'vue-router'
import store from '@/store';
import UserRegister from '@/components/User/UserRegister.vue'
import UserLogin from '@/components/User/UserLogin.vue'
import PasswordReset from "@/components/User/PasswordReset.vue"
import CreateSupplier from "@/components/Supplier/CreateSupplier.vue"
import SuppliersCards from "@/components/Supplier/SuppliersCards.vue";
import UserProfil from "@/components/User/UserProfil.vue";
import UserAccount from "@/components/User/UserAccount.vue";
import UsersCards from "@/components/User/UsersCards.vue";
import MentionsLegales from "@/components/FooterLinks/MentionsLegales.vue";
import CdtGalUtl from "@/components/FooterLinks/CdtGalUtl.vue";
import HomePage from "@/components/HomePage.vue";
import MatieresCards from "@/components/MatieresPremiere/MatieresCards.vue";
import CreateFormula from "@/components/Formules/CreateFormula.vue";

const routes = [
  {
    path: '/cgu/',
    name: 'CdtGalUtl',
    component: CdtGalUtl
  },
  {
    path: '/mentions/',
    name: 'MentionsLegales',
    component: MentionsLegales
  },
  {
    path: '/home/',
    name: 'Home',
    component: HomePage
  },
  {
    path: '/register',
    name: 'Register',
    component: UserRegister,
    beforeEnter: async (to, from, next) => {
    await store.dispatch('auth/checkAuthentication');

    if (store.state.auth.isLoggedIn) {
      await store.dispatch('notifications/showNotification', {
        message: 'Vous devez vous déconnecter pour accéder à cette page !',
        type: 'info'
      }, { root: true });
      next('/home');
      } else {
        next();
      }
    }
  },
  {
  path: '/login',
  name: 'Login',
  component: UserLogin,
  beforeEnter: async (to, from, next) => {
    await store.dispatch('auth/checkAuthentication');

    if (store.state.auth.isLoggedIn) {
      await store.dispatch('notifications/showNotification', {
        message: 'Vous devez vous déconnecter pour accéder à cette page !',
        type: 'info'
      }, { root: true });
      next('/home');
      } else {
        next();
      }
    }
  },
  {
    path: '/password-reset',
    name: 'PasswordReset',
    component: PasswordReset,
    beforeEnter: async (to, from, next) => {
      await store.dispatch('auth/checkAuthentication');

      if (store.state.auth.isLoggedIn) {
        await store.dispatch('notifications/showNotification', {
          message: 'Vous devez vous déconnecter pour accéder à cette page !',
          type: 'info'
        }, {root: true});
        next('/home');
      } else {
        next();
      }
    }
  },
  {
    path: '/user-account',
    name: 'UserAccount',
    component: UserAccount
  },
  {
    path: '/user',
    name: 'User',
    component: UserProfil
  },
  {
    path: '/users',
    name: 'UsersCards',
    component: UsersCards
  },
  {
    path: '/supplier',
    name: 'CreateSupplier',
    component: CreateSupplier
  },
  {
    path: '/supplier/:id',
    component: CreateSupplier,
    name: 'supplier-form',
    props: true
  },
  {
    path: '/suppliers',
    name: 'SuppliersCards',
    component: SuppliersCards
  },
  {
    path: '/matieres-premieres',
    name: 'MatieresCards',
    component: MatieresCards
  },
  {
    path: '/nouvelle-formule',
    name: 'CreateFormula',
    component: CreateFormula
  },
]

const router = createRouter({
  history: createWebHashHistory(process.env.BASE_URL || '/'),
  routes
})

export default router
