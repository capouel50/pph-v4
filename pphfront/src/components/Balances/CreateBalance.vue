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
      <div v-if="balanceId" class="text-h5 text-center text-cyan-4">{{ balance.nom }}</div>
      <div v-else class="text-h5 text-center text-cyan-4">Nouvelle Balance</div>
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
            v-model="nom"
            label="Nom de la balance"
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

          <q-input
            v-model="modele"
            color="cyan-4"
            class="col-3 hover-effect"
            label="Modèle"
          >
            <template v-slot:before>
              <q-icon name="local_pharmacy" color="cyan-4"/>
            </template>
          </q-input>
        </div>
        <div class="row">
          <q-select
            v-model="fabricant"
            color="cyan-4"
            class="col-2 hover-effect"
            label="Fabricant"
            :options="allSupplierLabel"
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
        title="Calibration"
        icon="calendar_month"
        :done="step > 2"
      >

      <div class="row">
        <q-input
        ref="dureeInput"
        type="date"
        class="my-0 col-2"
        v-model="date_calibration"
        label="Dernière calibration"
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
      <div class="row">
        <q-input
        ref="dureeInput"
        class="my-0 col-2"
        v-model="duree_calibration"
        label="Validitée"
        color ='cyan-4'
        @mouseover="changeLabelColor('nameInput','#ffb74d')"
        @mouseleave="changeLabelColor('nameInput','')"
        @focus="onFocus('name','#4dd0e1')"
        @blur="onBlur('name')"
      >
        <template v-slot:append>
          <div class="text-cyan-4 q-pt-md text-subtitle2">mois</div>
        </template>
        <template v-slot:before>
          <q-icon name="alarm" color="cyan-4"/>
        </template>
      </q-input>
      </div>
      <div class="q-pa-md q-gutter-sm">
        <div>
          <q-toggle
            v-model="blocage_calibration"
            color="green-4"
            icon="stop"
            label="Autoriser dépassement de date"
            size="md"
          />
         </div>
      </div>

        <q-stepper-navigation>
          <q-btn flat @click="step = 1" color="cyan-4" label="Précédent" class="hover-effect q-ml-sm" />
          <q-btn flat @click="step = 3" color="cyan-4" label="Suivant" class="hover-effect"/>
        </q-stepper-navigation>
      </q-step>

      <q-step
        :name="3"
        title="Instructions"
        icon="biotech"
        :done="step > 3"
      >
        <div class="row">
          <div class="col-12">
            <InstructionsForm v-if="step === 3" :newId="newId" :balanceId="balanceId"/>
          </div>
        </div>

        <q-stepper-navigation>
          <q-btn flat @click="step = 2" color="cyan-4" label="Précédent" class="hover-effect q-ml-sm" />
          <q-btn flat @click="step = 4" color="cyan-4" label="Suivant" class="hover-effect"/>
        </q-stepper-navigation>
      </q-step>

      <div class="row justify-center">
        <q-btn-group>
          <q-btn flat @click="submitForm" color="green-4" label="Enregistrer" class="btn-flat-success-pph"/>
        </q-btn-group>
    </div>
    </q-stepper>
  </div>
</template>

<script>
import InstructionsForm from './InstructionsForm.vue';
import {mapActions, mapGetters } from "vuex";

export default {
  components: {
    InstructionsForm,
  },
  data() {
    return {
      step: 1,
      newId: '',
      balanceId: '',
      nom: '',
      modele: '',
      fabricant: '',
      date_calibration: '',
      duree_calibration: '',
      blocage_calibration: false,
      balance: [],
    };
  },

  computed: {
    ...mapGetters('suppliers', ['allSuppliers']),
    ...mapGetters('balances', ['allBalances']),

    allSuppliersLabel() {
      return this.allSuppliers
          .map(supplier => ({
        ...supplier,
        label: supplier.name,
        id: supplier.id,
      }));
    },
  },

  async created() {
    await this.loadSuppliersBalances();
    await this.loadBalances();
    if(this.$route.params.id){
      this.balanceId = Number(this.$route.params.id);
      this.balance = this.allBalances.find(balance => balance.id === this.balanceId);
      this.nom = this.balance.nom;
      this.modele = this.balance.modele;
      this.fabricant = this.balance.fabricant.name;
      this.date_calibration = this.balance.calibration;
      this.duree_calibration = this.balance.duree_calibration;
      this.blocage_calibration = this.balance.bloque_calibration;
    }
    this.newId = this.allBalances.length;
  },

  methods: {
    ...mapActions('suppliers', ['loadSuppliersBalances']),
    ...mapActions('balances', ['addBalance', 'loadBalances']),

    addBalance() {
      const formData = {
        nom: this.nom,
        modele: this.modele,
        fabricant: this.fabricant,
        calibration: this.calibration,
        duree_calibration: this.duree_calibration,
        blocage_calibration: this.blocage_calibration,
      };
      this.addBalance(formData);
    }

  },
};
</script>






