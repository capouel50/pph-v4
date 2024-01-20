<template>
  <q-form @submit.prevent="submitForm">
    <div class="row">
      <div class="col-3 text-cyan-4 text-center">Matière Première</div>
      <div class="col-1 text-cyan-4 text-center">Qté</div>
      <div class="col-1 text-cyan-4 text-center">Unité</div>
      <div class="col-5 text-cyan-4 text-center">Calcul</div>
    </div>
    <div
      v-for="(row, index) in formRows"
      :key="index"
      class="row"
    >
      <q-select
        square outlined
        v-model="row.matiere"
        color="cyan-4"
        class="col-3 hover-effect"
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
      <q-input
          v-model="row.calculInput"
          square outlined
          color="cyan-4"
          class="col-5 bd-hover-effect text-center"
      >
        <template v-slot:append>
          <q-avatar>
            <q-btn flat size="md" @click="openCalculDialog(index)" icon="calculate" color="cyan-4" class="hover-effect"/>
          </q-avatar>
        </template>
      </q-input>
      <q-btn-group flat class="q-ml-lg">
        <q-btn flat size="sm" @click="addRow" icon="check_circle" color="green-4" class="hover-effect-success"/>
        <q-btn flat size="sm" @click="removeRow" icon="delete_forever" color="red-4" class="hover-effect-warning"/>
      </q-btn-group>
      <q-dialog v-model="calculDialog">
      <q-card>
        <q-card-section>
          <div class="row text-subtitle1 text-cyan-4 justify-center">
            Calcul pour {{ formRows[selectedRowIndex].matiere.nom }}
          </div>
        </q-card-section>
        <q-separator/>
        <q-card-section>
          <div class="row text-orange-4 text-subtitle2 justify-center">Paramètres de calcul</div>
          <q-card-actions>
            <div class="row justify-center">
            <div v-for="(parametre, index) in filteredParametresFormules" :key="index">
              <q-btn
                flat
                color="cyan-4"
                class="hover-effect"
                :label="parametre.label"
                @Click="inputParametre(parametre)"
              />
            </div>
              <q-btn
                flat
                color="cyan-4"
                class="hover-effect"
                label="Quantité"
                @Click="inputParametre(parametreFormule.label)"
              />
            </div>
          </q-card-actions>
        </q-card-section>
        <q-separator/>
        <q-card-section>
          <q-input
              v-model="row.calcul"
          />
        </q-card-section>
        <q-separator/>
        <q-card-section>
          <div class="row justify-center">
          <q-btn-group>
          <q-btn
            flat
            color="green-4"
            label="Valider"
            @click="validerCalcul"
          />
          <q-btn
            flat
            class="hover-effect"
            color="cyan-4"
            label="Effacer"
            @click="effacerCalcul"
          />
          <q-btn
            flat
            color="red-4"
            label="Annuler"
            @click="calculDialog = false"
          />
          </q-btn-group>
          </div>
        </q-card-section>
      </q-card>
      </q-dialog>
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
      calculDialog: false,
      enregistrements: [],
      selectedRowIndex: null,
      calculDetails: [],
      formRows: [
        {
          num_formule: null,
          matiere: null,
          qté: '',
          unite: null,
          calcul: '',
          calculInput: '',
        }
      ],
    };
  },
  computed: {
    ...mapGetters('matieresPremieres', ['allMatieres', 'allUnites']),
    ...mapGetters('formules', ['allParametres', 'allParametresFormules']),

    filteredParametresFormules() {
      if (this.selectedRowIndex !== null) {
        const numFormule = this.formRows[this.selectedRowIndex].num_formule;
        const allParametresDetails = this.allParametres; // Assurez-vous que ceci contient les détails complets des paramètres

        return this.allParametresFormules
          .filter(pf => pf.num_formule.toString() === numFormule.toString())
          .map(pf => {
            const parametreDetail = allParametresDetails.find(p => p.id === pf.parametre);
            return {
              ...pf,
              label: parametreDetail ? `${parametreDetail.nom} - ${parametreDetail.unite}` : 'Inconnu',
              id: pf.parametre
            };
          });
      }
      return [];
    },

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
      await this.loadMatieresPremieres();
      await this.loadUnites();
      await this.loadParametresFormules();
      await this.createNewNumCompo();
    },

  methods: {
    ...mapActions('matieresPremieres', ['loadMatieresPremieres', 'loadUnites']),
    ...mapActions('formules', ['addComposition']),
    ...mapActions('formules', ['loadParametresFormules']),

    validerCalcul() {
      if (this.selectedRowIndex !== null) {
        this.formRows[this.selectedRowIndex].calculInput = this.formRows[this.selectedRowIndex].calcul;
        let calculTransforme = this.formRows[this.selectedRowIndex].calcul;

        // Remplacer chaque label par son ID correspondant
        this.calculDetails.forEach(detail => {
          const regex = new RegExp(detail.label, 'g');
          calculTransforme = calculTransforme.replace(regex, detail.id);
        });

        // Mettre à jour le calcul dans formRows
        this.formRows[this.selectedRowIndex].calcul = calculTransforme;
      }

      // Réinitialiser les détails du calcul et fermer le dialogue
      this.calculDetails = [];
      this.calculDialog = false;
    },

    openCalculDialog(rowIndex) {
      this.selectedRowIndex = rowIndex;
      this.calculDialog = true;
      if (this.formRows[this.selectedRowIndex].calculInput){
        this.formRows[this.selectedRowIndex].calcul = this.formRows[this.selectedRowIndex].calculInput
      }
    },

    inputParametre(parametre) {
      console.log("Paramètre reçu :", parametre);

      if (this.selectedRowIndex !== null && this.formRows[this.selectedRowIndex]) {
        // Ajouter le label à l'input visible
        this.formRows[this.selectedRowIndex].calcul += parametre.label;

        // Ajouter les détails du paramètre pour le remplacement ultérieur
        this.calculDetails.push({
          label: parametre.label,
          id: parametre.id
        });
      }
    },

    effacerCalcul() {
      this.formRows[this.selectedRowIndex].calcul = " ";
    },

    removeRow(row) {
      // Supprime la ligne qui contient le bouton
      const index = this.formRows.indexOf(row);
      this.formRows.splice(index, 1);
    },

    async createNewNumCompo() {
      try {
        const response = await api.get('/PPH/nouvelle-formule/dernier_id');
        const dernierId = response.data.dernierId;
        const newNumFormule = dernierId + 1;
        console.error('dernier id', newNumFormule);
        if (this.formRows.length === 0 || this.formRows[0].num_formule === null) {
          this.formRows[0].num_formule = newNumFormule;
        }
      } catch (error) {
        console.error('Erreur lors de la récupération du dernier ID de la formule', error);
      }
    },

    async loadRecords() {
      try {
        // Assurez-vous que le dernier numéro de formule est chargé
        const dernierNumFormule = await this.createNewNumCompo();

        // Faites l'appel API en passant le dernier numéro de formule
        const response = await api.get(`/PPH/composition/filter/${dernierNumFormule}`);
        this.enregistrements = response.data;
        console.log('Enregistrements chargés:', this.enregistrements);
      } catch (error) {
        console.error('Erreur lors du chargement des enregistrements:', error);
        // Gérer l'erreur comme il convient
      }
    },

    async updateFilteredRecords() {
      const NumFormule = await this.createNewNumCompo(); // Assurez-vous que cette méthode renvoie le dernier numéro

      const enregistrementsFiltres = this.enregistrements.filter(enregistrement => {
        return enregistrement.num_formule === NumFormule;
      });

      if (enregistrementsFiltres.length === 0) {
        // S'il n'y a pas d'enregistrements correspondants, exécutez addRow()
        this.addRow();
      } else {
        // Sinon, mettez à jour formRows avec les enregistrements filtrés
        this.formRows = enregistrementsFiltres.map(enregistrement => {
          return {
            num_formule: enregistrement.num_formule,
            matiere: enregistrement.matiere,
            qté: enregistrement.qté,
            unite: enregistrement.unite,
            calcul: enregistrement.calcul
            // ... autres propriétés nécessaires
          };
        });
      }
    },

    async addRow() {
      try {
        const newNumFormule = await this.createNewNumCompo();

        this.formRows.push({
          num_formule: newNumFormule,
          matiere: null,
          qté: '',
          unite: null,
          calcul: ''
        });
      } catch (error) {
        console.error('Erreur lors de la récupération du dernier ID du modèle Formule', error);
      }
    },

    async submitForm() {
      // Récupérez les données de toutes les lignes
      const formData = {
        compositions: this.formRows.map(row => ({
          num_formule: row.num_formule,
          matiere: row.matiere.id,
          qté: row.qté,
          unite: row.unite.id,
          calcul: row.calcul
        })),
      };

      // Appelez votre action Vuex pour ajouter les compositions
      this.addComposition(formData);
    },
  },
};
</script>


