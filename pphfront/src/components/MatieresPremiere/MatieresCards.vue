<template>
  <q-page v-if="loadMatieresPremieres">
    <div class="row justify-center">
      <div class="col-md-12">
        <div class="row q-mx-sm q-mt-sm">
          <div class="col-3 q-mt-sm">
            <div class="row">

           <q-input
              ref="searchCatalogueInput"
              v-model="searchCatalogueQuery"
              label="Importer..."
              color="cyan-4"
              @input="filterCatalogueMatieres"
              @mouseover="changeLabelColor('searchCatalogueInput', '#ffb74d')"
              @mouseleave="changeLabelColor('searchCatalogueInput', '')"
              @focus="onFocus('searchCatalogueQuery', '#4dd0e1')"
              @blur="onBlur('searchCatalogueQuery')"
            >
              <template v-slot:before>
                <router-link to="/creation-matiere-premiere/">
                  <q-btn round icon="add_box" class="glossy btn-cyan-pph"/>
                </router-link>
              </template>
              <template v-slot:append>
                <q-icon v-if="searchCatalogueQuery.length < 1"
                                   name="search"
                                   style="color: #4dd0e1;"
                />
                <q-btn v-else-if="searchCatalogueQuery.length >= 1 && filteredMatieresCatalogue.length > 0"
                       size="lg"
                       @click="toogleMenuMat"
                       class="hover-effect-success q-pa-xs"
                       flat
                >
                  <font-awesome-icon
                                   icon="fa-solid fa-magnifying-glass-plus"
                                   beat-fade
                                   style="color: #a1d19b;"
                />
                </q-btn>
                <font-awesome-icon v-else
                                   icon="fa-solid fa-magnifying-glass-plus"
                                   fade
                                   style="color: #d59e9e;"
                                   size="fa-md"
                />
              </template>
              <q-menu v-model="menuMat" v-if="searchCatalogueQuery.length >= 1" anchor="bottom left">
                <q-list>
                  <q-item
                    v-for="matiere in filteredMatieresCatalogue"
                    :key="matiere.id"
                    clickable
                    @click="selectMatiere(matiere)"
                    class="hover-effect"
                  >
                    <!-- Insérez ici le contenu que vous souhaitez afficher pour chaque élément -->
                    {{ matiere.designation }},
                    {{ matiere.cdt }} {{ matiere.qté }}{{ matiere.unite }},
                    {{ matiere.fournisseur.name }}, ref:{{ matiere.code_fournisseur }}
                    <!-- Ajoutez d'autres éléments en fonction de vos besoins -->
                  </q-item>
                </q-list>
              </q-menu>
            </q-input>
             <q-form>
              <q-dialog v-model="addDialog">
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
                        <q-input
                            v-model="nom"
                            label="Désignation" color="cyan-4" class="hover-effect">
                          <template v-slot:prepend>
                            <q-btn
                                flat color="cyan-4"
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
                      <div class="col-4">
                        <q-input
                            label="Liste"
                            class="hover-effect"
                            color="cyan-4"
                            v-model="tva"
                        >
                          <template v-slot:append>
                            <div class="text-cyan-4 text-subtitle2">%</div>
                          </template>
                        </q-input>
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
                        <q-btn flat label="Annuler" @click="addDialog=false; this.searchCatalogueQuery=''" color="red-4"/>
                      </q-btn-group>
                    </div>
                  </q-card-section>
                </q-card>
              </q-dialog>
             </q-form>
            </div>
          </div>
          <div class="col-6 q-mt-md text-cyan-4 text-h6">
            <div class="row justify-center">
            {{ countMatieres }} matières premières référencées
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
                <q-card bordered class="card-maxi justify-center items-center text-center relative" :class="{ 'bd-red-4': !matiere.stockee}">
                  <div @click="redirectToLink(matiere.id)" class="card-content">
                    <q-img class="logo-card-mini"
                           src="../../assets/img/blanc.jpg"
                           loading="lazy"
                           spinner-color="red-4"
                           :alt="matiere.type.nom">
                      <font-awesome-icon
                          v-if="matiere.type.nom === 'Conditionnement'"
                          icon="fa-solid fa-prescription-bottle"
                          size="3x"
                          class="icon-background"
                      />
                      <font-awesome-icon
                          v-if="matiere.type.nom === 'Principe actif'"
                          icon="fa-solid fa-pills"
                          size="3x"
                          class="icon-background hover-effect"
                      />
                      <font-awesome-icon
                          v-if="matiere.type.nom === 'Cosmétique'"
                          icon="fa-solid fa-hand-holding-droplet"
                          size="3x"
                          class="icon-background"
                      />
                      <font-awesome-icon
                          v-if="matiere.type.nom === 'Complément alimentaire'"
                          icon="fa-solid fa-glass-water-droplet"
                          size="3x"
                          class="icon-background"
                      />
                      <font-awesome-icon
                          v-if="matiere.type.nom === 'Technique'"
                          icon="fa-solid fa-book-medical"
                          size="3x"
                          class="icon-background"
                      />
                      <font-awesome-icon
                          v-if="matiere.type.nom === 'Alimentaire'"
                          icon="fa-solid fa-bottle-droplet"
                          size="3x"
                          class="icon-background"
                      />
                      <font-awesome-icon
                          v-if="matiere.type.nom === 'Excipient'"
                          icon="fa-solid fa-flask"
                          size="3x"
                          class="icon-background"
                      />
                      <div class="absolute-top hover-effect q-my-none" :class="{ 'text-cyan-1': matiere.stockee, 'text-red-4': !matiere.stockee }">
                        <div>{{ matiere.nom }}</div>
                        <div>{{ matiere.forme.nom }} {{ matiere.qté_cdt }}{{ matiere.unite_cdt }}</div>
                        <div>
                          <font-awesome-icon v-if="matiere.qté_stock < matiere.stock_mini"
                                             icon="fa-solid fa-triangle-exclamation"
                                             beat-fade
                                             size="fa-xs"
                                             style="color: #e57373;"
                          />
                          <q-icon name="fact_check" color="orange-4" size="xs" v-if="matiere.cde"/>
                          <q-icon name="fact_check" color="green-4" size="xs" v-if="matiere.attente_livraison"/>
                          Stock : {{ matiere.qté_stock }}{{ matiere.unite_mesure.nom }}
                        </div>
                      </div>
                      <template v-slot:loading>
                        <q-spinner-rings color="red-4" />
                      </template>
                    </q-img>
                    <q-btn flat color="white" class="absolute-top-right hover-effect q-pa-none q-ma-none"
                           icon="more_vert" @click.stop="toggleMenu(matiere.id)"
                    />
                    <q-menu fit anchor="top right" self="bottom middle" v-model="showMenu[matiere.id]">
                      <q-list style="min-width: 100px">
                        <q-item clickable v-close-popup @click.stop="toggleCde({ matiereId: matiere.id, isCde: matiere.cde })">
                          <q-item-section :class="{ 'hover-effect-warning': matiere.cde, 'hover-effect-success': !matiere.cde }">
                            {{ matiere.cde ? 'Retirer de la liste de commande' : 'Ajouter à la liste de commande' }}
                          </q-item-section>
                        </q-item>
                        <q-item clickable v-close-popup @click.stop="toggleActivation({ matiereId: matiere.id, isStockee: matiere.stockee })">
                          <q-item-section class="hover-effect">
                            {{ matiere.stockee ? 'Non Stockée' : 'Stockée' }}
                          </q-item-section>
                        </q-item>
                      </q-list>
                    </q-menu>
                  </div>
                  <div class="absolute-top-left q-ml-sm q-mt-xs">
                    <div v-if="matiere.liste.nom==='Liste 1'" class="text-red-4 text-subtitle2">1</div>
                    <div v-if="matiere.liste.nom==='Liste 2'" class="text-green-4 text-subtitle2">2</div>
                    <div v-if="matiere.liste.nom==='Stupéfiant'" class="text-red-4 text-subtitle2">S</div>
                  </div>
                  <div class="absolute-bottom-left">
                    <div class="row q-mb-xs">
                      <font-awesome-icon v-if="matiere.froid" fade icon="fa-solid fa-snowflake" class="q-ml-xs fa-2x" style="color: #4dd0e1;" />
                      <q-img v-if="matiere.cmr" class="q-ml-xs fade-blink" src="@/assets/img/health_hazard.png" :style="{ width: '20px', height: '20px' }"/>
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
                      class="hover-effect"
                      :color="expanded[matiere.id] ? 'orange-4' : 'cyan-4'"
                      round
                      flat
                      dense
                      icon="info"
                      size="sm"
                      @click.stop="toggleInfo(matiere.id)"
                    />
                  </q-btn-group>

                  <q-menu fit anchor="bottom right" self="top middle" v-model="expanded[matiere.id]">
                    <q-list style="min-width: 100px">
                      <q-item class="justify-center">
                        <q-item-section avatar class="text-cyan-4">
                          Détails
                        </q-item-section>
                      </q-item>
                      <q-item v-if="matiere.fournisseur">
                        <q-item-section avatar class="text-orange-4">
                          Fournisseur :
                        </q-item-section>
                        <q-item-section class="text-grey-7">
                          {{ matiere.fournisseur.name }}
                        </q-item-section>
                      </q-item>
                      <q-item v-if="matiere.tva">
                        <q-item-section avatar class="text-orange-4">
                          TVA :
                        </q-item-section>
                        <q-item-section class="text-grey-7">
                          {{ matiere.tva }}%
                        </q-item-section>
                      </q-item>
                      <q-item v-if="matiere.prix">
                        <q-item-section avatar class="text-orange-4">
                          Prix :
                        </q-item-section>
                        <q-item-section class="text-grey-7">
                          {{ matiere.prix }} € HT - {{ matiere.prix_ttc }} € TTC
                        </q-item-section>
                      </q-item>
                      <q-item v-if="matiere.prix_unit">
                        <q-item-section avatar class="text-orange-4">
                          Prix unitaire :
                        </q-item-section>
                        <q-item-section class="text-grey-7">
                          {{ matiere.prix_unit }} €/{{ matiere.unite_mesure.nom }} HT - {{ matiere.prix_unit_ttc }} €/{{ matiere.unite_mesure.nom }} TTC
                        </q-item-section>
                      </q-item>
                      <q-item v-if="matiere.stock_mini">
                        <q-item-section avatar class="text-orange-4">
                          Stock mini :
                        </q-item-section>
                        <q-item-section class="text-grey-7">
                          {{ matiere.stock_mini }}{{ matiere.unite_mesure.nom }}
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
  <q-page v-else class="row items-center justify-center">
  <div class=" row justify-center">
      <atom-spinner
        class="bg-op-8"
        :animation-duration="1000"
        :size="200"
        :color="'#ff1d5e'"
      />
      </div>
  </q-page>
</template>

<script>
import { mapActions, mapGetters } from 'vuex';
import {AtomSpinner} from 'epic-spinners'
import {FontAwesomeIcon} from "@fortawesome/vue-fontawesome";


export default {
  name: "MatieresCards",
  components: {
    FontAwesomeIcon,
    AtomSpinner,
  },

  data() {
    return {
      searchCatalogueQuery: '',
      searchQuery: '',
      addDialog: false,
      menuMat: false,
      selectedMatiere: null,
      nom: '',
      tva: '',
      stock_mini: '',
      stockee: false,
      cde_auto: false,
      uniteMesure: null,
      liste: null,
      forme: null,
      type: null,
      unitesOptions: [],
    };
  },

  computed: {
    ...mapGetters('matieresPremieres', ['allMatieres', 'allMatieresCatalogue', 'allCategories',
                                        'allUnites','allFormes',
                                        'showMenu', 'expanded']),
    ...mapGetters('formules', ['allListes']),

    countMatieres() {
      return Array.isArray(this.filteredMatieres) ? this.filteredMatieres.length : 0;
    },

    filteredMatieres() {
      if (!Array.isArray(this.allMatieres)) {
        return [];
      }

      const categories = ["Chimiques & Excipients", "Alcools & Alcoolats", "Gélules", "Flaconnage", "Pots"];

      if (this.searchQuery) {
        return this.allMatieres.filter(matiere =>
          matiere.nom.toLowerCase().startsWith(this.searchQuery.toLowerCase()) &&
          categories.includes(matiere.categorie.nom)
        );
      }
      return this.allMatieres.filter(matiere => categories.includes(matiere.categorie.nom));
    },

    filteredMatieresCatalogue() {
      if (this.searchCatalogueQuery) {
        return this.allMatieresCatalogue.filter(matiere =>
            matiere.designation.toLowerCase().startsWith(this.searchCatalogueQuery.toLowerCase())
        );
      }
      return this.allMatieresCatalogue;
    },

    uniteStockNom() {
      if (this.unite_mesure && this.allUnites) {
        const uniteStock = this.allUnites.find(unite => unite.id === this.unite_mesure.id);
        return uniteStock ? uniteStock.nom : '';
      }
      return '';
    },
  },

  async created() {
    await this.loadMatieresPremieres();
    await this.loadMatieresPremieresCatalogue();
    await this.loadCategoriesMatieres();
    await this.loadUnites();
    await this.loadListes();
    await this.loadFormes();
    console.log('allMatieres', this.allMatieres);
    this.unitesOptions = this.allUnites
      .map(unite => ({
      label: unite.nom,
      value: unite.id,
    }));

    this.listesOptions = this.allListes
      .map(liste => ({
      label: liste.nom,
      value: liste.id,
    }));

    this.formesOptions = this.allFormes
      .map(forme => ({
      label: forme.nom,
      value: forme.id,
    }));

  },

  methods: {
    ...mapActions('matieresPremieres', ['loadMatieresPremieres', 'loadCategoriesMatieres',
                                        'loadMatieresPremieresCatalogue', 'deleteMatiere',
                                        'loadUnites','loadFormes', 'addMatiere',
                                        'toggleActivation', 'toggleMenuMat', 'toggleCde', 'toggleMenu', 'toggleInfo']),
    ...mapActions('formules', ['loadListes']),

    selectMatiere(matiere) {
      this.searchCatalogueQuery = matiere.designation;
      this.selectedMatiere = { ...matiere };
      this.menuMat=false;
      this.addDialog=true;
    },

    async transfert() {
      const formData = {
        nom: this.nom,
        type: this.selectedMatiere.type.id,
        qté_cdt: this.selectedMatiere.qté,
        unite_mesure: this.uniteMesure.value,
        fournisseur: this.selectedMatiere.fournisseur.id,
        prix: this.selectedMatiere.prix,
        tva: this.tva,
        stock_mini: this.stock_mini,
        qté_stock: 0,
        cdt: 1,
        froid: this.selectedMatiere.froid,
        cmr: this.selectedMatiere.cmr,
        liste: this.liste.value,
        forme: this.forme.value,
        stockee: this.stockee,
        ean: this.selectedMatiere.cip,
        code_fournisseur: this.selectedMatiere.code_fournisseur,
        unite_cdt : this.selectedMatiere.unite,
      };
      this.addMatiere(formData);
      await this.loadMatieresPremieres();
      this.selectedMatiere = null;
      this.searchCatalogueQuery = '';
      this.nom = '';
      this.stock_mini = '';
      this.tva = '';
      this.stockee = false;
      this.cde_auto = false;
      this.uniteMesure = null;
      this.liste = null;
      this.forme = null;
      this.type = null;
      this.addDialog=false;
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



