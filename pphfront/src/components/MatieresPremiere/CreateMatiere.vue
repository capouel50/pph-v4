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
            label="Nom"
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
        v-model="typeMat"
        color="cyan-4"
        class="col-3 hover-effect"
        label="Type de matière première"
        :options="allTypeMatLabel"
        option-label="label"
        option-value="id"
      >
        <template v-slot:before>
          <q-icon name="local_pharmacy" color="cyan-4"/>
        </template>
      </q-select>
      </div>
      <div class="row">
      <q-select
        v-model="forme"
        color="cyan-4"
        class="col-2 hover-effect"
        label="Forme"
        :options="allFormeLabel"
        option-label="label"
        option-value="id"
      >
        <template v-slot:before>
          <q-icon name="gavel" color="cyan-4"/>
        </template>
      </q-select>
      </div>
    <q-stepper-navigation>
      <q-btn flat @click="step = 2" color="cyan-4" label="Suivant" class="hover-effect" />
    </q-stepper-navigation>
  </q-step>

      <q-step
        :name="2"
        title="Fournisseur"
        icon="forklift"
        :done="step > 2"
      >
      <div class="row">
        <q-select
        v-model="fournisseur"
        color="cyan-4"
        class="col-3 hover-effect"
        label="Sélectionnez un fournisseur"
        :options="allSuppliersLabel"
        option-label="label"
        option-value="value"
      >
        <template v-slot:before>
          <q-icon name="forklift" color="cyan-4"/>
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
        title="Stock"
        icon="ac_unit"
        :done="step > 3"
      >

      <div class="row">
      <q-input
        ref="prixInput"
        class="my-0 col-1"
        v-model="prix"
        label="Prix (€)"
        color ='cyan-4'
        @mouseover="changeLabelColor('nameInput','#ffb74d')"
        @mouseleave="changeLabelColor('nameInput','')"
        @focus="onFocus('name','#4dd0e1')"
        @blur="onBlur('name')"
      >
        <template v-slot:before>
          <q-icon name="alarm" color="cyan-4"/>
        </template>
      </q-input>
      </div>
      <div class="q-pa-md q-gutter-sm">
        <div>
          <q-toggle
            v-model="stock"
            color="cyan-4"
            icon="ac_unit"
            label="Stockée"
            size="md"
          />
          <q-toggle
             v-model="cdeAuto"
             color="yellow-4"
             icon="light_mode"
             label="Déclenchement des commande"
             size="md"
          />
         </div>
      </div>

        <q-stepper-navigation>
          <q-btn flat @click="step = 4" color="cyan-4" label="Suivant" class="hover-effect"/>
          <q-btn flat @click="step = 2" color="cyan-4" label="Précédent" class="hover-effect q-ml-sm" />
        </q-stepper-navigation>
      </q-step>

      <q-step
        :name="4"
        title="Réglementation"
        icon="settings"
        :done="step > 4"
      >
        <div class="row">
          <div class="col-8">

          </div>
        </div>

        <q-stepper-navigation>
          <q-btn flat @click="step = 5" color="cyan-4" label="Suivant" class="hover-effect"/>
          <q-btn flat @click="step = 3" color="cyan-4" label="Précédent" class="hover-effect q-ml-sm" />
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
      stock: false,
      cdeAuto: false,
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

    allListeLabel() {
      return this.allListes.map(liste => ({
        ...liste,
        label: `${liste.nom}`,
      }));
    },

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
    this.loadTypes();
    this.loadListes();
  },

  methods: {
    ...mapActions('formules', ['loadTypes','loadListes', 'addFormule']),
    ...mapActions('voiesAdministration', ['loadVoies']),

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






