<template>
  <q-page>
    <div class="row justify-center">
      <div class="col-md-12">
        <div class="row q-mx-sm">
          <div class="col-1 q-mt-md">
              <q-btn
                  round
                  class="glossy btn-grey-primary-pph"
                  icon="playlist_add"
                  @click="importCatalogue=true"
              >
              <q-form enctype="multipart/form-data">
                <q-dialog
                    v-model="importCatalogue"
                >
                  <q-card>
                    <q-card-section>
                      <div class="row text-h6 text-cyan-4 justify-center">
                        Importer un catalogue
                      </div>
                    </q-card-section>
                    <q-separator/>
                    <q-card-section>
                      <div class="row text-subtitle1 text-orange-4">
                        Données du catalogue
                      </div>
                      <div class="row">
                        <div class="col-12">
                          <q-file
                            label="Sélectionner un fichier.pdf"
                            accept=".pdf"
                            v-model="selectedFile"
                          />
                        </div>
                      </div>
                      <div class="row">
                        <div class="col-6">
                          <q-select
                              label="Fournisseur"
                              color="cyan-4"
                              v-model="selectedSupplier"
                              :options="suppliersOptions"
                              options-label="label"
                              options-value="value"
                              @input="onSupplierChange"
                          />
                        </div>
                        <div class="col-5 offset-1">
                          <q-select
                              label="Catégorie"
                              color="cyan-4"
                              v-model="selectedCategory"
                              :options="categoriesOptions"
                              options-label="label"
                              options-value="value"
                          />
                        </div>
                      </div>
                    </q-card-section>
                    <q-card-section>
                      <div class="row text-subtitle1 text-orange-4">
                        Plage d'extraction
                      </div>
                      <div class="row">
                        <div class="col-4">
                          <q-input
                          label="Page de début"
                          v-model="pageDebut"
                          color="cyan-4"
                          />
                        </div>
                        <div class="col-4 offset-1">
                          <q-input
                          label="Page de fin"
                          v-model="pageFin"
                          color="cyan-4"
                        />
                        </div>
                      </div>

                      <div class="row">
                        <div class="col-4">
                          <q-input
                          label="Code CPF de début"
                          v-model="codeDebut"
                          color="cyan-4"
                          :mask="maskFormat"
                          />
                        </div>
                        <div class="col-4 offset-1">
                          <q-input
                          label="Code CPF de fin"
                          v-model="codeFin"
                          color="cyan-4"
                          :mask="maskFormat"
                          />
                        </div>

                      </div>
                    </q-card-section>
                      <q-separator/>
                    <q-card-section>
                      <div class="row justify-center">
                        <q-btn-group>
                          <q-btn flat label="Importer" @click="importer" color="green-4"/>
                          <q-btn flat label="Annuler" @click="importCatalogue=false" color="red-4"/>
                        </q-btn-group>
                      </div>
                    </q-card-section>

                  </q-card>
                </q-dialog>
              </q-form>
              </q-btn>
          </div>
          <div class="col-6 offset-2 q-mt-md text-cyan-4 text-h6">
            <div class="row justify-center">
            {{ countMatieresCatalogue }} matières premières disponibles
            </div>
          </div>

          <div class="col-2 offset-1">
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
                <q-card bordered
                        class="card-maxi justify-center items-center text-center relative">
                  <div @click="redirectToLink(matiere.id)" class="card-content">
                    <q-img class="logo-card-mini"
                           :src="matiere.fournisseur.logo"
                           :alt="matiere.designation"
                    >
                      <div class="absolute-top hover-effect q-my-none text-cyan-1">
                        <div>{{ matiere.designation }}</div>
                        <div>{{ matiere.prix }}€ - {{ matiere.qté }}{{ matiere.unite }}</div>
                        <div>Ref fournisseur : {{ matiere.code_fournisseur }}</div>
                      <div>EAN : {{ matiere.cip }}</div>
                      </div>
                    </q-img>
                  </div>
                  <div v-if="matiere.cmr" class="absolute-bottom-left">
                    <font-awesome-icon fade icon="fa-solid fa-skull-crossbones" class="q-ml-xs q-mb-xs fa-2x" style="color: #e57373;"/>
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
               <q-form>
            <q-dialog v-model="addMatiereCat">
                    <q-card>
                      <q-card-section>
                        <div class="row justify-center text-h6 text-cyan-4">
                          Intégrer
                        </div><br/>
                        <div class="row justify-center text-subtitle1 text-orange-4">
                        {{ selectedMatiere.designation }} {{ selectedMatiere.cdt }}
                          {{ selectedMatiere.qté }}{{ selectedMatiere.unite }} {{ selectedMatiere.fournisseur.name }} ref:{{ selectedMatiere.code_fournisseur }}
                        </div><br/>
                        <div class="row justify-center text-h6 text-cyan-4">
                          aux matières premières
                        </div>
                      </q-card-section>
                      <q-separator/>
                      <q-card-section>

                        <div class="row">
                          <div class="col-12">
                            <q-input v-model="nom"
                                     label="Désignation" color="cyan-4" class="hover-effect">
                              <template v-slot:prepend>
                                <q-btn flat color="cyan-4"
                                       class="hover-effect-success"
                                       @click="this.nom=this.selectedMatiere.designation"
                                >
                                <font-awesome-icon size="fa-sm" icon="fa-solid fa-clone"/>
                                </q-btn>
                              </template>
                            </q-input>
                          </div>
                        </div>
                        <div class="row">
                          <div class="col-6">
                            <q-toggle v-model="stockee" size="md" icon="inventory" label="Stockée" color="green-4"/>
                          </div>
                          <div class="col-6">
                            <q-toggle v-model="cde_auto" size="md" icon="list_alt" label="Commande auto" color="purple-4"/>
                          </div>
                        </div>
                        <div class="row">
                          <div class="col-5">
                            <q-select
                              label="Unité de mesure"
                              class="hover-effect"
                              color="cyan-4"
                              v-model="uniteMesure"
                              :options="unitesOptions"
                              options-label="label"
                              options-value="value"
                            />
                          </div>
                          <div class="col-5 offset-1">
                            <q-select
                              label="Liste"
                              class="hover-effect"
                              color="cyan-4"
                              v-model="liste"
                              :options="listesOptions"
                              options-label="label"
                              options-value="value"
                            />
                          </div>
                        </div>
                        <div class="row">
                          <div class="col-5">
                            <q-input v-model="stock_mini" label="Stock mini" color="cyan-4">
                              <template v-slot:append>
                                <div class="uniteStockName text-subtitle2 text-cyan-4">{{ uniteStockNom }}</div>
                              </template>
                            </q-input>
                          </div>
                          <div class="col-5 offset-1">
                            <q-select
                              label="Forme"
                              class="hover-effect"
                              color="cyan-4"
                              v-model="forme"
                              :options="formesOptions"
                              options-label="label"
                              options-value="value"
                            />
                          </div>
                        </div>
                      </q-card-section>
                      <q-separator/>
                      <q-card-section>
                        <div class="row justify-center">
                        <q-btn-group>
                          <q-btn flat label="Transférer" @click="transfert" color="green-4"/>
                          <q-btn flat label="Annuler" @click="addMatiereCat=false" color="red-4"/>
                        </q-btn-group>
                          </div>
                      </q-card-section>
                    </q-card>
                  </q-dialog>
             </q-form>
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
  name: "MatieresCatalogueCards",

  data() {
    return {
      importCatalogue: false,
      searchQuery: '',
      currentPage: 1,
      perPage: 24,
      addDialog: false,
      selectedFile: null,
      selectedMatiere: null,
      selectedSupplier: null, // Ajoutez une nouvelle propriété pour le fournisseur sélectionné
      selectedCategory: null,
      pageDebut: '',
      pageFin: '',
      codeDebut: '',
      codeFin: '',
      suppliersOptions: [], // Options pour le champ de sélection du fournisseur
      categoriesOptions: [],
      maskFormat: '# ### ###',
    };
  },

  computed: {
    ...mapGetters('matieresPremieres', ['allMatieresCatalogue','allCategories', 'showMenu', 'expanded']),
    ...mapGetters('suppliers', ['allSuppliers']),

    countMatieresCatalogue() {
      return this.allMatieresCatalogue.length;
    },

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

  async mounted() {
    await this.loadMatieresPremieresCatalogue();
    await this.loadCategoriesMatieres();
    await this.loadSuppliers();

    this.suppliersOptions = this.allSuppliers
      .filter(supplier => supplier.download_catalogue === true)
      .map(supplier => ({
      label: supplier.name,
      value: supplier.id,
    }));

    window.addEventListener('scroll', this.handleScroll);

  },

  unmounted() {
    window.removeEventListener('scroll', this.handleScroll);
  },

  watch: {
      selectedSupplier: 'onSupplierChange',
  },

  methods: {
    ...mapActions('matieresPremieres', ['loadMatieresPremieresCatalogue', 'loadCategoriesMatieres',
                                        'addImport',
                                        'toggleActivation', 'toggleMenu', 'toggleInfo']),
    ...mapActions('suppliers', ['loadSuppliers']),

    onSupplierChange() {
      console.log('suuplierId', this.selectedSupplier);
    if (this.selectedSupplier) {
      // Filtrer les catégories en fonction de l'ID du fournisseur sélectionné
      this.categoriesOptions = this.allCategories
        .filter(category => category.fournisseur.id === this.selectedSupplier.value)
        .map(category => ({
          label: category.nom,
          value: category.id,
        }));
    } else {
      // Réinitialiser les catégories si aucun fournisseur n'est sélectionné
      this.categoriesOptions = this.allCategories.map(category => ({
        label: category.nom,
        value: category.id,
      }));
    }
  },

    openDialog(matiere) {
      this.selectedMatiere = { ...matiere };
      this.addDialog = true;
    },
    importer() {
      console.log("Le formulaire est soumis");
      const formData = {
        pdf: this.selectedFile,
        fournisseur: this.selectedSupplier.value,
        categorie: this.selectedCategory.value,
        page_debut: this.pageDebut,
        page_fin: this.pageFin,
        code_debut: this.codeDebut,
        code_fin: this.codeFin,
      };
      console.log(formData);
      this.addImport(formData)
        .then(() => {
          // L'importation est réussie, chargez à nouveau les matières premières du catalogue
          this.loadMatieresPremieresCatalogue();
        });
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



