<template>
  <q-page v-if = "logged" class="row justify-center items-center">
    <div class="row justify-center q-my-xl q-py-xl">
      <atom-spinner class="bg-op-8"
        :animation-duration="1000"
        :size="100"
        :color="'#ff1d5e'"
      />
      </div>
      </q-page>
  <q-page v-else class="row  justify-center container-signup">
    <q-card class="card-signup shadow-10 col-md-3 col-xs-10">

      <q-card-section>
        <div class="row justify-center items-center">
          <div class="text-h6 text-center text-cyan-4">Connexion</div>
        </div>
      </q-card-section>

        <q-separator color="grey-7"/>

      <q-card-section>
          <UserLoginForm @submit="loginUser" />
      </q-card-section>

    </q-card>
  </q-page>
</template>

<script>
import UserLoginForm from "./UserLoginForm.vue";
import { mapMutations, mapActions, mapState } from 'vuex'
import {AtomSpinner} from 'epic-spinners'

export default {
  components: {
    UserLoginForm,
    AtomSpinner
  },
  data() {
    return {
      logged: false
    };
  },
  computed: {
    ...mapState('auth', ['isLoggedIn', 'user'])
  },
  mounted() {
    // Si l'utilisateur vient de valider son compte, affichez une notification.
    if (this.$route.query.accountActivated) {
      this.showActivatedNotification();
    }
  },
  methods: {
    ...mapMutations('error', ['SET_ERROR']),
    ...mapActions('auth', ['login']),

    async loginUser(user) {
      try {
        this.logged = true;
        await this.login(user);

        this.$store.dispatch('notifications/showNotification', {
          message: `Connexion réussie !`,
          type: 'success'
        });
        this.$store.dispatch('notifications/showNotification', {
          message: `Bienvenue ${this.user.firstName} !`,
          type: 'info'
        });
        this.$router.push({name: 'Home'});
      } catch (errorMessage) {
        this.SET_ERROR(errorMessage);
      }
      this.logged = false;
    },
    showActivatedNotification() {
      this.$store.dispatch('notifications/showNotification', {
        message: 'Votre compte est activé !',
        type: 'success'
      });
    }
  }
}
</script>







