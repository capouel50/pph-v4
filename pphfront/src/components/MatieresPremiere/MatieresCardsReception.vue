<template>
  <q-page v-if="loadMatieresPremieres">
    <div class="row justify-center">
      <div class="col-md-12">
        <div class="row q-mx-sm q-mt-sm">
          <div class="col-6 offset-3 q-mt-md text-cyan-4 text-h6">
            <div class="row justify-center">
            {{ countMatieres }} matières premières en attente de livraison
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
              <div class="col-2 q-pa-sm" v-for="matiere in filteredMatieres" :key="matiere.id">
                <q-card bordered class="card-maxi justify-center items-center text-center relative" :class="{ 'bd-red-4': !matiere.stockee}">
                  <div>
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
                        <q-item clickable v-close-popup @click.stop="toggleLivraison({ matiereId: matiere.id, isLivraison: matiere.attente_livraison })">
                          <q-item-section class="hover-effect-warning">Annuler commande</q-item-section>
                        </q-item>
                        <q-item clickable v-close-popup @click.stop="selectMatiere(matiere)">
                          <q-item-section class="hover-effect-success">
                            Réceptionner
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
                  <q-form>
                    <q-dialog v-model="addMatiereStock">
                    <q-card>

                      <q-card-section>
                        <div class="row justify-center text-h6 text-cyan-4">
                          Réceptionner
                        </div><br/>
                        <div class="row justify-center text-subtitle1 text-orange-4">
                        {{ selectedMatiere.nom }}
                          {{ selectedMatiere.qté_cdt }}{{ selectedMatiere.unite_cdt }} {{ selectedMatiere.fournisseur.name }} ref:{{ selectedMatiere.code_fournisseur }}
                        </div><br/>
                        <div class="row justify-center text-h6 text-cyan-4">
                          dans le stock du préparatoire
                        </div>
                      </q-card-section>

                      <q-separator/>

                      <q-card-section>
                        <div class="row">
                          <div class="col-4">
                            <q-input v-model="qte"
                                     label="Quantité" color="cyan-4" class="hover-effect">

                            </q-input>
                          </div>
                        </div>
                        <div class="row">
                          <div class="col-5">
                            <q-input
                              label="Lot"
                              class="hover-effect"
                              color="cyan-4"
                              v-model="lot"
                            />
                          </div>
                          <div class="col-5 offset-1">
                            <q-input
                              label="Peremption"
                              type="date"
                              hint="Native date"
                              class="hover-effect"
                              color="cyan-4"
                              v-model="peremption"
                            />
                          </div>
                        </div>
                        <div class="row">
                          <div class="col-12">
                            <q-file
                              label="Sélectionner un certificat(pdf)"
                              accept=".pdf"
                              v-model="certificat"
                            />
                          </div>
                        </div>
                      </q-card-section>

                      <q-separator/>

                      <q-card-section>
                        <div class="row justify-center">
                        <q-btn-group>
                          <q-btn flat label="Réceptionner" @click="receptionner" color="green-4"/>
                          <q-btn flat label="Annuler" @click="addMatiereStock=false" color="red-4"/>
                        </q-btn-group>
                          </div>
                      </q-card-section>

                    </q-card>
                  </q-dialog>
                  </q-form>

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
                      <q-item v-if="matiere.code_fournisseur">
                        <q-item-section avatar class="text-orange-4">
                          Ref :
                        </q-item-section>
                        <q-item-section class="text-grey-7">
                          {{ matiere.code_fournisseur }}
                        </q-item-section>
                      </q-item>
                      <q-item v-if="matiere.ean">
                        <q-item-section avatar class="text-orange-4">
                          EAN/CIP :
                        </q-item-section>
                        <q-item-section class="text-grey-7">
                          {{ matiere.ean }}
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
      searchQuery: '',
      addMatiereStock: false,
      selectedMatiere: null,
      qte: '',
      lot: '',
      peremption: '',
      certificat:'',
    };
  },

  computed: {
    ...mapGetters('matieresPremieres', ['allMatieres', 'expanded', 'showMenu']),

    countMatieres() {
      return this.filteredMatieresLivraison.length;
    },

    filteredMatieresLivraison() {
      return this.allMatieres.filter(matiere => matiere.attente_livraison === true);
    },

    filteredMatieres() {
      if (this.searchQuery) {
        return this.filteredMatieresLivraison.filter(matiere =>
            matiere.nom.toLowerCase().startsWith(this.searchQuery.toLowerCase())
        );
      }
      return this.filteredMatieresLivraison;
    },

  },

  async created() {
    await this.loadMatieresPremieres();

  },

  methods: {
    ...mapActions('matieresPremieres', ['loadMatieresPremieres', 'addReception', 'toggleLivraison', 'toggleInfo', 'toggleMenu']),

    selectMatiere(matiere) {
      this.selectedMatiere = { ...matiere };
      this.addMatiereStock=true;
    },

    async receptionner() {
      const formData = {
        matiere: this.selectedMatiere.id,
        qte: this.qte,
        lot: this.lot,
        peremption: this.peremption,
        certificat: this.certificat,
      };
      console.log('formData', formData);
      // Appelez votre action Vuex pour ajouter les compositions
      await this.addReception(formData);
      await this.loadMatieresPremieres();
      this.selectedMatiere = null;
      this.qte = '';
      this.lot = '';
      this.peremption = '';
      this.certificat = '';
      this.addMatiereStock=false;
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

  }
};
</script>



