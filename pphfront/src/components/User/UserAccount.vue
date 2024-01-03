<template>
  <q-page class="container">
    <div class="row justify-center">
      <div class="col-12">
        <h5 class="text-cyan-4 q-mb-lg text-center">Mon compte utilisateur</h5>
        <UserAccountForm :userData="this.$store.getters.user" />
      </div>
    </div>
  </q-page>
</template>

<script>
import UserAccountForm from './UserAccountForm.vue';
export default {
  components: {
    UserAccountForm
  },
  data() {
    return {
      error: null,
      formSubmitted: false,
    };
  },
  mounted() {
  this.$store.dispatch('fetchUserData');
  },
}
</script>

