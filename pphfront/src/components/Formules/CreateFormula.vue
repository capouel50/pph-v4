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
      <div v-if="formuleId" class="text-h5 text-center text-cyan-4">{{ formule.nom }}</div>
      <div v-else class="text-h5 text-center text-cyan-4">Nouvelle Formule</div>
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
            option-value="id"
          >
            <template v-slot:before>
              <q-icon name="local_pharmacy" color="cyan-4"/>
            </template>
          </q-select>
        </div>
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
            <q-toggle
                class="col-2 offset-1 q-ml-lg q-mt-sm"
                v-model="pediatric"
                label="Formule pédiatrique"
                size="md"
                color="red-4"
                icon="account_child"
            />
        </div>
        <q-stepper-navigation>
          <q-btn flat @click="step = 2" color="cyan-4" label="Suivant" class="hover-effect" />
        </q-stepper-navigation>
      </q-step>

      <q-step
        :name="2"
        title="Voie d'administration"
        icon="vaccines"
        :done="step > 2"
      >
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

      <q-stepper-navigation>
          <q-btn flat @click="step = 1" color="cyan-4" label="Précédent" class="hover-effect q-ml-sm" />
        <q-btn flat @click="step = 3" color="cyan-4" label="Suivant" class="hover-effect"/>
        </q-stepper-navigation>
      </q-step>

      <q-step
        :name="3"
        title="Conservation"
        icon="ac_unit"
        :done="step > 3"
      >

      <div class="row">
      <q-input
        ref="dureeInput"
        class="my-0 col-1"
        v-model="duree"
        label="Durée (j)"
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
            v-model="froid"
            color="cyan-4"
            icon="ac_unit"
            label="4°C - 8°C"
            size="md"
          />
          <q-toggle
             v-model="lumiere"
             color="yellow-4"
             icon="light_mode"
             label="Abris de la lumiere"
             size="md"
          />
          <q-toggle
             v-model="agiter"
             color="red-4"
             icon="waving_hand"
             label="Agiter avant emploi"
             size="md"
          />
         </div>
      </div>

        <q-stepper-navigation>
          <q-btn flat @click="step = 2" color="cyan-4" label="Précédent" class="hover-effect q-ml-sm" />
          <q-btn flat @click="step = 4" color="cyan-4" label="Suivant" class="hover-effect"/>
        </q-stepper-navigation>
      </q-step>

      <q-step
        :name="4"
        title="Matériel"
        icon="biotech"
        :done="step > 4"
      >
        <div class="row">
          <div class="col-8">
            <ArticlesForm v-if="step === 4" :newId="newId" :formuleId="formuleId"/>
          </div>
        </div>

        <q-stepper-navigation>
          <q-btn flat @click="step = 3" color="cyan-4" label="Précédent" class="hover-effect q-ml-sm" />
          <q-btn flat @click="step = 5" color="cyan-4" label="Suivant" class="hover-effect"/>
        </q-stepper-navigation>
      </q-step>

      <q-step
        :name="5"
        title="Paramètres"
        icon="settings"
        :done="step > 5"
      >
        <div class="row">
          <div class="col-8">
            <ParametresForm v-if="step === 5" :newId="newId" :formuleId="formuleId"/>
          </div>
        </div>

        <q-stepper-navigation>
          <q-btn flat @click="step = 4" color="cyan-4" label="Précédent" class="hover-effect q-ml-sm" />
          <q-btn flat @click="step = 6" color="cyan-4" label="Suivant" class="hover-effect"/>
        </q-stepper-navigation>
      </q-step>

      <q-step
        :name="6"
        title="Composition"
        icon="science"
        :done="step > 6"
      >
        <div class="row">
          <div class="col-12">
            <CompositionForm/>
          </div>
        </div>

        <q-stepper-navigation>
          <q-btn flat @click="step = 5" color="cyan-4" label="Précédent" class="hover-effect q-ml-sm" />
          <q-btn flat @click="step = 7" color="cyan-4" label="Suivant" class="hover-effect"/>
        </q-stepper-navigation>
      </q-step>

      <q-step
        :name="7"
        title="EPI"
        icon="masks"
        :done="step > 7"
      >
        <div class="row">
          <div class="col-8">
            <EpiForm v-if="step === 7" />
          </div>
        </div>

        <q-stepper-navigation>
          <q-btn flat @click="step = 6" color="cyan-4" label="Précédent" class="hover-effect q-ml-sm" />
          <q-btn flat @click="step = 8" color="cyan-4" label="Suivant" class="hover-effect"/>
        </q-stepper-navigation>
      </q-step>

      <q-step
        :name="8"
        title="Mode opératoire"
        icon="list_alt"
        :done="step > 8"
      >

        <div class="row">
        <q-input
        ref="modeOpInput"
        class="my-0 col-3"
        v-model="modeOperatoire"
        label="Mode opératoire"
        color ='cyan-4'
        autogrow
        @mouseover="changeLabelColor('nameInput','#ffb74d')"
        @mouseleave="changeLabelColor('nameInput','')"
        @focus="onFocus('name','#4dd0e1')"
        @blur="onBlur('name')"
      >
        <template v-slot:before>
          <q-icon name="menu_book" color="cyan-4"/>
        </template>
      </q-input>
      </div>

        <q-stepper-navigation>
          <q-btn flat @click="step = 7" color="cyan-4" label="Précédent" class="hover-effect q-ml-sm" />
          <q-btn flat @click="step = 9" color="cyan-4" label="Suivant" class="hover-effect"/>
        </q-stepper-navigation>
      </q-step>

      <q-step
        :name="9"
        title="Contre-indications et précautions d'emploi"
        icon="warning"
        :done="step > 9"
      >
      <div class="row">
      <q-input
        ref="emploiInput"
        class="my-0 col-3"
        v-model="emploi"
        label="Entrez les informations"
        color ='cyan-4'
        autogrow
        @mouseover="changeLabelColor('nameInput','#ffb74d')"
        @mouseleave="changeLabelColor('nameInput','')"
        @focus="onFocus('name','#4dd0e1')"
        @blur="onBlur('name')"
      >
        <template v-slot:before>
          <q-icon name="info" color="cyan-4"/>
        </template>
      </q-input>
      </div>

        <q-stepper-navigation>
          <q-btn flat @click="step = 8"  color="cyan-4" label="Précédent" class="hover-effect q-ml-sm" />
          <q-btn flat @click="step = 10" color="cyan-4" label="Suivant" class="hover-effect"/>
        </q-stepper-navigation>
      </q-step>

      <q-step
        :name="10"
        title="Publications"
        icon="article"
        :done="step > 10"
      >
      <div class="row">
        <q-input
        ref="publicationsInput"
        class="my-0 col-3"
        v-model="publications"
        label="Publications, données de stabilité..."
        color ='cyan-4'
        autogrow
        @mouseover="changeLabelColor('nameInput','#ffb74d')"
        @mouseleave="changeLabelColor('nameInput','')"
        @focus="onFocus('name','#4dd0e1')"
        @blur="onBlur('name')"
      >
        <template v-slot:before>
          <q-icon name="article" color="cyan-4"/>
        </template>
      </q-input>
      </div>
        <q-stepper-navigation>
          <q-btn flat @click="step = 9" color="cyan-4" label="Précédent" class="hover-effect q-ml-sm" />
          <q-btn flat @click="step = 11" color="cyan-4" label="Suivant" class="hover-effect q-ml-sm" />
        </q-stepper-navigation>
      </q-step>

      <q-step
          :name="11"
          title="PPH cloud"
          icon="cloud"
          :done="step > 11"
        >
        <div class="row">
          <div class="col-2">
            <q-toggle
                v-model="cloud"
                :label="cloud ? 'Publique' : 'Privée'"
                size="md"
                color="green-4"
                icon="publish"
            />
          </div>
        </div>

        <q-stepper-navigation>
          <q-btn flat @click="step = 10" color="cyan-4" label="Précédent" class="hover-effect q-ml-sm" />
          <q-btn flat @click="step = 12" color="cyan-4" label="Terminer" class="hover-effect"/>
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
import CompositionForm from './CompositionForm.vue';
import ParametresForm from './ParametresForm.vue';
import EpiForm from './EpiForm.vue';
import ArticlesForm from './ArticlesForm.vue';
import {mapActions, mapGetters, mapMutations } from "vuex";
import api from "../../../api";

export default {
  components: {
    CompositionForm,
    ParametresForm,
    EpiForm,
    ArticlesForm
  },
  data() {
    return {
      step: 1,
      name: '',                // Pour le Nom de la formule
      typePrep: null,          // Pour le Type de préparation
      liste: null,             // Pour la Liste
      voie: null,              // Pour la Voie d'administration
      duree: '',               // Pour la Durée
      froid: false,            // Toggle pour Conservation au froid
      lumiere: false,          // Toggle pour Abris de la lumiere
      agiter: false,           // Toggle pour Agiter avant emploi
      modeOperatoire: '',      // Pour le Mode opératoire
      emploi: '',              // Pour les Contre-indications et précautions d'emploi
      publications: '',
      cloud: false,
      pediatric: false,
      specialite: false,
      newId: null,
      formuleId: null,
      formule:[],
    };
  },

  computed: {
    ...mapGetters('formules', ['allFormules', 'allTypes', 'allListes', 'allArticlesFormules', "allParametresFormules"]),
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

  async created() {
    if(this.$route.params.id) {
      this.formuleId = Number(this.$route.params.id);
    }else{
      this.loadLastId();
    }

    await Promise.all([
      this.loadVoies(),
      this.loadTypes(),
      this.loadListes(),
      this.loadArticlesFormules(),
      this.loadParametresFormules(),
    ]);

    if(this.formuleId) {
      this.formule = this.allFormules.find(formule => formule.id === this.formuleId);
      this.name = this.formule.nom;
      this.typePrep = this.formule.type.nom;
      this.liste = this.formule.liste.nom;
      this.voie = this.formule.voie.nom;
      this.duree = this.formule.duree;
      this.froid = this.formule.froid;
      this.lumiere = this.formule.lumiere;
      this.agiter = this.formule.agiter;
      this.modeOperatoire = this.formule.mode_operatoire;
      this.emploi = this.formule.contre_indications;
      this.publications = this.formule.publications,
      this.cloud = this.formule.cloud;
      this.pediatric = this.formule.pediatric;
      this.specialite = this.formule.specialite;
    }
  },

  methods: {
    ...mapActions('formules', ['loadTypes','loadListes', 'addFormule', 'loadArticlesFormules',
                               'addArticles', 'loadParametresFormules', 'addParametres', 'updateParametres', 'updateArticles', 'updateFormule']),
    ...mapActions('voiesAdministration', ['loadVoies']),
    ...mapMutations('formules', ['RESET_ARTICLES_FORMULES', 'RESET_PARAMETRES_FORMULES']),

    async loadLastId() {
      try {
        // Utilisez une API Django ou Axios pour récupérer le dernier ID + 1
        const response = await api.get('/PPH/nouvelle-formule/dernier_id');
        const dernierId = response.data.dernierId;

        // Incrémentez l'ID de 1 pour obtenir la nouvelle valeur de num_formule
        this.newId = dernierId + 1;
        console.log('lastId', this.newId);
      } catch (error) {
        console.error('Erreur lors de la récupération du dernier ID de la formule', error);
      }
    },

    async submitForm() {
      const stateData = this.allArticlesFormules
          .filter(article => this.formuleId ?
              article.num_formule === this.formuleId : article.num_formule === this.newId)
          .map(article => ({
          num_formule: article.num_formule,
          article: article.articleId,
      }));
      const paramData = this.allParametresFormules
          .filter(parametre => this.formuleId ?
              parametre.num_formule === this.formuleId : parametre.num_formule === this.newId)
          .map(parametre => ({
          num_formule: parametre.num_formule,
          parametre: parametre.parametreId,
          unite: parametre.unite,
      }));
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
        cloud: this.cloud,
        pediatric: this.pediatric,
        specialite: this.specialite,
      };
      if(!this.formuleId){
        await this.addArticles(stateData);
        await this.addParametres(paramData);
        await this.addFormule(formData);
      }else{
        await this.updateArticles(stateData);
        await this.updateParametres(paramData);
        await this.updateFormule(formData);
      }
      this.RESET_ARTICLES_FORMULES(this.newId);
      this.RESET_PARAMETRES_FORMULES(this.newId);
      this.name= '';
      this.typePrep= null;
      this.liste= null;
      this.voie= null;
      this.duree= '';
      this.froid= false;
      this.lumiere= false;
      this.agiter= false;
      this.modeOperatoire= '';
      this.emploi= '';
      this.publications= '';
      this.cloud= false;
      this.pediatric= false;
      this.specialite= false;
      this.step= 1;

    },
  },
};
</script>






