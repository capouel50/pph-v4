import { createRouter, createWebHistory } from 'vue-router'
import store from '@/store';
import UserRegister from '@/components/User/UserRegister.vue'
import UserLogin from '@/components/User/UserLogin.vue'
import PasswordReset from "@/components/User/PasswordReset.vue"
import CreateSupplier from "@/components/Supplier/CreateSupplier.vue"
import SuppliersCards from "@/components/Supplier/SuppliersCards.vue";
import UserProfil from "@/components/User/UserProfil.vue";
import UsersCards from "@/components/User/UsersCards.vue";
import MentionsLegales from "@/components/FooterLinks/MentionsLegales.vue";
import CdtGalUtl from "@/components/FooterLinks/CdtGalUtl.vue";
import HomePage from "@/components/HomePage.vue";
import MatieresCards from "@/components/MatieresPremiere/MatieresCards.vue";
import MaterielCards from "@/components/MatieresPremiere/MaterielCards.vue";
import MatieresCatalogueCards from "@/components/MatieresPremiere/MatieresCatalogueCards.vue";
import CreateFormula from "@/components/Formules/CreateFormula.vue";
import CreateFiche from "@/components/Fiches/CreateFiche.vue";
import InfosFiche from "@/components/Fiches/InfosFiche.vue";
import ControlesCards from "@/components/Fiches/ControlesCards.vue";
import FichesArchivesCards from "@/components/Fiches/FichesArchivesCards.vue";
import CreateDemande from "@/components/Demandes/CreateDemande.vue";
import DemandesCards from "@/components/Demandes/DemandesCards.vue";
import FormulaCards from "@/components/Formules/FormulaCards.vue";
import CreateMatiere from "@/components/MatieresPremiere/CreateMatiere.vue";
import MatieresCardsReception from "@/components/MatieresPremiere/MatieresCardsReception.vue";
import MatieresCardsCommande from "@/components/MatieresPremiere/MatieresCardsCommande.vue";
import BalancesCards from "@/components/Balances/BalancesCards.vue";
import CreateBalance from "@/components/Balances/CreateBalance.vue";

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
    component: HomePage,
    beforeEnter: async (to, from, next) => {
    await store.dispatch('auth/checkAuthentication');

    if (!store.state.auth.isLoggedIn) {
      await store.dispatch('notifications/showNotification', {
        message: 'Vous devez vous connecter pour accéder à cette page !',
        type: 'info'
      }, { root: true });
      next('/login');
      } else {
        next();
      }
    }
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
    path: '/user/:id',
    name: 'UserAccount',
    component: UserProfil,
  },
  {
    path: '/user',
    name: 'User',
    component: UserProfil
  },
  {
    path: '/user/:id',
    name: 'User',
    component: UserProfil,
    props: true
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
    path: '/materiel',
    name: 'MaterielCards',
    component: MaterielCards
  },
  {
    path: '/catalogue',
    name: 'MatieresCatalogueCards',
    component: MatieresCatalogueCards
  },
  {
    path: '/nouvelle-formule',
    name: 'CreateFormula',
    component: CreateFormula
  },
  {
    path: '/nouvelle-formule/:id',
    name: 'UpdateFormula',
    component: CreateFormula,
    props: true
  },
  {
    path: '/formules',
    name: 'FormulaCards',
    component: FormulaCards
  },
  {
    path: '/demande',
    name: 'CreateDemande',
    component: CreateDemande
  },
  {
    path: '/demandes',
    name: 'DemandesCards',
    component: DemandesCards
  },
  {
    path: '/fiches',
    name: 'CreateFiche',
    component: CreateFiche
  },
  {
    path: '/fiches/:demandeId',
    name: 'GenerateFiche',
    component: InfosFiche,
    props: true
  },
  {
    path: '/fiche/:ficheId',
    name: 'CompoFiche',
    component: InfosFiche,
    props: true
  },
  {
    path: '/fiche/:id',
    name: 'details-fiche',
    component: InfosFiche,
    props: true
  },
  {
    path: '/controles',
    name: 'ControlesCards',
    component: ControlesCards
  },
  {
    path: '/archives',
    name: 'FichesArchivesCards',
    component: FichesArchivesCards
  },
  {
    path: '/creation-matiere-premiere',
    name: 'CreateMatiere',
    component: CreateMatiere
  },
  {
    path: '/reception',
    name: 'MatieresCardsReception',
    component: MatieresCardsReception
  },
  {
    path: '/commande',
    name: 'MatieresCardsCommande',
    component: MatieresCardsCommande
  },
  {
    path: '/balances',
    name: 'BalancesCards',
    component: BalancesCards
  },
  {
    path: '/suppliers/balances',
    name: 'CreateBalancesSupplier',
    component: CreateSupplier
  },
  {
    path: '/creer-balances',
    name: 'CreateBalances',
    component: CreateBalance,
    props: true,
  },
  {
    path: '/modifier-balances/:id',
    name: 'updateBalances',
    component: CreateBalance,
    props: true,
  },
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL || '/'),
  routes
})

export default router
