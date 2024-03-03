<template>
  <div class="row">
    <div class="col-8">

    <div
      v-for="(row, index) in formRows"
      :key="index"
      class="row"
    >
      <q-select
        :label="row.parametre ? 'Paramètre n° ' + (index + 1) : 'Ajouter un paramètre'"
        v-model="row.parametre"
        color="cyan-4"
        class="col-6 hover-effect"
        :options="!formuleId && getParametres.length ? allParametresStateLabel : allParametresLabel"
        option-label="label"
        option-value="value"
        @change="addParametreState(row)"
      >
        <template v-slot:append v-if="!row.parametre">
          <q-btn flat @click="parametreDialog=true" icon="add_box" color="green-4" class="q-px-none hover-effect"/>
        </template>
      </q-select>
      <q-dialog v-model="parametreDialog">
      <q-card>
        <q-card-section>
          <div class="row text-subtitle1 text-cyan-4 justify-center">
            Créer un paramètre
          </div>
        </q-card-section>
        <q-separator/>
        <q-card-section>
          <div class="row">
            <q-input
            v-model="parametre"
            label="Nom"
            color ='cyan-4'
            @mouseover="changeLabelColor('nameInput','#ffb74d')"
            @mouseleave="changeLabelColor('nameInput','')"
            @focus="onFocus('name','#4dd0e1')"
            @blur="onBlur('name')"
          />
          </div>
          <div class="row">
            <q-input
            v-model="unite"
            label="Unité"
            color ='cyan-4'
            @mouseover="changeLabelColor('nameInput','#ffb74d')"
            @mouseleave="changeLabelColor('nameInput','')"
            @focus="onFocus('name','#4dd0e1')"
            @blur="onBlur('name')"
          />
          </div>
        </q-card-section>
        <q-separator/>
        <div class="row justify-center">
        <q-btn flat @click="validerParametre" label="Créer" color="green-4"/>
        <q-btn flat @click="parametreDialog=false" label="Annuler" color="red-4"/>
        </div>
      </q-card>
     </q-dialog>
      <q-btn-group flat class="q-ml-lg">
        <q-btn flat size="sm" @click="addParametreState(row)" icon="check_circle" color="green-4"/>
        <q-btn flat size="sm" @click="removeRow(row)" icon="delete_forever" color="red-4"/>
      </q-btn-group>
    </div>

    </div>
  </div>
</template>

<script>
import {mapActions, mapGetters, mapMutations} from 'vuex';

export default {
  props: ['newId', 'formuleId'],
  data() {
    return {
      parametre: "",
      unite: '',
      parametreDialog: false,
      selectedRowIndex: null,
      formRows: [
        {
          num_formule: null,
          parametreId: null,
          parametre: null,
          unite: null,
        }
      ],
    };
  },
  computed: {
    ...mapGetters('formules', ['allParametres', 'allParametresFormules']),
    allParametresLabel() {
        return this.allParametres.map(parametre => ({
        ...parametre,
        label: `${parametre.nom} - ${parametre.unite}`,
        value: parametre.id,
      }));
    },
    allParametresStateLabel() {
        return this.allParametresFormules
            .filter(parametre => parametre.num_formule === this.newId)
            .map(parametre => ({
              label: `${parametre.parametre} - ${parametre.unite}`,
              value: parametre.parametreId,
        }));
    },

  },

  async created() {
      this.loadLastId();
      this.loadParametres();
      this.fetchParametresAndAddRow();
      if(this.formuleId){
        this.loadParametresFormules();
        // Here we reset formRows and repopulate it if formuleId is set
          this.formRows = this.allParametresFormules
            .filter(parametre => parametre.num_formule === this.formuleId)
            .map(parametre => ({
              num_formule: parametre.num_formule,
              parametreId: parametre.parametre.id,
              parametre: `${parametre.parametre.nom} - ${parametre.parametre.unite}`,
              unite: parametre.parametre.unite,
            }));
          this.addRow();
        }
    },

  watch: {
      parametre: 'addParametreState',
  },

  methods: {
    ...mapActions('formules', ['loadParametres', 'loadParametresFormules', 'addParametre']),
    ...mapMutations('formules', ['ADD_PARAMETRE', 'REMOVE_PARAMETRE']),

    async validerParametre(){
      const formData = {
        nom: this.parametre,
        unite: this.unite,
      };
      console.log(formData);
      await this.addParametre(formData);
      this.parametreDialog=false;
    },

    async fetchParametresAndAddRow() {
        if (!this.formuleId) {
          try {
            const parametres = await this.getParametres();
            if (parametres.length > 0) {
              this.formRows = parametres.map((parametre) => ({
                num_formule: parametre.num_formule,
                parametreId: parametre.parametreId,
                parametre: parametre.parametre,
                unite: parametre.unite,
              }));
              this.addRow();
            }
          } catch (error) {
            console.error('Erreur lors de la récupération des paramètres', error);
          }
        }
      },

    async getParametres() {
      const numFormule = this.newId;

      return this.allParametresFormules.filter(parametre => parametre.num_formule === numFormule);
    },

    async loadLastId() {
      try {
        this.formRows[0].num_formule = this.newId;
        console.log('NewId', this.newId)
      } catch (error) {
        console.error('Erreur lors de la récupération du dernier ID de la formule', error);
      }
    },

    async addRow() {
      try {
        if(this.formuleId){
          this.formRows.push({
          num_formule: this.formuleId,
          parametreId: null,
          parametre: null,
          unite: null,
        });
        }else {
          this.formRows.push({
            num_formule: this.newId,
            parametre: null,
            parametereId: null,
            unite: null,
          });
        }
      } catch (error) {
        console.error('Erreur lors de la récupération du dernier ID du modèle Formule', error);
      }
    },

    addParametreState(row) {
        this.ADD_PARAMETRE({
          num_formule: row.num_formule,
          parametreId: row.parametre.value,
          parametre: row.parametre.label,
          unite: row.parametre.unite,
        });
      if(this.formRows.indexOf(row) === this.formRows.length - 1) {
        this.addRow();
      }
    },

    removeRow(row) {
      this.REMOVE_PARAMETRE({
        num_formule: row.num_formule,
        parameteId: row.parametreId,
      });
      // Supprime la ligne qui contient le bouton
      const index = this.formRows.indexOf(row);
      this.formRows.splice(index, 1);
    },

  },
};
</script>


