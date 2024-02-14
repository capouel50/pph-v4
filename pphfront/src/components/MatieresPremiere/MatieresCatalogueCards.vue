<template>
  <q-page v-if="isLoading" class="row items-center justify-center">
  <div class=" row justify-center">
      <atom-spinner
        class="bg-op-8"
        :animation-duration="1000"
        :size="200"
        :color="'#ff1d5e'"
      />
      </div>
  </q-page>
  <q-page v-else>
    <div class="row justify-center">
      <div class="col-md-12">
        <div class="row q-mx-sm">
          <div class="col-1 q-mt-md">
            <q-fab size="sm" glossy class="btn-grey-primary-pph" icon="add_box" direction="right">
              <q-fab-action glossy external-label label-position="bottom"
                            label="Excel"
                            class="btn-grey-primary-pph"
                            @click="importCatalogueExcel=true" icon="playlist_add" />
              <q-fab-action glossy external-label label-position="bottom"
                            label="PDF"
                            class="btn-grey-primary-pph"
                            @click="importCatalogue=true" icon="post_add" />
              <q-fab-action glossy external-label label-position="bottom"
                            label="Site"
                            class="btn-grey-primary-pph"
                            @click="selectColumns=true" icon="add_business" />

              <q-form enctype="multipart/form-data">
                <q-dialog
                    v-model="importCatalogueExcel"
                >
                  <q-card>
                    <q-card-section>
                      <div class="row text-h6 text-cyan-4 justify-center">
                        Importer un catalogue Excel
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
                            label="Sélectionner un fichier.xls"
                            accept=".xls"
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
                          <q-btn flat label="Colonnes" @click="importCatalogueExcel=false;SelectColumns=true" color="green-4"/>
                          <q-btn flat label="Annuler" @click="importCatalogue=false" color="red-4"/>
                        </q-btn-group>
                      </div>
                    </q-card-section>
                  </q-card>
                </q-dialog>
                <q-dialog v-model="selectColumns">
                    <q-card>
                      <div class="row text-cyan-4 justify-center text-h6">
                           Importer un catalogue Excel
                         </div>
                      <q-separator/>
                     <q-splitter
                         horizontal
                     >
                       <template v-slot:after>

                         <div class="row text-orange-4 justify-center text-subtitle2">
                           Données a importer
                         </div>
                         <div class="row">
                         <div class="col">
                          <div class="drop-target" @dragover="onDragOver" @drop="onDrop">
                            <div
                              v-for="(label, index) in labels"
                              :key="index"
                              class="label q-mx-xs"
                              :class="{ 'active': isLabelActive(label) }"
                              @dragenter="onLabelDragEnter(label)"
                              @dragleave="onLabelDragLeave(label)"
                            >
                              {{ label }}
                          </div>
                          </div>
                         </div>
                        </div>
                       </template>
                       <template v-slot:before>
                         <div class="row text-orange-4 justify-center text-subtitle2">
                           Colonnes du fichier Excel
                         </div>
                          <div class="items">
                            <div
                              v-for="(item, index) in items"
                              :key="index"
                              class="item q-mx-xsm run "
                              :draggable="true"
                              @dragstart="onDragStart(index)"
                              @dragend="onDragEnd"
                            >
                              {{ item }}
                            </div>
                          </div>
                      </template>
                      </q-splitter>
                      <q-separator/>
                      <div class="row justify-center">
                      <q-card-actions>
                        <q-btn-group>
                        <q-btn flat label="Importer" @click="transfert" color="green-4" />
                        <q-btn flat label="Annuler" @click="selectColumns=false" color="red-4" />
                        </q-btn-group>
                      </q-card-actions>
                      </div>
                    </q-card>
                  </q-dialog>
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
              </q-fab>
          </div>

          <div class="col-6 offset-2 q-mt-md text-cyan-4 text-h6">
            <div class="row justify-center">
            {{ countMatieresCatalogue }} matières premières disponibles
              <q-btn
              flat
              size="md"
              @click="toggleCard = !toggleCard"
              :icon="toggleCard ? 'list' : 'grid_view'"
            />
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
            <div v-if="toggleCard" class="row justify-start">
              <div class="col-2 q-pa-sm" v-for="matiere in filteredMatieres" :key="matiere.id"
                   @click="redirectToLink(matiere.id)">
                <q-card bordered
                        class="card-maxi justify-center items-center text-center relative">

                  <div>
                    <q-img class="logo-card-mini"
                           src="../../assets/img/blanc.jpg"
                           loading="lazy"
                           spinner-color="red-4"
                           :alt="matiere.designation"
                    >
                      <q-icon
                          :name="matiere.fournisseur.name === 'Cooper' ? 'copyright' : 'info'"
                          class="icon-background"
                      />
                      <div class="absolute-top hover-effect q-my-none text-cyan-1">
                        <div>{{ matiere.designation }}</div>
                        <div>{{ matiere.prix }}€ - {{ matiere.qté }}{{ matiere.unite }}</div>
                        <div>Ref fournisseur : {{ matiere.code_fournisseur }}</div>
                        <div>EAN : {{ matiere.cip }}</div>
                      </div>
                      <template v-slot:loading>
                        <q-spinner-rings color="red-4" />
                      </template>
                    </q-img>
                  </div>
                  <div v-if="matiere.cmr" class="absolute-bottom-left">
                    <q-img v-if="matiere.cmr" class="q-ml-xs q-mb-xs fade-blink" src="@/assets/img/health_hazard.png" :style="{ width: '30px', height: '30px' }"/>
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
            </div>
            <div v-else class="row">
                <q-list bordered class="col-12 bg-white bg-op-8">
                  <div class="row">
                    <div class="col-3 text-center">Désignation</div>
                    <div class="col-1 text-center">Conditionnement</div>
                    <div class="col-1 text-center">Prix HT</div>
                    <div class="col-2 text-center">Ref fournisseur</div>
                    <div class="col-2 text-center">EAN</div>
                    <div class="col-1 text-center">Fournisseur</div>
                  </div>
                  <q-item class="row hover-effect" v-for="matiere in filteredMatieres" :key="matiere.id" clickable @click="redirectToLink(matiere.id)">

                    <q-item-section class="col-3">
                      <q-item-label>{{ matiere.designation }}</q-item-label>
                    </q-item-section>

                    <q-item-section class="col-1 text-center">
                      <q-item-label caption>{{ matiere.qté }}{{ matiere.unite }}</q-item-label>
                    </q-item-section>

                    <q-item-section class="col-1 text-center">
                      <q-item-label caption>{{ matiere.prix }}€</q-item-label>
                    </q-item-section>

                    <q-item-section class="col-2 text-center">
                      <q-item-label caption>{{ matiere.code_fournisseur }}</q-item-label>
                    </q-item-section>

                    <q-item-section class="col-2 text-center">
                      <q-item-label caption>{{ matiere.cip }}</q-item-label>
                    </q-item-section>

                    <q-item-section class="col-1 text-center">
                      <q-item-label caption>{{ matiere.fournisseur.name }}</q-item-label>
                    </q-item-section>

                    <q-item-section class="col-1 text-center">
                      <font-awesome-icon v-if="matiere.cmr" fade size="fa-lg" icon="fa-solid fa-skull-crossbones" style="color: #e57373;" class="q-ml-md"/>
                    </q-item-section>

                    <q-item-section class="col-1">
                      <q-btn flat icon="add_box" color="cyan-4" @click.stop="openDialog(matiere)" />
                    </q-item-section>

                  </q-item>
                </q-list>

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
import {AtomSpinner} from 'epic-spinners'

export default {
  name: "MatieresCatalogueCards",
  components: {
    AtomSpinner,
  },

  data() {
    return {
      toggleCard: true,
      showing: true,
      items: ['Item 1', 'Item 2','Item 3', 'Item 4', 'Item 5'],
      labels: ['Nom', 'Code fournisseur', 'CIP/EAN', 'Prix'],
      activeLabel: null,
      selectColumns: false,
      importCatalogueExcel: false,
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
    ...mapGetters('matieresPremieres', ['allMatieresCatalogue','allCategories', 'showMenu', 'expanded', 'loadingMatieres']),
    ...mapGetters('suppliers', ['allSuppliers']),
    ...mapGetters('spinner', ['isLoading']),

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
    this.showing=false;

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



    onDragStart(index) {
      // Gérer le démarrage du glissement de l'élément
      event.dataTransfer.setData('text/plain', index);
    },
    onDragEnd() {
      // Réinitialiser l'étiquette active après le glissement
      this.activeLabel = null;
    },
    onLabelDragEnter(label) {
      // Gérer l'entrée du glissement dans une étiquette
      this.activeLabel = label;
    },
    onLabelDragLeave(label) {
      // Gérer la sortie du glissement d'une étiquette
      if (this.activeLabel === label) {
        this.activeLabel = null;
      }
    },
    onDragOver(event) {
      // Gérer le survol de la zone de dépôt
      event.preventDefault();
    },
    onDrop(event) {
      // Gérer le dépôt de l'élément
      event.preventDefault();
      const index = event.dataTransfer.getData('text/plain');
      if (this.activeLabel !== null) {
        // Associer l'élément à l'étiquette active
        this.labels[this.labels.indexOf(this.activeLabel)] = `${this.activeLabel}: ${this.items[index]}`;
        // Supprimer l'élément de la liste des items
        this.items.splice(index, 1);
      }
    },
    isLabelActive(label) {
      // Vérifier si l'étiquette est active
      return this.activeLabel === label;
    },

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
        data_source: "PDF"
      };
      console.log(formData);
      this.addImport(formData)
        .then(() => {
          this.importCatalogue=false;
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

<style scoped>
.drop-target {
  display: flex;
  justify-content: space-between;
  border: 2px dashed #4dd0e1;
  border-radius: 10px;
  padding: 10px;
  margin: 10px;
}

.label {
  width: 30%;
  padding: 10px;
  text-align: center;
  border: 2px solid #4dd0e1;
  border-radius: 10px;
  cursor: pointer;
}

.label.active {
  background-color: #ffb74d;
}

.items {
  display: flex;
  justify-content: space-between;
  padding: 10px;
}

.item {
  width: 30%;
  padding: 10px;
  text-align: center;
  border: 2px solid #4dd0e1;
  border-radius: 10px;
  cursor: grab;
}
</style>

