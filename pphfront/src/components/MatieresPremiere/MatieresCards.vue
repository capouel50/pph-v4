<template>
  <q-page>
    <div class="row justify-center">
      <div class="col-md-12">
        <div class="row">
          <div class="col-1 q-ml-sm q-mt-sm">
            <router-link to="/supplier/">
              <q-btn round class="glossy btn-grey-primary-pph" icon="add"/>
            </router-link>
          </div>
          <div class="col-2 q-ml-xl-md offset-8">
            <q-input
                ref="searchInput"
                v-model="searchQuery"
                label="Recherche..."
                @input="filterMatieres"
                color="cyan-4"
                @mouseover="changeLabelColor('searchInput', '#ffb74d')"
                @mouseleave="changeLabelColor('searchInput', '')"
                @focus="onFocus('searchQuery', '#4dd0e1')"
                @blur="onBlur('searchQuery')"
            >
              <template v-slot:before>
                <q-icon name="search" color="cyan-4"/>
              </template>
            </q-input>
          </div>
        </div>
        <div class="row q-mt-sm">
          <div class="col-9 justify-center">
            <div class="row justify-start">
              <div class="col-2 q-pa-sm" v-for="matiere in filteredMatieres" :key="matiere.id" @click="redirectToLink(matiere.id)">
                <q-card bordered class="card-maxi justify-center items-center text-center relative" :class="{ 'bd-red-4': !matiere.stockee}">
                  <div @click="redirectToLink(matiere.id)" class="card-content">
                    <q-img class="logo-card-mini" :src="matiere.type.logo" :alt="matiere.type.nom">
                      <div class="absolute-top hover-effect q-my-none" :class="{ 'text-cyan-1': matiere.stockee, 'text-red-4': !matiere.stockee }">
                        <div>{{ matiere.nom }}</div>
                        <div>{{ matiere.forme.nom }} {{ matiere.qté_cdt }}{{ matiere.forme.unite_mesure.nom }}</div>
                        <div>
                          <q-icon v-if="matiere.qté_stock < matiere.stock_mini" name="warning" color="red-4"/>
                          Stock : {{ matiere.qté_stock }}{{ matiere.forme.unite_stock }}
                        </div>
                      </div>
                    </q-img>
                    <q-btn flat color="white" class="absolute-top-right hover-effect q-pa-none q-ma-none"
                           icon="more_vert" @click.stop="toggleMenu(matiere.id)"
                    />
                    <q-menu fit anchor="top right" self="bottom middle" v-model="showMenu[matiere.id]">
                      <q-list style="min-width: 100px">
                        <q-item clickable v-close-popup @click.stop="deleteMatiere(matiere.id)">
                          <q-item-section class="hover-effect">Supprimer</q-item-section>
                        </q-item>
                        <q-item clickable v-close-popup @click.stop="toggleActivation({ matiereId: matiere.id, isStockee: matiere.stockee })">
                          <q-item-section class="hover-effect">
                            {{ matiere.stockee ? 'Non Stockée' : 'Stockée' }}
                          </q-item-section>
                        </q-item>
                      </q-list>
                    </q-menu>
                  </div>
                  <q-btn-group class="absolute-bottom-right q-pa-none q-ma-none">
                    <q-btn
                       class="q-pa-none hover-effect"
                       flat
                       color="cyan-4"
                       icon="bar_chart"
                    />
                    <q-btn
                       class="q-pa-none hover-effect"
                       flat
                       color="cyan-4"
                       icon="playlist_add"
                    />
                    <q-btn
                      class="hover-effect"
                      color="cyan-4"
                      round
                      flat
                      dense
                      icon="info"
                      @click.stop="toggleInfo(matiere.id)"
                    />
                  </q-btn-group>

                  <q-menu fit anchor="bottom right" self="top middle" v-model="expanded[matiere.id]">
                    <q-list style="min-width: 100px">
                      <q-item v-if="matiere.fournisseur">
                        <q-item-section avatar class="text-cyan-4">
                          Fournisseur :
                        </q-item-section>
                        <q-item-section class="text-grey-7">
                          {{ matiere.fournisseur.name }}
                        </q-item-section>
                      </q-item>
                      <q-item v-if="matiere.prix">
                        <q-item-section avatar class="text-cyan-4">
                          Prix :
                        </q-item-section>
                        <q-item-section class="text-grey-7">
                          {{ matiere.prix }} €
                        </q-item-section>
                      </q-item>
                      <q-item v-if="matiere.prix_unit">
                        <q-item-section avatar class="text-cyan-4">
                          Prix unitaire :
                        </q-item-section>
                        <q-item-section class="text-grey-7">
                          {{ matiere.prix_unit }} €/{{ matiere.forme.unite_stock }}
                        </q-item-section>
                      </q-item>
                      <q-item v-if="matiere.stock_mini">
                        <q-item-section avatar class="text-cyan-4">
                          Stock mini :
                        </q-item-section>
                        <q-item-section class="text-grey-7">
                          {{ matiere.stock_mini }}{{ matiere.forme.unite_stock }}
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
  name: "MatieresCards",

  data() {
    return {
      searchQuery: '',
    };
  },

  computed: {
    ...mapGetters('matieresPremieres', ['allMatieres', 'showMenu', 'expanded']),

    filteredMatieres() {
      if (this.searchQuery) {
        return this.allMatieres.filter(matiere =>
          matiere.nom.toLowerCase().startsWith(this.searchQuery.toLowerCase())
        );
      }
      return this.allMatieres;
    }
  },

  created() {
    this.loadMatieresPremieres();
  },

  methods: {
    ...mapActions('matieresPremieres', ['loadMatieresPremieres', 'deleteMatiere', 'toggleActivation', 'toggleMenu', 'toggleInfo']),

    filterMatieres() {
      if (!this.searchQuery) {
        return this.allMatieres;
      } else {
        return this.allMatieres.filter(matiere => {
          return matiere.nom.toLowerCase().startsWith(this.searchQuery.toLowerCase());
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
      this.$router.push(`/matiere/${id}`);
    },
  }
};
</script>



