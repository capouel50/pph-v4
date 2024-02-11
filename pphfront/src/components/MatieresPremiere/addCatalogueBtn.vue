<template>
  <q-fab glossy class="btn-grey-primary-pph" icon="add_box" direction="right">
    <q-fab-action glossy class="btn-grey-primary-pph" @click="importCatalogue=true" icon="playlist_add" />
    <q-fab-action glossy class="btn-grey-primary-pph" @click="importCatalogue=true" icon="post_add" />
  </q-fab>
</template>

<script>
import { mapState } from 'vuex';

export default {
  name: "addCatalogueBtn",

  computed: {
    ...mapState('contact', ['showForm'])
  },

};
</script>


<style scoped>
.q-fab {
  bottom: 10px; /* ou la marge que vous souhaitez depuis le bas de l'écran */
  right: 10px; /* ou la marge que vous souhaitez depuis le côté droit de l'écran */
  z-index: 10000; /* assurez-vous qu'il passe par-dessus les autres éléments, ajustez si nécessaire */
}
</style>