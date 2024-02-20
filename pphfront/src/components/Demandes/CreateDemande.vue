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
      <div class="text-h5 text-center text-cyan-4">Demande</div>
        <q-step
          :name="1"
          title="Plannification"
          icon="calendar_month"
          :done="step > 1"
        >
          <div class="row">
            <q-input
                type="date"
                ref="dateInput"
                class="q-mr-lg col-2"
                v-model="date_prevu"
                label="Date prévue"
                color ='cyan-4'
                @mouseover="changeLabelColor('dateInput','#ffb74d')"
                @mouseleave="changeLabelColor('dateInput','')"
                @focus="onFocus('date_prevu','#4dd0e1')"
                @blur="onBlur('date_prevu')"
            >
              <template v-slot:before>
                <q-icon name="calendar_month" color="cyan-4"/>
              </template>
            </q-input>
            <q-toggle
                v-model="toggleRepeat"
                icon="calendar_month"
                color="purple-4"
                size="md"
                label="Répéter"
                class="col-2"
            />
          </div>
          <div class="row">
            <q-input
                v-if="toggleRepeat"
                ref="repeatInput"
                class="q-mr-lg col-2"
                v-model="repeat"
                label="Répétition"
                color ='cyan-4'
                @mouseover="changeLabelColor('dateInput','#ffb74d')"
                @mouseleave="changeLabelColor('dateInput','')"
                @focus="onFocus('date_prevu','#4dd0e1')"
                @blur="onBlur('date_prevu')"
            >
              <template v-slot:before>
                <q-icon name="update" color="cyan-4"/>
              </template>
              <template v-slot:append>
                <div class="text-cyan-4 text-subtitle2">Jours</div>
              </template>
            </q-input>
            <q-input
                v-if="toggleRepeat"
                ref="repeatInput"
                class="q-mr-lg col-2"
                v-model="delai"
                label="Délai"
                color ='cyan-4'
                @mouseover="changeLabelColor('dateInput','#ffb74d')"
                @mouseleave="changeLabelColor('dateInput','')"
                @focus="onFocus('date_prevu','#4dd0e1')"
                @blur="onBlur('date_prevu')"
            >
              <template v-slot:before>
                <q-icon name="alarm" color="cyan-4"/>
              </template>
              <template v-slot:append>
                <div class="text-cyan-4 text-subtitle2">Jours</div>
              </template>
            </q-input>
          </div>
          <q-stepper-navigation>
      <q-btn flat @click="step = 2" color="cyan-4" label="Suivant" class="hover-effect" />
    </q-stepper-navigation>
        </q-step>

        <q-step
          :name="2"
          title="Patient"
          icon="personal_injury"
          :done="step > 2"
        >
          <div class="row">
            <q-input
            ref="nomInput"
            class="q-mr-lg col-3"
            v-model="patient"
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
            class="q-mr-lg col-1"
            v-model="age"
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
          <template v-slot:append>
            <div class="text-cyan-4 text-subtitle2" color="cyan-4">ans</div>
          </template>
        </q-input>
          </div>
          <q-stepper-navigation>
            <q-btn flat @click="step = 3" color="cyan-4" label="Suivant" class="hover-effect" />
            <q-btn flat @click="step = 1" color="cyan-4" label="Précédent" class="hover-effect q-ml-sm" />
          </q-stepper-navigation>
        </q-step>

        <q-step
          :name="3"
          title="Demandeur"
          icon="person_book"
          :done="step > 3"
        >
          <div class="row">
            <q-select
              v-model="service"
              color="cyan-4"
              class="col-2 hover-effect"
              label="Service"
              :options="allServicesLabel"
              option-label="label"
              option-value="value"
            >
            <template v-slot:before>
              <q-icon name="groups" color="cyan-4"/>
            </template>
            </q-select>
          </div>
          <div class="row">
            <q-input
              v-model="prescripteur"
              color="cyan-4"
              class="col-3 hover-effect"
              label="Prescripteur"
            >
            <template v-slot:before>
              <q-icon name="badge" color="cyan-4"/>
            </template>
            </q-input>
          </div>

          <q-stepper-navigation>
            <q-btn flat @click="step = 4" color="cyan-4" label="Suivant" class="hover-effect"/>
            <q-btn flat @click="step = 2" color="cyan-4" label="Précédent" class="hover-effect q-ml-sm" />
          </q-stepper-navigation>
        </q-step>

        <q-step
          :name="4"
          title="Formule"
          icon="local_pharmacy"
          :done="step > 4"
        >
          <div class="row">
            <q-select
              v-model="typePrep"
              color="cyan-4"
              class="col-2 hover-effect"
              label="Type"
              :options="allTypePrepLabel"
              option-label="label"
              option-value="value"
              @input="onTypeChange"
            >
            <template v-slot:before>
              <q-icon name="local_pharmacy" color="cyan-4"/>
            </template>
            </q-select>
          </div>
          <div class="row">
            <q-select
              v-model="formule"
              color="cyan-4"
              class="col-3 hover-effect"
              label="Formule"
              :options="allFormulesLabel"
              option-label="label"
              option-value="value"
              @input="onFormuleChange"
            >
            <template v-slot:before>
              <q-icon name="local_pharmacy" color="cyan-4"/>
            </template>
            </q-select>
          </div>

          <q-stepper-navigation>
            <q-btn flat @click="step = 5" color="cyan-4" label="Suivant" class="hover-effect"/>
            <q-btn flat @click="step = 3" color="cyan-4" label="Précédent" class="hover-effect q-ml-sm" />
          </q-stepper-navigation>
        </q-step>

        <q-step
          :name="5"
          title="Paramètres"
          icon="settings"
          :done="step > 5"
        >
          <div v-if="parametres.length > 0" class="row">
          <div class="col-1">
              <div v-for="(parametre, index) in parametres" :key="index">
                <q-input :label="parametre.parametre.nom" color="cyan-4" v-model="parametre.valeur_parametre">
                  <template v-slot:append>
                    <div class="text-cyan-4 text-subtitle2">{{ parametre.parametre.unite }}</div>
                  </template>
                </q-input>
              </div>
          </div>
        </div>
          <div v-else class="text-center text-cyan-4">Aucun paramètre trouvé pour cette formule.</div>

          <q-stepper-navigation>
            <q-btn flat @click="step = 6" color="cyan-4" label="Suivant" class="hover-effect"/>
            <q-btn flat @click="step = 4" color="cyan-4" label="Précédent" class="hover-effect q-ml-sm" />
          </q-stepper-navigation>
        </q-step>

        <q-step
          :name="6"
          title="Composition"
          icon="science"
          :done="step > 6"
        >
        <div v-if="compositions.length > 0" class="row">
          <div class="col-2">
            <q-list>
              <q-item clickable v-close-popup v-for="(composition, index) in compositions" :key="index">
                <q-item-section class="hover-effect">{{ composition.matiere.nom }} {{ composition.qté }} {{ composition.matiere.unite_mesure.nom }}</q-item-section>
              </q-item>
            </q-list>
          </div>
        </div>
      <div v-else class="text-center text-cyan-4">Aucune composition trouvée pour cette formule.</div>

        <q-stepper-navigation>
          <q-btn flat @click="step = 7" color="cyan-4" label="Suivant" class="hover-effect"/>
          <q-btn flat @click="step = 5" color="cyan-4" label="Précédent" class="hover-effect q-ml-sm" />
        </q-stepper-navigation>
      </q-step>

        <q-step
          :name="7"
          title="Commentaire"
          icon="edit_note"
          :done="step > 7"
        >
          <div class="row">
            <q-input
            ref="comInput"
            class="q-mr-lg col-3"
            v-model="commentaire"
            label="Commentaire"
            color ='cyan-4'
            @mouseover="changeLabelColor('nameInput','#ffb74d')"
            @mouseleave="changeLabelColor('nameInput','')"
            @focus="onFocus('name','#4dd0e1')"
            @blur="onBlur('name')"
        >
          <template v-slot:before>
            <q-icon name="edit_note" color="cyan-4"/>
          </template>
        </q-input>
          </div>

          <q-stepper-navigation>
          <q-btn flat @click="step = 8" color="cyan-4" label="Terminer" class="hover-effect"/>
          <q-btn flat @click="step = 6" color="cyan-4" label="Précédent" class="hover-effect q-ml-sm" />
        </q-stepper-navigation>
        </q-step>

      <div class="row justify-center">
        <q-btn-group>
          <q-btn flat @click="validDemande" color="green-4" label="Enregistrer" class="btn-flat-success-pph"/>
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
      toggleRepeat: false,
      repeat: '',
      delai: '',
      patient: '',
      age: '',
      typePrep: null,
      formule: null,
      prescripteur: null,
      commentaire: null,
      service: '',
      date_prevu: '',
      allTypePrepLabel: [], // Options pour le champ de sélection du fournisseur
      allFormulesLabel: [],
      allServicesLabel: [],
      parametres: [],
      valeurParametre: null,
      compositions: [],
    };
  },

  computed: {
    ...mapGetters('formules', ['allTypes', 'allListes', 'allFormules', 'allParametresFormules',
                  'allParametres', 'allCompositions']),
    ...mapGetters('voiesAdministration', ['allVoies']),
    ...mapGetters('services', ['allServices']),
    ...mapGetters('demandes', ['allDemandes']),

  },


  created() {
    this.loadTypes();
    this.loadFormules();
    this.loadParametres();
    this.loadParametresFormules();
    this.loadCompositions();
    this.loadServices();
    this.loadDemandes();
    this.allTypePrepLabel = this.allTypes
      .map(type => ({
      label: type.nom,
      value: type.id,
    }));
    this.allServicesLabel = this.allServices
      .map(service => ({
      label: service.nom,
      value: service.id,
    }));
    console.log('allservices: ', this.allServices);
    console.log('Service: ', this.service.nom)
  },

  watch: {
      typePrep: 'onTypeChange',
      formule: 'onFormuleChange',
  },

  methods: {
    ...mapActions('formules', ['loadTypes', 'loadFormules', 'loadParametresFormules',
                              'loadParametres', 'loadCompositions']),
    ...mapActions('demandes', ['addDemande', 'addParametresValues', 'loadDemandes']),
    ...mapActions('services', ['addService', 'loadServices']),

    onFormuleChange() {
      if (this.formule) {
          // Filtrer les paramètres en fonction de l'ID de la formule sélectionnée
          this.parametres = this.allParametresFormules.filter(parametre =>
              parametre.num_formule === this.formule.value
          );
          this.compositions = this.allCompositions.filter(composition =>
              composition.num_formule === this.formule.value
          );
      } else {
          // Réinitialiser les paramètres si aucune formule n'est sélectionnée
          this.parametres = [];
          this.compositions = [];
      }
    },


    onTypeChange() {
      if (this.typePrep) {
        // Filtrer les catégories en fonction de l'ID du fournisseur sélectionné
        this.allFormulesLabel = this.allFormules
          .filter(formule => formule.type.id === this.typePrep.value && formule.is_activate === true)
          .map(formule => ({
            label: formule.nom,
            value: formule.id,
          }));
      } else {
        // Réinitialiser les catégories si aucun fournisseur n'est sélectionné
        this.allFormulesLabel = this.allFormules.map(formule => ({
          label: formule.nom,
          value: formule.id,
        }));
      }
    },

    async validDemande() {
      const allDemandes = this.allDemandes;

        // Vérifiez si allDemandes est vide
        if (allDemandes.length === 0) {
          console.error('Aucune demande n\'a été trouvée.');
          return;
        }
        // Trouvez le dernier ID de demande
        const lastDemandeId = Math.max(...allDemandes.map(demande => demande.id));
        // Créez un tableau pour stocker les données formatées
        const formData = [];
        // Parcourez chaque paramètre et préparez les données formatées
        this.parametres.forEach(parametre => {
          const formattedParametre = {
            num_demande: lastDemandeId + 1, // Incrémentation du dernier ID de demande
            parametre: parametre.parametre.id,
            valeur_parametre: parametre.valeur_parametre
          };
          formData.push(formattedParametre);
        });
        console.log(formData);
        const jsonData = JSON.stringify(formData);
        console.log(jsonData)
      this.addParametresValues(jsonData);

      const demandeData = {
        date_prevu : this.date_prevu,
        recurence: this.repeat,
        delai: this.delai,
        prep: this.formule.value,
        typePrep: this.typePrep.value,
        service: this.service.value,
        patient: this.patient,
        age: this.age,
        prescripteur: this.prescripteur,
        commentaire: this.commentaire,
      };
      this.addDemande(demandeData);
      this.date_prevu = '';
      this.toggleRepeat= false;
      this.repeat = '';
      this.delai = '';
      this.formule = null;
      this.typePrep = null;
      this.service = '';
      this.patient = '';
      this.age = '';
      this.prescripteur = '';
      this.commentaire = '';
      this.step = 1;
    },
  },
};
</script>






