<template>
  <q-page class="row  justify-center container-signup">
    <q-card class="card-signup shadow-10 col-md-3">

      <q-card-section>
        <div class="row justify-center items-center">
          <div class="text-h6 text-center text-cyan-4">Nouveau mot de passe</div>
        </div>
      </q-card-section>

        <q-separator color="grey-7"/>

      <q-card-section>
          <PasswordResetForm :register="register" />
      </q-card-section>

    </q-card>
  </q-page>
</template>

<script>
import { ref } from 'vue';
import axios from 'axios';
import PasswordResetForm from "./PasswordResetForm.vue";

export default {
  components: {
    PasswordResetForm
  },
  setup() {
    const email = ref('');
    const message = ref('');

    const submitForm = async () => {
      try {
        const response = await axios.post('http://localhost:8000/dj-rest-auth/password/reset/', {
          email: email.value
        });

        if (response.status === 200) {
          message.value = 'Votre demande de réinitialisation du mot de passe a été soumise.';
        }
      } catch (error) {
        console.error(error);
      }
    }

    return {
      email,
      message,
      submitForm
    };
  },
}
</script>






