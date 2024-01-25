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
      <div class="row text-h6 justify-center text-cyan-4">Matière première</div>
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
        v-model="type"
        color="cyan-4"
        class="col-3 hover-effect"
        label="Type"
        :options="allTypeLabel"
        option-label="label"
        option-value="id"
      >
        <template v-slot:before>
          <q-icon name="medication" color="cyan-4"/>
        </template>
        <template v-slot:append>
          <q-btn flat @click="typeDialog=true" icon="add_box" color="green-4" class="hover-effect"/>
        </template>
      </q-select>

       <q-dialog v-model="typeDialog">
      <q-card>
        <q-card-section>
          <div class="row text-subtitle1 text-cyan-4 justify-center">
            Ajouter un type de matière première
          </div>
        </q-card-section>
        <q-separator/>
        <q-card-section>
          <q-input
            v-model="typeMat"
            label="Type"
            color ='cyan-4'
            @mouseover="changeLabelColor('nameInput','#ffb74d')"
            @mouseleave="changeLabelColor('nameInput','')"
            @focus="onFocus('name','#4dd0e1')"
            @blur="onBlur('name')"
          />
        </q-card-section>
        <q-separator/>
        <div class="row justify-center">
        <q-btn flat @click="validerType" label="Ajouter" color="green-4"/>
        <q-btn flat @click="typeDialog=false" label="Annuler" color="red-4"/>
        </div>
      </q-card>
     </q-dialog>
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
        @input="updateForme"
      >
        <template v-slot:before>
          <q-icon name="medication_liquid" color="cyan-4"/>
        </template>
        <template v-slot:append>
          <q-btn flat @click="formeDialog=true" icon="add_box" color="green-4" class="hover-effect"/>
        </template>
      </q-select>

        <q-dialog v-model="formeDialog">
      <q-card>
        <q-card-section>
          <div class="row text-subtitle1 text-cyan-4 justify-center">
            Ajouter une forme de matière première
          </div>
        </q-card-section>
        <q-separator/>
        <q-card-section>
          <q-input
            v-model="formeMat"
            label="Forme"
            color ='cyan-4'
            @mouseover="changeLabelColor('nameInput','#ffb74d')"
            @mouseleave="changeLabelColor('nameInput','')"
            @focus="onFocus('name','#4dd0e1')"
            @blur="onBlur('name')"
          /><br/>
          <div class="row">
            <div class="text-cyan-4">Unités : </div>
          </div>
          <div class="row">
           <q-select
            v-model="uniteStock"
            color="cyan-4"
            class="col-4 hover-effect"
            label="Stock"
            :options="allUniteLabel"
            option-label="label"
            option-value="id"
          />

           <q-select
            v-model="uniteMes"
            color="cyan-4"
            class="col-4 offset-1 hover-effect"
            label="Mesure"
            :options="allUniteLabel"
            option-label="label"
            option-value="id"
          />
          </div>
        </q-card-section>
        <q-separator/>
        <div class="row justify-center">
        <q-btn flat @click="validerForme" label="Ajouter" color="green-4"/>
        <q-btn flat @click="formeDialog=false" label="Annuler" color="red-4"/>
        </div>
      </q-card>
     </q-dialog>
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
        option-value="id"
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
        title="Conditionnement"
        icon="science"
        :done="step > 3"
      >
      <div class="row">
        <div class="col-8">
          <div class="row">
      <q-select
        v-model="cdt"
        color="cyan-4"
        class="col-3 hover-effect"
        label="Conditionnement"
        :options="allCdtLabel"
        option-label="label"
        option-value="id"
      >
        <template v-slot:append>
          <q-btn flat @click="cdtDialog=true" icon="add_box" color="green-4" class="hover-effect"/>
        </template>

        <template v-slot:before>
          <font-awesome-icon icon="fa-solid fa-prescription-bottle" style="color: #4dd0e1;"/>
        </template>
        </q-select>
            <q-dialog v-model="cdtDialog">
          <q-card>
            <q-card-section>
              <div class="row text-subtitle1 text-cyan-4 justify-center">
                Ajouter un conditionnement
              </div>
            </q-card-section>
            <q-separator/>
            <q-card-section>
              <q-input
                v-model="cdtMat"
                label="Type"
                color ='cyan-4'
                @mouseover="changeLabelColor('nameInput','#ffb74d')"
                @mouseleave="changeLabelColor('nameInput','')"
                @focus="onFocus('name','#4dd0e1')"
                @blur="onBlur('name')"
              />
            </q-card-section>
            <q-separator/>
            <div class="row justify-center">
            <q-btn flat @click="validerCdt" label="Ajouter" color="green-4"/>
            <q-btn flat @click="cdtDialog=false" label="Annuler" color="red-4"/>
            </div>
          </q-card>
         </q-dialog>
        </div>
          <div class="row">
        <q-input
        ref="qteInput"
        class="my-0 col-2"
        v-model="qté_cdt"
        label="Quantité cdt"
        color ='cyan-4'
        @mouseover="changeLabelColor('nameInput','#ffb74d')"
        @mouseleave="changeLabelColor('nameInput','')"
        @focus="onFocus('name','#4dd0e1')"
        @blur="onBlur('name')"
      >
        <template v-slot:append>
          <div class="uniteStockName text-subtitle2 text-cyan-4">{{ uniteStockNom }}</div>
        </template>
        <template v-slot:before>
          <font-awesome-icon icon="fa-solid fa-weight-scale" style="color: #4dd0e1;"/>
        </template>
        </q-input>
            </div>
          </div>
        </div>

        <q-stepper-navigation>
          <q-btn flat @click="step = 4" color="cyan-4" label="Suivant" class="hover-effect"/>
          <q-btn flat @click="step = 2" color="cyan-4" label="Précédent" class="hover-effect q-ml-sm" />
        </q-stepper-navigation>
      </q-step>

        <q-step
        :name="4"
        title="Coût"
        icon="point_of_sale"
        :done="step > 4"
      >
       <div class="row">
        <q-input
        ref="prixInput"
        class="my-0 col-1"
        v-model="prix"
        label="Prix"
        color ='cyan-4'
        @mouseover="changeLabelColor('nameInput','#ffb74d')"
        @mouseleave="changeLabelColor('nameInput','')"
        @focus="onFocus('name','#4dd0e1')"
        @blur="onBlur('name')"
      >
        <template v-slot:append>
          <div class="uniteStockName text-subtitle2 text-cyan-4">€</div>
        </template>
        <template v-slot:before>
          <q-icon name="euro" color="cyan-4"/>
        </template>
      </q-input>
       </div>
      <div class="row">
      <div class="col-8">
      <div class="row">
      <q-input
        ref="prixUnitInput"
        class="my-0 col-2"
        v-model="prix_unit"
        label="Prix"
        color ='cyan-4'
        @mouseover="changeLabelColor('nameInput','#ffb74d')"
        @mouseleave="changeLabelColor('nameInput','')"
        @focus="onFocus('name','#4dd0e1')"
        @blur="onBlur('name')"
      >
        <template v-slot:append>
          <div class="uniteStockName text-subtitle2 text-cyan-4">€/{{ uniteStockNom }}</div>
        </template>
        <template v-slot:before>
          <q-icon name="euro" color="cyan-4"/>
        </template>
      </q-input>
      </div>
      </div>
      </div>
      <q-stepper-navigation>
          <q-btn flat @click="step = 5" color="cyan-4" label="Suivant" class="hover-effect"/>
          <q-btn flat @click="step = 2" color="cyan-4" label="Précédent" class="hover-effect q-ml-sm" />
        </q-stepper-navigation>
      </q-step>
        <q-step
        :name="5"
        title="Stock"
        icon="inventory"
        :done="step > 5"
      >
      <div class="row">
          <q-input
            ref="stockMini"
            class="my-0 col-2"
            v-model="stock_mini"
            label="Stock mini"
            color ='cyan-4'
            @mouseover="changeLabelColor('nameInput','#ffb74d')"
            @mouseleave="changeLabelColor('nameInput','')"
            @focus="onFocus('name','#4dd0e1')"
            @blur="onBlur('name')"
          >
            <template v-slot:append>
              <div class="uniteStockName text-subtitle2 text-cyan-4">{{ uniteStockNom }}</div>
            </template>
            <template v-slot:before>
              <font-awesome-icon icon="fa-solid fa-flask" style="color: #4dd0e1;"/>
            </template>
          </q-input>
          </div>
          <div class="row">
          <q-toggle
            v-model="stock"
            color="green-4"
            icon="inventory"
            label="Stockée"
            size="md"
          />
          <q-toggle
             v-model="cdeAuto"
             color="purple-4"
             icon="shopping_cart"
             label="Déclenchement des commande"
             size="md"
          />
         </div>

        <q-stepper-navigation>
          <q-btn flat @click="step = 6" color="cyan-4" label="Suivant" class="hover-effect"/>
          <q-btn flat @click="step = 4" color="cyan-4" label="Précédent" class="hover-effect q-ml-sm" />
        </q-stepper-navigation>
      </q-step>

      <q-step
        :name="6"
        title="Réglementation"
        icon="settings"
        :done="step > 6"
      >
        <div class="row">
            <q-select
            v-model="liste"
            color="cyan-4"
            class="col-2 hover-effect"
            label="Liste"
            :options="allListeLabel"
            option-label="label"
            option-value="id"
          >
            <template v-slot:before>
              <q-icon name="gavel" color="cyan-4"/>
            </template>
          </q-select>
        </div>
        <q-stepper-navigation>
          <q-btn flat @click="step = 5" color="cyan-4" label="Précédent" class="hover-effect"/>
          <q-btn flat @click="step = 7" color="cyan-4" label="Terminer" class="hover-effect q-ml-sm" />
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
      cdtDialog: false,
      cdtMat: "",
      uniteMes: [],
      uniteStock: [],
      typeDialog: false,
      formeDialog: false,
      typeMat: "",
      formeMat: "",
      step: 1,
      name: '',
      type: null,
      forme: null,
      fournisseur: null,
      cdt: '',
      qté_cdt: '',
      prix_unit: '',
      prix: '',
      qté_stock: '',
      stock_mini: '',
      stock: false,
      cdeAuto: false,
      cde: false,
      liste: null,
      attente_livraison: false
    };
  },

  computed: {
    ...mapGetters('matieresPremieres', ['allTypes', 'allUnites', 'allFormes', 'allCdts']),
    ...mapGetters('formules', ['allListes']),
    ...mapGetters('suppliers', ['allSuppliers']),

    allCdtLabel() {
      return this.allCdts.map(cdt => ({
        ...cdt,
        label: `${cdt.nom}`,
        id: `${cdt.id}`,
      }));
    },

    allSuppliersLabel() {
      return this.allSuppliers.map(supplier => ({
        ...supplier,
        label: `${supplier.name}`,
        id: `${supplier.id}`,
      }));
    },

    allTypeLabel() {
      // Calculer le libellé complet avec le nom et le fournisseur
      return this.allTypes.map(type => ({
        ...type,
        label: `${type.nom}`,
        id: `${type.id}`,
      }));
    },

    allListeLabel() {
      return this.allListes.map(liste => ({
        ...liste,
        label: `${liste.nom}`,
        id: `${liste.id}`,
      }));
    },

    allUniteLabel() {
      // Calculer le libellé complet avec le nom et le fournisseur
      return this.allUnites.map(unite => ({
        ...unite,
        label: `${unite.nom}`,
        id: `${unite.id}`,
      }));
    },

    allFormeLabel() {
      // Calculer le libellé complet avec le nom et le fournisseur
      return this.allFormes.map(forme => ({
        ...forme,
        label: `${forme.nom}`,
        id: `${forme.id}`,
      }));
    },

    uniteStockNom() {
      if (this.forme && this.allUnites) {
        const uniteStock = this.allUnites.find(unite => unite.id === this.forme.unite_stock.id);
        return uniteStock ? uniteStock.nom : '';
      }
      return '';
    },
  },

  async mounted() {
   await this.loadUnites();
   await this.loadTypes();
   await this.loadListes();
   await this.loadFormes();
   await this.loadSuppliers();
   await this.loadCdt();
   console.log('allCdt', this.allCdts)
  },

  methods: {
    ...mapActions('matieresPremieres', ['loadTypes','loadFormes', 'loadUnites', 'addMatiere', 'addType', 'addForme', 'loadCdt', 'addCdt']),
    ...mapActions('formules', ['loadListes']),
    ...mapActions('suppliers', ['loadSuppliers']),

    updateForme(value) {
      this.forme = this.allFormeLabel.find(forme => forme.id === value);
    },

    async validerCdt(){
      const formData = {
        nom: this.cdtMat,
      };
      await this.addCdt(formData);
      await this.loadCdt();
      this.cdtDialog=false;
    },

    async validerType(){
      const formData = {
        nom: this.typeMat,
      };
      await this.addType(formData);
      await this.loadTypes();
      this.typeDialog=false;
    },

    async validerForme(){
      const formData = {
        nom: this.formeMat,
        unite_mesure: this.uniteMes.id,
        unite_stock: this.uniteStock.id
      };
      console.log("formData envoyé:", formData);
      await this.addForme(formData);
      await this.loadFormes();
      this.formeDialog=false;
    },

    async submitForm() {
      const formData = {
      nom: this.name,
      type: this.type.id,
      forme: this.forme.id,
      fournisseur: this.fournisseur.id,
      cdt: this.cdt.id,
      qté_cdt: this.qté_cdt,
      prix_unit: this.prix_unit,
      prix: this.prix,
      qté_stock: 0,
      stock_mini: this.stock_mini,
      stock: this.stock,
      cde_auto: this.cdeAuto,
      cde: false,
      liste: this.liste.id,
      attente_livraison: false

      };
      this.addMatiere(formData);
    },
  },
};
</script>






