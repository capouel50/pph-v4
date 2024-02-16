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
                        <div>{{ demande.qté }} {{ demande.prep.nom }}</div>
                        <div>Pour le {{ demande.date_prevu }}</div>
                        <div v-if="demande.service">{{ demande.service.nom }}</div>
                      </div>
                      <template v-slot:loading>
                        <q-spinner-rings color="red-4" />
                      </template>
                    </q-img>
                    <q-btn flat color="white" class="absolute-top-right hover-effect q-pa-none q-ma-none" icon="more_vert" @click.stop="toggleMenu(demande.id)" />
                    <q-menu fit anchor="top right" self="bottom middle" v-model="showMenu[demande.id]">
                      <q-list style="min-width: 100px">
                        <q-item clickable v-close-popup @click.stop="toggleProduction(demande.id)">
                          <q-item-section class="hover-effect-success">
                            Générer fiche de fabrication
                          </q-item-section>
                        </q-item>
                        <q-item clickable v-close-popup @click.stop="deleteDemande(demande.id)">
                          <q-item-section class="hover-effect-warning">Supprimer</q-item-section>
                        </q-item>
                      </q-list>
                    </q-menu>
                  </div>
                  <div class="absolute-bottom-left">
                    <div class="row">
                      <font-awesome-icon v-if="demande.prep.froid" fade icon="fa-solid fa-snowflake" class="q-ml-xs q-mb-xs fa-2x" style="color: #4dd0e1;" />
                      <q-icon v-if="demande.prep.lumiere" name="light_mode" class="q-ml-xs q-mb-xs" color="red-4" size="md"/>
                    </div>
                  </div>
                  <q-btn-group class="absolute-bottom-right q-pa-none q-ma-none">
                    <q-btn
                      class="hover-effect"
                      color="cyan-4"
                      round
                      flat
                      dense
                      icon="info"
                      @click.stop="toggleInfo(demande.id)"
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
  name: "demandesCards",

  data() {
    return {
      searchQuery: '',
    };
  },

  computed: {
    ...mapGetters('demandes', ['allDemandes', 'showMenu', 'info']),

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
  },

  methods: {
    ...mapActions('demandes', ['loadDemandes', 'toggleInfo', 'toggleMenu']),

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



