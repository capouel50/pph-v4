<template v-if="isLoggedIn">
  <q-page class="container">
    <div class="row justify-center">
      <div class="col-12">
        <h5 class="text-cyan-4 q-mb-lg text-center">Profil utilisateur</h5>
        <UserProfilForm />
      </div>
    </div>
  </q-page>
</template>

<script>
import UserProfilForm from './UserProfilForm.vue';
export default {
  components: {
    UserProfilForm
  },
  data() {
    return {
      error: null,
      formSubmitted: false,
    };
  },
}
</script>

