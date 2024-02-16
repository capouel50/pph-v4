<template>
  <q-page>
    <div class="row justify-center">
      <div class="col-md-12">
        <div class="row q-mx-sm">
          <div class="col-4 offset-4 q-mt-md text-cyan-4 text-h6">
            <div class="row justify-center">
            {{ controlCount }} fiches en attente de contrôle
            </div>
          </div>
          <div class="col-2 offset-2">
            <q-input
                ref="searchInput"
                v-model="searchQuery"
                label="Recherche..."
                @input="filteredFiches"
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
              <div class="col-2 q-pa-sm" v-for="fiche in filteredFiches" :key="fiche.id">
                <q-card bordered class="card-maxi justify-center items-center text-center relative">
                  <div class="card-content">
                    <q-img
                        class="logo-card-mini"
                        src="../../assets/img/blanc.jpg"
                        :alt="fiche.prep.nom"
                        loading="lazy"
                        spinner-color="red-4"
                    >
                      <div class="absolute-top hover-effect q-my-none text-cyan-1">
                        <div>{{ fiche.date_fab }}</div>
                        <div v-if="fiche.patient">{{ fiche.patient }}</div>
                        <div>{{ fiche.prep.nom }}</div>
                      </div>
                      <template v-slot:loading>
                        <q-spinner-rings color="red-4" />
                      </template>
                    </q-img>
                    <q-btn flat color="white" class="absolute-top-right hover-effect q-pa-none q-ma-none" icon="more_vert" @click.stop="toggleMenu(fiche.id)" />
                    <q-menu fit anchor="top right" self="bottom middle" v-model="showMenu[fiche.id]">
                      <q-list style="min-width: 100px">
                        <q-item clickable v-close-popup @click.stop="toggleControle({ ficheId: fiche.id, isControl: fiche.controle_valide })">
                          <q-item-section class="hover-effect-success">
                            Valider contrôle
                          </q-item-section>
                        </q-item>
                        <q-item clickable v-close-popup @click.stop="toggleDestruction(fiche.id)">
                          <q-item-section class="hover-effect-warning">Destruction</q-item-section>
                        </q-item>
                      </q-list>
                    </q-menu>
                  </div>
                  <div class="absolute-top-left hover-effect q-ml-xs q-my-none text-red-4">
                    <div>{{ fiche.id }}</div>
                  </div>
                  <div class="absolute-bottom-left">
                    <div class="row">
                      <font-awesome-icon v-if="fiche.prep.froid" fade icon="fa-solid fa-snowflake" class="q-ml-xs q-mb-xs fa-2x" style="color: #4dd0e1;" />
                      <q-icon v-if="fiche.prep.agiter" name="waving_hand" class="q-ml-xs q-mb-xs" color="cyan-4" size="md"/>
                      <q-icon v-if="fiche.prep.lumiere" name="light_mode" class="q-ml-xs q-mb-xs" color="red-4" size="md"/>
                    </div>
                  </div>
                  <q-btn-group class="absolute-bottom-right q-pa-none q-ma-none">
                    <q-btn
                       class="q-pa-none hover-effect"
                       flat
                       color="cyan-4"
                       icon="list"
                       @click.stop="toggleCompo(fiche.id)"
                    />
                    <q-btn
                       class="q-pa-none hover-effect"
                       flat
                       color="cyan-4"
                       icon="settings"
                       @click.stop="toggleSettings(fiche.id)"
                    />
                    <q-btn
                      class="hover-effect"
                      color="cyan-4"
                      round
                      flat
                      dense
                      icon="info"
                      @click.stop="toggleInfo(fiche.id)"
                    />
                  </q-btn-group>
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
  name: "ControlesCards",

  data() {
    return {
      searchQuery: '',
    };
  },

  computed: {
    ...mapGetters('fiches', ['allFiches', 'fichesControlCount', 'showMenu', 'settings', 'info', 'compo']),

    controlCount() {
      return this.fichesControlCount;
    },

    filteredFichesControle() {
      return this.allFiches.filter(fiche => fiche.attente_controle === true);
    },

    filteredFiches() {
      if (this.searchQuery) {
        return this.filteredFichesControle.filter(fiche =>
            fiche.prep.nom.toLowerCase().startsWith(this.searchQuery.toLowerCase()) ||
            fiche.id.toString().startsWith(this.searchQuery.toLowerCase()) ||
            fiche.patient.toLowerCase().startsWith(this.searchQuery.toLowerCase())
        );
      }
      return this.filteredFichesControle;
    },
  },

  created() {
    this.loadFiches();
    console.log('filteredfiches:', this.filteredFichesControle)
    console.log('allfiches:', this.allFiches)
  },

  methods: {
    ...mapActions('fiches', ['loadFiches', 'toggleInfo', 'toggleSettings', 'toggleCompo', 'toggleControle', 'toggleMenu']),

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



