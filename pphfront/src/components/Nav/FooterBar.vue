<template>
  <q-footer class="bg-blue-grey-3">
    <div class="row justify-center">
      <div class="justify-center">
        <router-link to="cgu/" class="hover-effect pph-link text-cyan-1">CGU</router-link>
          <div color="cyan-1" class="q-mx-sm inline-block">|</div>
        <router-link to="mentions/" class="hover-effect pph-link text-cyan-1">Mentions légales</router-link>
          <div color="cyan-1" class="q-mx-sm inline-block">|</div>
        <router-link to="cookies/" class="hover-effect pph-link text-cyan-1">Politique cookies</router-link>
          <div color="cyan-1" class="q-mx-sm inline-block">|</div>
        <router-link to="confidential/" class="hover-effect pph-link text-cyan-1">Politique de confidentialité</router-link>
      </div>
    </div>
  </q-footer>
</template>

<script>
export default {
  name: 'FooterBar'
}
</script>

<style scoped>
/* Ajoutez des styles supplémentaires ici si nécessaire */
</style>
