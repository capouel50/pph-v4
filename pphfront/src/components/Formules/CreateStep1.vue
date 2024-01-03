<template>
  <q-step
        :name="1"
        title="Identification"
        icon="info"
        :done="step > 1"
      >
  <div class="row">
        <q-input
            ref="nomInput"
            class="q-mr-lg col-3"
            v-model="name"
            label="Nom de la formule"
            color ='cyan-4'
            @mouseover="changeLabelColor('nameInput','#ffb74d')"
            @mouseleave="changeLabelColor('nameInput','')"
            @focus="onFocus('name','#4dd0e1')"
            @blur="onBlur('name')"
        >
          <template v-slot:before>
            <q-icon name="local_pharmacy" color="cyan-4"/>
          </template>
        </q-input>

        <q-select
        v-model="typePrep"
        color="cyan-4"
        class="col-3 hover-effect"
        label="Type de préparation"
        :options="allTypePrepLabel"
        option-label="label"
        option-value="value"
      >
        <template v-slot:before>
          <q-icon name="local_pharmacy" color="cyan-4"/>
        </template>
      </q-select>
      </div>
    <q-stepper-navigation>
      <q-btn flat @click="validateAndNext" color="cyan-4" label="Suivant" class="hover-effect" />
    </q-stepper-navigation>
  </q-step>
</template>

<script>
import { mapActions, mapGetters } from 'vuex';

export default {
  name: "CreateStep1",

  computed: {
    ...mapGetters('formules', ['allTypes']),

    allTypePrepLabel() {
      // Calculer le libellé complet avec le nom et le fournisseur
      return this.allTypes.map(type => ({
        ...type,
        label: `${type.nom}`,
      }));
    },
  },

  created() {
    this.loadTypes();
  },

  methods: {
    ...mapActions('formules', ['loadTypes']),


    async submitForm() {
      // Vous pouvez maintenant utiliser this.matieres ici
    },
  },
};
</script>

<style scoped>

</style>