<template>
  <q-page>
    <div class="row justify-center">
      <div class="col-md-12">
        <div class="row q-mx-sm">
          <div class="col-4 offset-4 q-mt-md text-cyan-4 text-h6">
            <div class="row justify-center">
            {{ controlCount }} demandes en attente
            </div>
          </div>
          <div class="col-2 offset-2">
            <q-input
                ref="searchInput"
                v-model="searchQuery"
                label="Recherche..."
                @input="filteredDemandes"
                color="cyan-4"
                @mouseover="changeLabelColor('searchInput', '#ffb74d')"
                @mouseleave="changeLabelColor('searchInput', '')"
                @focus="onFocus('searchQuery', '#4dd0e1')"
                @blur="onBlur('searchQuery')"
            >
              <template v-slot:append>
                <q-icon name="search" color="cyan-4"/>
              </template>
            </q-input>
          </div>
        </div>
        <div class="row q-mt-sm">
          <div class="col col-12 justify-center">
            <div class="row justify-start">
              <div class="col-2 q-pa-sm" v-for="demande in filteredDemandes" :key="demande.id">
                <q-card bordered class="card-maxi justify-center items-center text-center relative">
                  <div class="card-content">
                    <q-img
                        class="logo-card-mini"
                        src="../../assets/img/blanc.jpg"
                        :alt="demande.prep.nom"
                        loading="lazy"
                        spinner-color="red-4"
                    >
                      <div class="absolute-top hover-effect q-my-none text-cyan-1">
                        <div>{{ demande.prep.nom }}</div>
                        <div>{{ demande.prep.type.nom }}</div>
                        <div>Pour le {{ demande.date_prevu }}</div>
                      </div>
                      <template v-slot:loading>
                        <q-spinner-rings color="red-4" />
                      </template>
                    </q-img>
                    <q-btn flat color="white" class="absolute-top-right hover-effect q-pa-none q-ma-none" icon="more_vert" @click.stop="toggleMenu(demande.id)" />
                    <q-menu fit anchor="top right" self="bottom middle" v-model="showMenu[demande.id]">
                      <q-list style="min-width: 100px">
                        <q-item clickable v-close-popup @click.stop="toggleProduction({ demandeId: demande.id })">
                          <q-item-section class="hover-effect-success">
                            Générer fiche de fabrication
                          </q-item-section>
                        </q-item>
                        <q-item v-if="demande.recurence" clickable v-close-popup @click.stop="stopRepeat({ demandeId: demande.id })">
                          <q-item-section class="hover-effect-warning">Stopper répétition</q-item-section>
                        </q-item>
                        <q-item v-if="!demande.recurence" clickable v-close-popup @click.stop="toggleRepeat(demande.id)">
                          <q-item-section class="hover-effect-info">Ajouter répétition</q-item-section>
                        </q-item>
                        <q-item clickable v-close-popup @click.stop="deleteDemande(demande.id)">
                          <q-item-section class="hover-effect-warning">Supprimer</q-item-section>
                        </q-item>
                      </q-list>
                    </q-menu>
                    <q-form>
                      <q-dialog v-model="repeatDialog[demande.id]">
                        <q-card>
                          <q-card-section>
                            <div class="row justify-center text-h6 text-cyan-4">
                              Répétition pour la demande n°{{ demande.id }}
                            </div>
                            <div class="row justify-center text-subtitle1 text-orange-4">
                              {{ demande.prep.nom }}
                            </div>
                          </q-card-section>
                          <q-separator/>
                          <q-card-section>
                            <div class="row">
                              <div class="col-4">
                                <q-input v-model="repeat" label="Répétition" color="cyan-4">
                                  <template v-slot:append>
                                    <div class="text-subtitle2 text-cyan-4 q-mb-none q-pa-none">jours</div>
                                  </template>
                                </q-input>
                              </div>
                            </div>
                          </q-card-section>
                          <q-separator/>
                          <q-card-section>
                            <div class="row justify-center">
                              <q-btn-group>
                                <q-btn flat label="Valider"
                                       @click.stop="addRepeat({ demandeId: demande.id, repeatTime: this.repeat }); toggleRepeat(demande.id)"
                                       color="green-4"/>
                                <q-btn flat label="Annuler"
                                       @click.stop="toggleRepeat(demande.id)"
                                       color="red-4"/>
                              </q-btn-group>
                            </div>
                          </q-card-section>
                        </q-card>
                      </q-dialog>
                    </q-form>
                    <div v-if="demande.recurence" class="absolute-top-left row q-ml-xs q-mt-xs">
                      <q-icon name="update" color="cyan-4" size="xs" />
                      <div class="text-cyan-4">{{ demande.recurence }}j</div>
                    </div>
                  </div>
                  <div class="absolute-bottom-left">
                    <div class="row q-mb-xs">
                      <font-awesome-icon v-if="demande.prep.pediatric" icon="fa-solid fa-child" class="q-ml-xs fa-lg" style="color: #4dd0e1;"/>
                      <font-awesome-icon v-if="demande.prep.froid" fade icon="fa-solid fa-snowflake" class="q-ml-xs fa-lg" style="color: #4dd0e1;" />
                      <q-icon v-if="demande.prep.agiter" name="waving_hand" class="q-ml-xs" color="cyan-4" size="xs"/>
                      <q-icon v-if="demande.prep.lumiere" name="light_mode" class="q-ml-xs" color="red-4" size="xs"/>
                    </div>
                  </div>
                  <q-btn-group class="absolute-bottom-right q-pa-none q-ma-none">
                    <q-btn
                       class="q-pa-none hover-effect"
                       flat
                       :color="compo[demande.id] ? 'orange-4' : 'cyan-4'"
                       icon="science"
                       size="sm"
                       @click.stop="toggleCompo(demande.id)"
                    />
                    <q-btn
                      class="hover-effect"
                      :color="settings[demande.id] ? 'orange-4' : 'cyan-4'"
                      round
                      flat
                      dense
                      icon="settings"
                      size="sm"
                      @click.stop="toggleSettings(demande.id)"
                    />
                    <q-btn
                      class="hover-effect"
                      :color="expanded[demande.id] ? 'orange-4' : 'cyan-4'"
                      round
                      flat
                      dense
                      icon="info"
                      size="sm"
                      @click.stop="toggleInfo(demande.id)"
                    />
                  </q-btn-group>
                  <q-menu class="row" fit anchor="bottom right" self="top middle" v-model="compo[demande.id]">
                    <q-list class="col-12">
                      <q-item>
                        <q-item-section class="text-cyan-4 text-center">
                          Composition de la formule
                        </q-item-section>
                      </q-item>
                      <q-item class="row" v-for="compo in filteredCompositions(demande.prep.id)" :key="compo.id">
                        <q-item-section class="col-auto text-orange-4 text-no-wrap">
                          {{ compo.matiere.nom }} :
                        </q-item-section>
                        <q-item-section class="col-auto text-grey-7">
                          <q-item-label>{{ getCalculatedQty(compo.calcul,filteredParametres(demande.id), compo.qté, compo.matiere.unite_mesure.nom) }} {{ compo.matiere.unite_mesure.nom }}</q-item-label>
                        </q-item-section>
                        <q-item-section v-if="compo.matiere.cmr" class="col-auto q-ml-none text-grey-7">
                          <q-img class="fade-blink" src="@/assets/img/health_hazard.png"
                                 :style="{ width: '20px', height: '20px' }"/>
                        </q-item-section>
                      </q-item>
                    </q-list>
                  </q-menu>
                  <q-menu fit anchor="bottom right" self="top middle" v-model="settings[demande.id]">
                    <q-list style="min-width: 100px">
                      <q-item>
                        <q-item-section class="text-cyan-4 text-center">
                          Paramètres de la formule
                        </q-item-section>
                      </q-item>
                      <q-item class="row" v-for="parametre in filteredParametres(demande.id)" :key="parametre.id">
                        <q-item-section class="col-auto text-orange-4 text-no-wrap">
                          {{ parametre.parametre.nom }} :
                        </q-item-section>
                        <q-item-section class="col-auto text-grey-7">
                          {{ parametre.valeur_parametre }}{{ parametre.parametre.unite }}
                        </q-item-section>
                      </q-item>
                    </q-list>
                  </q-menu>
                  <q-menu fit anchor="bottom right" self="top middle" v-model="expanded[demande.id]">
                    <q-list style="min-width: 100px">
                      <q-item>
                        <q-item-section class="text-cyan-4 text-center">
                          Détails de la demande n° {{ demande.id }}
                        </q-item-section>
                      </q-item>
                      <q-item v-if="demande.date_demande">
                        <q-item-section avatar class="text-orange-4">
                          Date d'émission :
                        </q-item-section>
                        <q-item-section class="text-grey-7">
                          {{ demande.date_demande }}
                        </q-item-section>
                      </q-item>
                      <q-item v-if="demande.patient">
                        <q-item-section avatar class="text-orange-4">
                          Patient :
                        </q-item-section>
                        <q-item-section class="text-grey-7">
                          {{ demande.patient }} - {{ demande.age }} ans
                        </q-item-section>
                      </q-item>
                      <q-item v-if="demande.service.nom">
                        <q-item-section avatar class="text-orange-4">
                          Service :
                        </q-item-section>
                        <q-item-section class="text-grey-7">
                          {{ demande.service.nom }}
                        </q-item-section>
                      </q-item>
                      <q-item v-if="demande.prescripteur">
                        <q-item-section avatar class="text-orange-4">
                          Prescripteur :
                        </q-item-section>
                        <q-item-section class="text-grey-7">
                          {{ demande.prescripteur }}
                        </q-item-section>
                      </q-item>
                      <q-item v-if="demande.commentaire">
                        <q-item-section avatar class="text-orange-4">
                          Commentaire :
                        </q-item-section>
                        <q-item-section class=" row items-center text-grey-7 hover-effect">
                            {{ demande.commentaire }}
                          </q-item-section>
                      </q-item>
                    </q-list>
                  </q-menu>
                </q-card>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </q-page>
</template>

<script>
import { mapActions, mapGetters } from 'vuex';

export default {
  name: "demandesCards",

  data() {
    return {
      searchQuery: '',
      repeat: '',
    };
  },

  computed: {
    ...mapGetters('demandes', ['allDemandes', 'allParametresDemandes', 'settings',
                               'showMenu', 'expanded', 'compo', 'repeatDialog']),
    ...mapGetters('dateFormatter', ['getFormattedDate']),
    ...mapGetters('formules', ['allCompositions']),

    controlCount() {
      return this.filteredDemandesAttente.length;
    },


    filteredDemandesAttente() {
      return this.allDemandes.filter(demande => demande.production === false);
    },

    filteredDemandes() {
      if (this.searchQuery) {
        return this.filteredDemandesAttente.filter(demande =>
            demande.prep.nom.toLowerCase().startsWith(this.searchQuery.toLowerCase()) ||
            demande.service.nom.toLowerCase().startsWith(this.searchQuery.toLowerCase())
        );
      }
      return this.filteredDemandesAttente;
    },
  },

  created() {
    this.loadDemandes();
    this.loadParametresDemandes();
    this.loadCompositions();
  },

  methods: {
    ...mapActions('demandes', ['loadDemandes', 'loadParametresDemandes', 'deleteDemande', 'toggleInfo',
                               'toggleMenu', 'toggleProduction', 'toggleSettings', 'toggleCompo',
                               'stopRepeat', 'toggleRepeat', 'addRepeat']),
    ...mapActions('dateFormatter', ['formatDate']),
    ...mapActions('formules', ['loadCompositions', 'loadFormules']),

    getCalculatedQty(formula, params, qte, unitMeasureString) {
      for(let param of params){
        let searchTerm = param.parametre.nom + " - " + param.parametre.unite;
        formula = formula.replace(new RegExp(searchTerm, 'g'), param.valeur_parametre);

        let qteSearchTerm = "Quantité - " + unitMeasureString;
        formula = formula.replace(new RegExp(qteSearchTerm, 'g'), qte);
      }

      try {
        let result = eval(formula);
        // Si le résultat est un nombre, le formater avec 3 chiffres après la virgule
        if(!isNaN(result)) {
          return Number(result).toFixed(2);
        } else {
          return result;
        }
      } catch(e) {
        return "Erreur";
      }
    },

    filteredParametres(demandeId) {
      return this.allParametresDemandes.filter(parametre => parametre.num_demande === demandeId);
    },

    filteredCompositions(demandeFormule) {
      return this.allCompositions.filter(compo => compo.num_formule === demandeFormule);
    },

    changeLabelColor(inputRef, color) {
      if (!this[inputRef.replace('Input', '')]) {
        this.$refs[inputRef].$el.querySelector('.q-field__label').style.color = color;
      }
    },

    onFocus(field, color) {
      this[`${field}Focused`] = true;
      this.changeLabelColor(`${field}Input`, color);
    },

    onBlur(field) {
      this[`${field}Focused`] = false;
    },

    redirectToLink(id) {
      this.$router.push(`/supplier/${id}`);
    }
  }
};
</script>



