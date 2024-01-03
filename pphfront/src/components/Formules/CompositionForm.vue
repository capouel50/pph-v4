<template>
  <q-form @submit.prevent="submitForm">
    <div class="row">
      <div class="col-1 text-cyan-4 text-center">Num</div>
      <div class="col-6 text-cyan-4 text-center">Matière Première</div>
      <div class="col-1 text-cyan-4 text-center">Qté</div>
      <div class="col-1 text-cyan-4 text-center">Unité</div>
    </div>
    <div
      v-for="(row, index) in formRows"
      :key="index"
      class="row"
    >
      <q-input
        square outlined
        v-model="row.num_formule"
        color="cyan-4"
        class="col-1"
      />
      <q-select
        square outlined
        v-model="row.matiere"
        color="cyan-4"
        class="col-6 hover-effect"
        :options="allMatieresLabel"
        option-label="label"
        option-value="id"
      />
      <q-input
        square outlined
        v-model="row.qté"
        color="cyan-4"
        class="col-1 bd-hover-effect text-center"
      />
      <q-select
        square outlined
        v-model="row.unite"
        color="cyan-4"
        class="col-1 hover-effect text-center"
        :options="allUnitesMesure"
        option-label="label"
        option-value="id"
      />
      <q-btn-group flat class="q-ml-lg">
        <q-btn flat size="sm" @click="addRow" icon="check_circle" color="cyan-4" class="hover-effect-success"/>
        <q-btn flat size="sm" @click="removeRow" icon="delete_forever" color="cyan-4" class="hover-effect-warning"/>
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
</template>

<script>
import { mapActions, mapGetters } from 'vuex';
import api from '../../../api';

export default {
  data() {
    return {
      filteredRecords: [],
      selectedRowIndex: null,
      formRows: [
        {
          num_formule: null,
          matiere: null,
          qté: '',
          unite: null
        }
      ],
    };
  },
  computed: {
    ...mapGetters('matieresPremieres', ['allMatieres', 'allUnites']),
    allMatieresLabel() {
      // Calculer le libellé complet avec le nom et le fournisseur
      return this.allMatieres.map(matiere => ({
        ...matiere,
        label: `${matiere.nom} ${matiere.qté_cdt}${matiere.forme.unite_mesure.nom} - ${matiere.forme.nom} - ${matiere.fournisseur.name}`,
        id: `${matiere.id}`,
      }));
    },
    allUnitesMesure() {
      // Calculer le libellé complet avec le nom et le fournisseur
      return this.allUnites.map(unite => ({
        ...unite,
        label: `${unite.nom}`,
      }));
    },
  },

  async created() {
      this.loadMatieresPremieres();
      this.loadUnites();
      this.loadLastId();
    },

  methods: {
    ...mapActions('matieresPremieres', ['loadMatieresPremieres', 'loadUnites']),
    ...mapActions('formules', ['addComposition']),

    async addRow() {
      try {
        const response = await api.get('PPH/nouvelle-formule/dernier_id/');
        const dernierId = response.data.dernierId;

        const newNumFormule = dernierId + 1;

        this.formRows.push({
          num_formule: newNumFormule,
          matiere: null,
          qté: '',
          unite: null
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
      this.filterAndShowRecords();
    },

    async filterAndShowRecords() {
      if (this.formRows[0].num_formule !== null) {
        try {
          const response = await api.get(`/PPH/composition/filter/${this.formRows[0].num_formule}`);
          this.filteredRecords = response.data;
          console.log('Enregistrements filtrés :', this.filteredRecords);

          this.updateFormWithFilteredRecords();
        } catch (error) {
          console.error('Erreur lors de la récupération des enregistrements filtrés', error);
        }
      } else {
        console.warn('Veuillez d\'abord remplir le champ num_formule dans le formulaire.');
      }
    },

    updateFormWithFilteredRecords() {
    this.formRows = this.filteredRecords.map((record) => {
      const { num_formule, matiere, qté, unite } = record;

      // Recherchez la matière dans la liste complète
      const matiereDetails = this.allMatieres.find(item => item.id === matiere);

      // Recherchez l'unité dans la liste complète
      const uniteDetails = this.allUnites.find(item => item.id === unite);

      // Assurez-vous que les détails sont disponibles
      if (matiereDetails && uniteDetails) {
        return {
          num_formule,
          matiere: matiereDetails.nom, // Assurez-vous d'ajuster cela en fonction de votre structure réelle
          qté,
          unite: uniteDetails.nom, // Assurez-vous d'ajuster cela en fonction de votre structure réelle
        };
      }

      return null;
    });

    this.formRows = this.formRows.filter(row => row !== null);
  },


    async submitForm() {
      // Récupérez les données de toutes les lignes
      const formData = {
        compositions: this.formRows.map(row => ({
          num_formule: row.num_formule,
          matiere: row.matiere.id,
          qté: row.qté,
          unite: row.unite.id,
        })),
      };

      // Appelez votre action Vuex pour ajouter les compositions
      this.addComposition(formData);
    },
  },
};
</script>


