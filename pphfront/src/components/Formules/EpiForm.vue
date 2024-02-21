<template>
  <div class="row">
    <div class="col-8">
  <q-form @submit.prevent="submitForm">
    <div
      v-for="(row, index) in formRows"
      :key="index"
      class="row"
    >
      <q-select
        :label="'Epi n° ' + (index + 1)"
        v-model="row.epi"
        color="cyan-4"
        class="col-6 hover-effect"
        :options="allEpiLabel"
        option-label="label"
        option-value="value"
      />
      <q-btn-group flat class="q-ml-lg">
        <q-btn flat size="sm" @click="addRow" icon="add_box" color="green-4"/>
        <q-btn flat size="sm" @click="removeRow" icon="delete_forever" color="red-4"/>
      </q-btn-group>
    </div>

    <div class="row">
      <div class="col-4">
        <q-btn flat @click="submitForm" color="green-4" class="q-mt-xs">
          Valider
        </q-btn>
      </div>
    </div>
  </q-form>
    </div>
  </div>
</template>

<script>
import { mapActions, mapGetters } from 'vuex';
import api from "../../../api";

export default {
  data() {
    return {
      selectedRowIndex: null,
      formRows: [
        {
          num_formule: null,
          epi: null,
        }
      ],
    };
  },
  computed: {
    ...mapGetters('epi', ['allEpis']),
    allEpiLabel() {
      // Calculer le libellé complet avec le nom et le fournisseur
      return this.allEpis.map(epi => ({
        ...epi,
        label: `${epi.nom}`,
        value: epi.id,
      }));
    },
  },

  async created() {
      this.loadLastId();
      this.loadEpis();

    },

  methods: {
    ...mapActions('epi', ['loadEpis', 'addEpi']),

    async loadLastId() {
      try {
        // Utilisez une API Django ou Axios pour récupérer le dernier ID + 1
        const response = await api.get('/PPH/nouvelle-formule/dernier_id');
        const dernierId = response.data.dernierId;

        // Incrémentez l'ID de 1 pour obtenir la nouvelle valeur de num_formule
        const newNumFormule = dernierId + 1;

        // Initialisez la première ligne du formulaire avec le dernier ID + 1
        this.formRows[0].num_formule = newNumFormule;
      } catch (error) {
        console.error('Erreur lors de la récupération du dernier ID de la formule', error);
      }
    },

    async addRow() {
      // Récupérez l'ID du dernier enregistrement du modèle Formule depuis votre API Django
      try {
        const response = await api.get('PPH/nouvelle-formule/dernier_id/');
        const dernierId = response.data.dernierId;

        // Incrémentez l'ID de 1 pour obtenir la nouvelle valeur de num_formule
        const newNumFormule = dernierId + 1;

        // Ajoutez une nouvelle ligne au tableau formRows avec le nouveau num_formule
        this.formRows.push({
          num_formule: newNumFormule,
          epi: null,
        });
      } catch (error) {
        console.error('Erreur lors de la récupération du dernier ID du modèle Formule', error);
      }
    },

    removeRow(row) {
      // Supprime la ligne qui contient le bouton
      const index = this.formRows.indexOf(row);
      this.formRows.splice(index, 1);
    },

    async submitForm() {
      // Préparez un tableau d'objets pour l'envoi
      const formData = this.formRows.map(row => ({
          num_formule: row.num_formule,
          epi: row.epi.id,
      }));
      console.log("Envoi de formData:", formData);

      // Appelez votre action Vuex pour ajouter les compositions
      this.addEpi(formData);
    },
  },
};
</script>


