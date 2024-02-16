<template>
  <div class="q-pa-md">
    <q-stepper
      v-model="step"
      class="bg-op-8"
      vertical
      done-color="cyan-4"
      active-color="orange-4"
      header-nav
      animated
    >
      <div class="text-h5 text-center text-cyan-4">Fiche de fabrication</div>
       <q-step
        :name="1"
        title="Patient"
        icon="personal_injury"
        :done="step > 1"
      >
  <div class="row">
        <q-input
            ref="nomInput"
            class="q-mr-lg col-3"
            v-model="name"
            label="Nom et prénom"
            color ='cyan-4'
            @mouseover="changeLabelColor('nameInput','#ffb74d')"
            @mouseleave="changeLabelColor('nameInput','')"
            @focus="onFocus('name','#4dd0e1')"
            @blur="onBlur('name')"
        >
          <template v-slot:before>
            <q-icon name="badge" color="cyan-4"/>
          </template>
        </q-input>
        <q-input
            ref="ageInput"
            class="q-mr-lg col-2"
            v-model="nom"
            label="Age"
            color ='cyan-4'
            @mouseover="changeLabelColor('nameInput','#ffb74d')"
            @mouseleave="changeLabelColor('nameInput','')"
            @focus="onFocus('name','#4dd0e1')"
            @blur="onBlur('name')"
        >
          <template v-slot:before>
            <q-icon name="badge" color="cyan-4"/>
          </template>
        </q-input>
      </div>
    <q-stepper-navigation>
      <q-btn flat @click="step = 2" color="cyan-4" label="Suivant" class="hover-effect" />
    </q-stepper-navigation>
  </q-step>

      <q-step
        :name="2"
        title="Formule"
        icon="local_pharmacy"
        :done="step > 2"
      >
      <div class="row">
        <q-select
        v-model="voie"
        color="cyan-4"
        class="col-3 hover-effect"
        label="Type"
        :options="allTypePrepLabel"
        option-label="label"
        option-value="value"
      >
        <template v-slot:before>
          <q-icon name="local_pharmacy" color="cyan-4"/>
        </template>
        </q-select>
      </div>
      <div class="row">
        <q-select
        v-model="voie"
        color="cyan-4"
        class="col-3 hover-effect"
        label="Formule"
        :options="allFormulesLabel"
        option-label="label"
        option-value="value"
      >
        <template v-slot:before>
          <q-icon name="local_pharmacy" color="cyan-4"/>
        </template>
        </q-select>
      </div>

      <q-stepper-navigation>
          <q-btn flat @click="step = 3" color="cyan-4" label="Suivant" class="hover-effect"/>
          <q-btn flat @click="step = 1" color="cyan-4" label="Précédent" class="hover-effect q-ml-sm" />
        </q-stepper-navigation>
      </q-step>

      <q-step
        :name="3"
        title="Paramètres"
        icon="settings"
        :done="step > 3"
      >
        <div class="row">
          <div class="col-8">

          </div>
        </div>

        <q-stepper-navigation>
          <q-btn flat @click="step = 4" color="cyan-4" label="Suivant" class="hover-effect"/>
          <q-btn flat @click="step = 2" color="cyan-4" label="Précédent" class="hover-effect q-ml-sm" />
        </q-stepper-navigation>
      </q-step>

      <q-step
        :name="4"
        title="Composition"
        icon="science"
        :done="step > 4"
      >
        <div class="row">
          <div class="col-12">

          </div>
        </div>

        <q-stepper-navigation>
          <q-btn flat @click="step = 3" color="cyan-4" label="Précédent" class="hover-effect"/>
          <q-btn flat @click="step = 5" color="cyan-4" label="Terminer" class="hover-effect q-ml-sm" />
        </q-stepper-navigation>
      </q-step>

      <div class="row justify-center">
        <q-btn-group>
          <q-btn flat @click="submitForm" color="green-4" label="Enregistrer" class="btn-flat-success-pph"/>
          <q-btn flat color="red-4" label="Supprimer" class="btn-flat-danger-pph"/>
        </q-btn-group>
    </div>
    </q-stepper>
  </div>
</template>

<script>

import {mapActions, mapGetters} from "vuex";

export default {
  data() {
    return {
      step: 1,
      nom: '',
      age: '',
      typePrep: null,          // Pour le Type de préparation
      modeOperatoire: '',      // Pour le Mode opératoire
    };
  },

  computed: {
    ...mapGetters('formules', ['allTypes', 'allListes']),
    ...mapGetters('voiesAdministration', ['allVoies']),

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
      const formData = {
        nom: this.name,
        type: this.typePrep,
        liste: this.liste,
        voie: this.voie,
        duree: this.duree,
        froid: this.froid,
        lumiere: this.lumiere,
        agiter: this.agiter,
        mode_operatoire: this.modeOperatoire,
        contre_indications: this.emploi,
        publications: this.publications,

      };
      this.addFormule(formData);
    },
  },
};
</script>






