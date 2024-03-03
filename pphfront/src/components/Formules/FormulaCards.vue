<template>
  <q-page>
    <div class="row justify-center">
      <div class="col-md-12">
        <div class="row q-mx-sm q-mt-sm">
          <div class="col-3 q-mt-sm">
            <q-fab glossy class="glossy btn-cyan-pph" icon="add_box" direction="right">
              <router-link to="/nouvelle-formule/">
                <q-fab-action flat external-label label-position="bottom" label="Créer" color="cyan-4" icon="add"/>
              </router-link>
              <router-link to="/cloud">
                <q-fab-action flat external-label label-position="bottom" label="Cloud" color="cyan-4" icon="cloud"/>
              </router-link>
            </q-fab>
          </div>
          <div class="col-6 q-mt-md text-cyan-4 text-h6">
            <div class="row justify-center">
            {{ countFormules }} formules référencées
            </div>
          </div>
          <div class="col-2 offset-1">
            <q-input
                ref="searchInput"
                v-model="searchQuery"
                label="Recherche..."
                @input="filterFormules"
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
              <div class="col-2 q-pa-sm" v-for="formule in filteredFormules" :key="formule.id"
                   @click="redirectToLink(formule.id)"
              >
                <q-card bordered class="card-maxi justify-center items-center text-center relative" :class="{ 'bd-red-4': !formule.is_activate}">
                  <div @click="redirectToLink(formule.id)" class="card-content">
                    <q-img class="logo-card-mini"
                           src="../../assets/img/blanc.jpg"
                           :alt="formule.nom"
                           loading="lazy"
                           spinner-color="red-4"
                    >
                      <q-icon
                          v-if="formule.is_valid"
                          name="done_all"
                          color="green-4"
                          class="icon-background"
                      />
                      <q-icon
                          v-if="!formule.is_valid"
                          name="remove_done"
                          color="red-4"
                          class="icon-background"
                      />
                      <div class="absolute-top hover-effect q-my-none" :class="{ 'text-cyan-1': formule.is_activate, 'text-red-4': !formule.is_activate }">
                        <div>{{ formule.nom }}</div>
                        <div>{{ formule.type.nom }}</div>
                      </div>
                      <template v-slot:loading>
                        <q-spinner-rings color="red-4" />
                      </template>
                    </q-img>
                    <q-btn flat color="white" class="absolute-top-right hover-effect q-pa-none q-ma-none" icon="more_vert" @click.stop="toggleMenu(formule.id)" />
                    <q-menu fit anchor="top right" self="bottom middle" v-model="showMenu[formule.id]">
                      <q-list style="min-width: 100px">
                        <q-item clickable v-close-popup @click.stop="toggleCloud({ formuleId: formule.id, isCloud: formule.cloud })">
                          <q-item-section class="hover-effect">
                            {{ formule.cloud ? 'Retirer du cloud' : 'Ajouter au cloud' }}
                          </q-item-section>
                        </q-item>
                        <q-item clickable v-close-popup v-if="formule.is_valid" @click.stop="toggleActivation({ formuleId: formule.id, isActive: formule.is_activate })">
                          <q-item-section :class="{ 'hover-effect-success': !formule.is_activate, 'hover-effect-warning': formule.is_activate }">
                            {{ formule.is_activate ? 'Désactiver' : 'Activer' }}
                          </q-item-section>
                        </q-item>
                        <q-item v-if="!formule.is_valid" clickable v-close-popup @click.stop="validFormule({ formuleId: formule.id, isValid: formule.is_valid })">
                          <q-item-section class="green-4 hover-effect-success">
                            Valider la formule
                          </q-item-section>
                        </q-item>
                      </q-list>
                    </q-menu>
                    <div class="absolute-top-left row q-ml-xs q-mt-xs">
                      <q-icon v-if="formule.cloud" name="cloud" color="cyan-4" size="xs" />
                    </div>
                  </div>
                  <div class="absolute-bottom-left">
                    <div class="row q-mb-xs">
                      <font-awesome-icon v-if="formule.pediatric" icon="fa-solid fa-child" class="q-ml-xs fa-lg" style="color: #4dd0e1;"/>
                      <font-awesome-icon v-if="formule.froid" fade icon="fa-solid fa-snowflake" class="q-ml-xs fa-lg" style="color: #4dd0e1;" />
                      <q-icon v-if="formule.agiter" name="waving_hand" class="q-ml-xs" color="cyan-4" size="xs"/>
                      <q-icon v-if="formule.lumiere" name="light_mode" class="q-ml-xs" color="red-4" size="xs"/>
                    </div>
                  </div>
                  <q-btn-group class="absolute-bottom-right q-pa-none q-ma-none">
                    <q-btn
                       class="q-pa-none hover-effect"
                       flat
                       color="cyan-4"
                       icon="bar_chart"
                       size="sm"
                    />
                    <q-btn
                       class="q-pa-none hover-effect"
                       flat
                       :color="compo[formule.id] ? 'orange-4' : 'cyan-4'"
                       icon="science"
                       size="sm"
                       @click.stop="toggleCompo(formule.id)"
                    />
                    <q-btn
                       class="q-pa-none hover-effect"
                       flat
                       :color="settings[formule.id] ? 'orange-4' : 'cyan-4'"
                       icon="settings"
                       size="sm"
                       @click.stop="toggleSettings(formule.id)"
                    />
                    <q-btn
                      class="hover-effect"
                      :color="expanded[formule.id] ? 'orange-4' : 'cyan-4'"
                      round
                      flat
                      dense
                      icon="info"
                      size="sm"
                      @click.stop="toggleInfo(formule.id)"
                    />
                  </q-btn-group>
                  <q-menu class="row" fit anchor="bottom right" self="top middle" v-model="compo[formule.id]">
                    <q-list class="col-12">
                      <q-item>
                        <q-item-section class="text-cyan-4 text-center">
                          Composition  et calcul de la formule
                        </q-item-section>
                      </q-item>
                      <q-item class="row" v-for="compo in filteredCompositions(formule.id)" :key="compo.id">
                        <q-item-section class="col-auto">
                          <q-item-label class="row">
                            <div class="text-orange-4">{{ compo.matiere.nom }} :&nbsp;</div>
                            <div class="text-grey-7">{{ compo.qté }} {{ compo.matiere.unite_mesure.nom }}</div>
                            </q-item-label>
                          <q-item-label class="row text-no-wrap" caption>
                            <div class="text-bold">Calcul :&nbsp;</div>
                            <div class="text-italic">{{ compo.calcul }}</div>
                          </q-item-label>
                        </q-item-section>
                        <q-item-section top v-if="compo.matiere.cmr" class="col-auto q-ml-none text-grey-7">
                          <q-img class="fade-blink" src="@/assets/img/health_hazard.png"
                                 :style="{ width: '20px', height: '20px' }"/>
                        </q-item-section>
                      </q-item>
                    </q-list>
                  </q-menu>
                  <q-menu fit anchor="bottom right" self="top middle" v-model="settings[formule.id]">
                    <q-list style="min-width: 100px">
                      <q-item>
                        <q-item-section class="text-cyan-4 text-center">
                          Paramètres de la formule
                        </q-item-section>
                      </q-item>
                      <q-item class="row" v-for="parametre in filteredParametres(formule.id)" :key="parametre.id">
                        <q-item-section class="col-auto text-no-wrap">
                          {{ parametre.parametre.nom }} - {{ parametre.parametre.unite }}
                        </q-item-section>
                      </q-item>
                    </q-list>
                  </q-menu>
                  <q-menu fit anchor="bottom right" self="top middle" v-model="expanded[formule.id]">
                    <q-list style="min-width: 100px">
                      <q-item v-if="formule.voie">
                        <q-item-section avatar class="text-cyan-4">
                          Voie :
                        </q-item-section>
                        <q-item-section class="text-grey-7">
                          {{ formule.voie.nom }}
                        </q-item-section>
                      </q-item>
                      <q-item v-if="formule.liste">
                        <q-item-section avatar class="text-cyan-4">
                          Liste :
                        </q-item-section>
                        <q-item-section class="text-grey-7">
                          {{ formule.liste.nom }} €
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
  name: "formulaCards",

  data() {
    return {
      searchQuery: '',
      id: null,
      epis: [],
      articles: [],
    };
  },

  computed: {
    ...mapGetters('formules', ['allFormules', 'allCompositions', 'allParametresFormules', 'allArticlesFormules', 'compo', 'settings', 'showMenu', 'expanded']),
    ...mapGetters('epi', ['allEpis', 'allEpisFormules']),

    countFormules() {
      return Array.isArray(this.filteredFormules) ? this.filteredFormules.length : 0;
    },

    filteredFormules() {
      if (this.searchQuery) {
        return this.allFormules.filter(formule =>
          formule.nom.toLowerCase().startsWith(this.searchQuery.toLowerCase())
        );
      }
      return this.allFormules;
    }
  },

  created() {
    this.loadFormules();
    this.loadParametresFormules();
    this.loadCompositions();
  },

  methods: {
    ...mapActions('formules', ['loadFormules', 'loadParametresFormules', 'loadCompositions',  'toggleActivation', 'validFormule',
                               'toggleInfo', 'toggleCompo', 'toggleSettings', 'toggleMenu', 'toggleCloud']),


    filteredParametres(formuleId) {
      return this.allParametresFormules.filter(parametre => parametre.num_formule === formuleId);
    },

    filteredCompositions(formuleId) {
      return this.allCompositions.filter(compo => compo.num_formule === formuleId);
    },

    filterFormules() {
    if (!this.searchQuery) {
      return this.allFormules;
    } else {
      return this.allFormules.filter(formule => {
        return formule.nom.toLowerCase().startsWith(this.searchQuery.toLowerCase());
      });
    }
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
      this.$router.push(`/nouvelle-formule/${id}`);
    }
  }
};
</script>

