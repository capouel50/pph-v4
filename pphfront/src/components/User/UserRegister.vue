<template>
  <q-page class="row  justify-center container-signup">
    <q-card class="card-signup shadow-10 col-md-3">

      <q-card-section>
        <div class="row justify-center items-center">
          <div class="text-h6 text-center text-cyan-4">Inscription</div>
        </div>
      </q-card-section>

        <q-separator color="grey-7"/>

      <q-card-section>
        <div v-if="!formSubmitted">
          <UserRegisterForm :register="register" />
        </div>
        <div v-else>
          <div class="row justify-center q-my-md">
            <q-icon size="10em" name="check_circle" color="green-4"/>
          </div>
          <div class="row justify-center q-mt-lg text-cyan-4 pph-link">
            <router-link class="q-mx-md text-cyan-4 pph-link" to="/login">Déjà inscrit ? Connectez-vous</router-link>
          </div>
        </div>
      </q-card-section>

    </q-card>
  </q-page>
</template>

<script>
import UserRegisterForm from './UserRegisterForm.vue'
import api from '../../../api';

export default {
  components: {
    UserRegisterForm
  },
  data() {
    return {
      error: null,
      formSubmitted: false,
    };
  },
  methods: {
    register(user) {
      api.post('/accounts/register/', user, {
        headers: {
          'Content-Type': 'application/json'
        }
      })
      .then(() => {
        this.$q.notify({
          message: 'Inscription réussie !\n Un mail de confirmation\nvient de vous être envoyé.',
          icon: 'announcement',
          color: 'green-4',
          timeout: 10000,
          position: 'top-right',
        });
        this.formSubmitted = true;
      })
      .catch(err => {
        if (err.response && err.response.status === 400) {
          this.error = err.response.data; // Mettre à jour la donnée 'error'
        }
        this.$q.notify({
          message: 'Échec de l\'inscription.',
          icon: 'warning amber',
          color: 'red-3',
          timeout: 5000,
          position: 'top-right',
        });
      });
    },
  }
}
</script>






