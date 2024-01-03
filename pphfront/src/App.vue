<template>
<ParticlesAnimated />
  <q-layout view="lHh Lpr lFf">

    <q-toolbar class="q-mt-sm q-ml-sm" style="position: fixed; top: 0; left: 0; right: 0; z-index: 1000;">
      <div>
        <font-awesome-icon icon="fa-solid fa-mortar-pestle" size="xl" color="#ffb74d" />
      </div>
      <q-toolbar-title class="text-cyan-4" style="max-width:100px;">PPH</q-toolbar-title>
    </q-toolbar>


    <q-header v-if="isLoggedIn" style="z-index: 6000;">
      <NavBar />
    </q-header>

    <q-page-container>
      <q-page>
        <div v-if="shouldDisplayButton" class="center-container">
          <router-link to="/login" >
            <q-btn outline size="xxl" color="cyan-4" class="hover-effect" icon="start" > Start</q-btn>
          </router-link>
        </div>
        <router-view />
        <UserHelper v-if="isLoggedIn" />
        <ContactForm />
      </q-page>
    </q-page-container>

    <q-footer v-if="!isLoggedIn" style="z-index: 6000;">
      <FooterBar />
    </q-footer>
  </q-layout>
</template>

<style>
 body::before {
    content:"";
    top: 0;
    right: 0;
    bottom: 0;
    left: 0;
    z-index: -1;
    position: fixed;
    background-image: url(~@/assets/img/molecule.jpg);
    background-repeat: no-repeat;
    background-size: cover;
    background-position: center center;
    background-attachment: fixed;
    opacity: 0.3;
  }

.center-container {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh; /* Prend la hauteur totale de la fenêtre de visualisation */
}

</style>

<script>
import ParticlesAnimated from '@/components/Animations/ParticlesAnimated.vue';
import { mapState, mapActions } from 'vuex';
import NavBar from "@/components/Nav/NavBar.vue";
import FooterBar from "@/components/Nav/FooterBar.vue";
import UserHelper from "@/components/UserHelper/UserHelper.vue";
import ContactForm from "@/components/Contact/ContactForm.vue";

export default {
  name: 'App',

  data() {
    return {
      interval: null,
      intentionalLogout: false,
    };
  },

  components: {
    ParticlesAnimated,
    NavBar,
    FooterBar,
    UserHelper,
    ContactForm,

  },
  computed: {
    ...mapState('auth', ['isLoggedIn']),
    shouldDisplayButton() {
        return this.$route.path === '/';
    }
  },
  methods: {
    handleFullscreenChange() {
      if (document.fullscreenElement) {
        this.$store.commit('screen/SET_FULLSCREEN', true);
      } else {
        this.$store.commit('screen/SET_FULLSCREEN', false);
      }
    },
    ...mapActions('auth', ['checkAuthentication']),
  },
  created() {
    if (this.isLoggedIn) {
      this.checkAuthentication();
      this.interval = setInterval(this.checkAuthentication, 60 * 1000);
    }
  },


watch: {
  isLoggedIn(newValue) {
    if (newValue && !this.interval) {
      this.interval = setInterval(this.checkAuthentication, 60 * 1000);
    } else if (!newValue && this.interval) {
      clearInterval(this.interval);
      this.interval = null;
    }
  },
},

  mounted() {
    document.addEventListener('fullscreenchange', this.handleFullscreenChange);
  },
  beforeUnmount() {
    document.removeEventListener('fullscreenchange', this.handleFullscreenChange);
    clearInterval(this.interval);
  },
};
</script>


