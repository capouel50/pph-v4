<template>
        <div class="row">
        <q-select
        v-model="voie"
        color="cyan-4"
        class="col-3 hover-effect"
        label="Sélectionnez la voie"
        :options="allVoiesLabel"
        option-label="label"
        option-value="value"
      >
        <template v-slot:before>
          <q-icon name="vaccines" color="cyan-4"/>
        </template>
        </q-select>
      </div>
</template>

<script>
import {mapActions, mapGetters} from "vuex";

export default {
  name: "CreateStep2",

  computed: {
    ...mapGetters('voiesAdministration', ['allVoies']),
    allVoiesLabel() {
      // Calculer le libellé complet avec le nom et le fournisseur
      return this.allVoies.map(voie => ({
        ...voie,
        label: `${voie.nom}`,
      }));
    },
  },

  created() {
    this.loadVoies();
  },

  methods: {
    ...mapActions('voiesAdministration', ['loadVoies']),
  },
};
</script>

<style scoped>

</style>