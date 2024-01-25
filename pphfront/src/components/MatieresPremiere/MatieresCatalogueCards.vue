<template>
  <q-page>
    <div class="row justify-center">
      <div class="col-md-12">
        <div class="row q-mx-sm q-mt-sm">
          <div class="col-1">
            <router-link to="/creation-matiere-premiere/">
              <q-btn round class="glossy btn-grey-primary-pph" icon="add"/>
            </router-link>
          </div>
          <div class="col-2">
            <!-- <MatieresImport/> -->
          </div>
          <div class="col-2 offset-7">
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
              <template v-slot:append>
                <q-icon name="search" color="cyan-4"/>
              </template>
            </q-input>
          </div>
        </div>
        <div class="row q-mt-sm">
          <div class="col-12 justify-center">
            <div class="row justify-start">
              <div class="col-2 q-pa-sm" v-for="matiere in filteredMatieres" :key="matiere.id" @click="redirectToLink(matiere.id)">
                <q-card bordered class="card-maxi justify-center items-center text-center relative">
                  <div @click="redirectToLink(matiere.id)" class="card-content">
                    <q-img class="logo-card-mini bg-op-8" :src="matiere.fournisseur.logo" :alt="matiere.designation">
                      <div class="absolute-top hover-effect q-my-none text-cyan-1">
                        <div>{{ matiere.designation }}</div>
                        <div>{{ matiere.cdt }} {{ matiere.qté }}{{ matiere.unite }}</div>
                        <div>Ref fournisseur : {{ matiere.code_fournisseur }}</div>
                      <div>ACL : {{ matiere.cip }}</div>
                      </div>
                    </q-img>
                  </div>
                  <q-btn-group class="absolute-bottom-right q-pa-none q-ma-none">

                    <q-btn
                       class="q-pa-none hover-effect"
                       flat
                       color="cyan-4"
                       icon="add_box"
                       @click.stop="openDialog(matiere)"
                    />

                  </q-btn-group>

                </q-card>
              </div>
               <q-dialog v-model="addDialog">
                    <q-card>
                      <q-card-section>
                        <div class="row justify-center text-h6 text-cyan-4">Intégrer une matière première</div>
                      </q-card-section>
                      <q-separator/>
                      <q-card-section>

                        <div class="row">
                          <div class="col-8">
                            <q-input v-model="selectedMatiere.designation" label="Désignation" />
                          </div>
                        </div>

                        <div class="row">
                          <div class="col-3">
                            <q-input v-model="selectedMatiere.fournisseur.name" label="Fournisseur" />
                          </div>
                        </div>

                        <div class="row">
                          <div class="col-3">
                            <q-input v-model="selectedMatiere.code_fournisseur" label="Code fournisseur" />
                          </div>
                          <div class="col-3 offset-1">
                            <q-input v-model="selectedMatiere.cip" label="ACL" />
                          </div>
                        </div>

                        <div class="row">
                          <div class="col-3">
                            <q-input v-model="selectedMatiere.cdt" label="Conditionnement" />
                          </div>
                          <div class="col-2 offset-1">
                            <q-input v-model="selectedMatiere.qté" label="Quantité cdt" />
                          </div>
                          <div class="col-2 offset-1">
                            <q-input v-model="selectedMatiere.unite" label="Unité" />
                          </div>
                        </div>

                        <div class="row">
                          <div class="col-2">
                            <q-input v-model="selectedMatiere.prix" label="Prix" />
                          </div>
                        </div>
                      </q-card-section>
                      <q-separator/>
                      <q-card-section>
                        <div class="row justify-center">
                        <q-btn-group>
                          <q-btn flat label="Transférer" @click="transfert()" color="green-4"/>
                          <q-btn flat label="Annuler" @click="addDialog=false" color="red-4"/>
                        </q-btn-group>
                          </div>
                      </q-card-section>
                    </q-card>
                  </q-dialog>
            </div>
          </div>
        </div>
      </div>
    </div>
  </q-page>
</template>

<script>
import { mapActions, mapGetters } from 'vuex';
// import MatieresImport from './MatieresImport.vue'

export default {
  name: "MatieresCatalogueCards",

  data() {
    return {
      searchQuery: '',
      currentPage: 1,
      perPage: 24,
      addDialog: false,
      selectedMatiere: null,
    };
  },

  computed: {
    ...mapGetters('matieresPremieres', ['allMatieresCatalogue', 'showMenu', 'expanded']),

    filteredMatieres() {
      let start = (this.currentPage - 1) * this.perPage;
      let end = this.currentPage * this.perPage;
      let filtered = this.allMatieresCatalogue;
      if (this.searchQuery) {
        filtered = filtered.filter(matiere =>
          matiere.designation.toLowerCase().startsWith(this.searchQuery.toLowerCase())
        );
      }
      return filtered.slice(start, end);
    }
  },

  created() {
    this.loadMatieresPremieresCatalogue();
    window.addEventListener('scroll', this.handleScroll);
    console.log('allmatieresCatalogue', this.allMatieresCatalogue)
    console.log('loadCatalogue', this.loadMatieresPremieresCatalogue)
  },

  unmounted() {
    window.removeEventListener('scroll', this.handleScroll);
  },

  methods: {
    ...mapActions('matieresPremieres', ['loadMatieresPremieresCatalogue', 'toggleActivation', 'toggleMenu', 'toggleInfo']),

    openDialog(matiere) {
      this.selectedMatiere = { ...matiere };
      this.addDialog = true;
    },
    transfert() {
      // Logique de mise à jour des données de la matière première
      // Par exemple, envoie les données modifiées à votre serveur/API
    },
    handleScroll() {
      let bottomOfWindow = document.documentElement.scrollTop + window.innerHeight === document.documentElement.offsetHeight;
      if (bottomOfWindow) {
        this.loadMore();
      }
    },

    loadMore() {
      this.currentPage++;
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



