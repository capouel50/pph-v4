<template>
  <q-page v-if="loadedPage">

    <div class="row justify-center">
      <div class="col-md-8">

        <div class="row q-mt-md">
          <div class="col-6 text-h6 text-center text-cyan-4">
            Matières premières
          </div>
          <div class="col-6 text-h6 text-center text-cyan-4">
            Préparations
          </div>
        </div>

        <div class="row justify-center">
          <div class="col-2 card-home q-ml-sm q-mt-sm">
            <q-card bordered>
              <q-img
                  src="../assets/img/commande.jpg"
                  loading="lazy"
                  spinner-color="red-4"
              >
                <div class="absolute-top text-subtitle2 text-center hover-effect">
                  En attente commande
                  <div class="text-h5 text-center text-cyan-4">
                  {{ matieresCdeCount }}
                  </div>
                </div>
                <template v-slot:loading>
                  <q-spinner-rings color="red-4" />
                </template>
              </q-img>
              <q-btn-group class="absolute-bottom-right q-pa-none q-ma-none">
                <router-link to="/commande/">
                  <q-btn
                       class="q-pa-none hover-effect"
                       flat
                       color="cyan-4"
                       icon="visibility"
                    />
                </router-link>
                <q-btn
                    class="q-pa-none hover-effect"
                    flat
                    color="cyan-4"
                    icon="print"
                />
                <q-btn
                    class="q-pa-none hover-effect"
                    flat
                    color="green-4"
                    icon="check_circle"
                    @click="validateCommande"
                />
              </q-btn-group>
            </q-card>
          </div>

          <div class="col-2 card-home offset-1 q-mt-sm">
            <q-card bordered>
              <q-img
                  src="../assets/img/livrer.jpg"
                  loading="lazy"
                  spinner-color="red-4"
              >
                <div class="absolute-top text-subtitle2 text-center hover-effect">
                  En attente livraison
                  <div class="text-h5 text-center text-cyan-4">
                    {{ matieresLivraisonCount }}
                  </div>
                </div>
                <template v-slot:loading>
                  <q-spinner-rings color="red-4" />
                </template>
              </q-img>
              <q-btn-group class="absolute-bottom-right q-pa-none q-ma-none">
                <router-link to="/reception/" >
                  <q-btn
                       class="q-pa-none hover-effect"
                       flat
                       color="cyan-4"
                       icon="visibility"
                    />
                </router-link>
              </q-btn-group>
            </q-card>
          </div>

          <div class="col-2 card-home offset-1 q-mt-sm">
            <q-card bordered>
              <q-img
                  src="../assets/img/demande3.jpg"
                  loading="lazy"
                  spinner-color="red-4"
              >
                <div class="absolute-top text-subtitle2 text-center hover-effect">
                  En attente préparation
                  <div class="text-h5 text-center text-cyan-4">
                    {{ nombreDemandes }}
                  </div>
                  <div class="text-subtitle2 text-center">
                    {{ nombreDemandesProche }} pour le <br>
                    {{ demandeProche.dateFormatee }}
                  </div>
                </div>
                <template v-slot:loading>
                  <q-spinner-rings color="red-4" />
                </template>
              </q-img>
              <q-btn-group class="absolute-bottom-right q-pa-none q-ma-none">
                    <q-btn
                       class="q-pa-none hover-effect"
                       flat
                       color="cyan-4"
                       icon="calendar_month"
                       @click="openCalendar"
                    />
              </q-btn-group>
              <q-dialog v-model="calendarDialog">
                <q-card>
                  <q-toolbar>
                    <q-btn
                        flat
                        class="text-cyan-4 hover-effect"
                        label="Nouvelle demande"
                  />
                    <q-btn
                        flat
                        class="text-cyan-4 hover-effect"
                        label="Toutes les demandes"
                  />
                  <q-btn
                        flat
                        class="text-cyan-4 hover-effect absolute-right"
                        icon="close"
                        @click="calendarDialog = false"
                  />
                  </q-toolbar>
                    <q-splitter v-model="splitterModel">
                      <template v-slot:before>
                        <div class="q-ma-md">
                          <q-date
                            v-model="dateCalendar"
                            :events="formatDemandesDates"
                            event-color="orange"
                            color="cyan-4"
                          />
                        </div>
                      </template>

                    <template v-slot:after>
                      <div class="q-pa-md">
                        <div class="text-h6 text-center text-orange-4">Demandes en cours</div>
                        <q-scroll-area
                          :thumb-style="thumbStyle"
                          :bar-style="barStyle"
                          style="height: 310px; max-width: 300px;"
                        >
                        <div v-if="Object.keys(demandesGroupesParType).length">
                          <div v-for="(demandes, type) in demandesGroupesParType" :key="type">
                            <q-separator/>
                            <div class="text-subtitle1 text-center text-cyan-4">{{ type }}</div>
                              <div v-for="(demande, index) in demandes" :key="index">
                                <div class="text-bold">
                                {{ demande.qté }} {{ demande.prep.nom }}<br/>
                                 </div>
                                {{ demande.service.nom }}
                                <div class="text-italic">{{ demande.commentaire }}</div>
                                <div class="row justify-center">
                                  <q-btn
                                        size="xs"
                                        flat
                                        class="text-cyan-4 hover-effect"
                                        icon="visibility"
                                  />
                                  <q-btn
                                        flat
                                        size="xs"
                                        icon="local_pharmacy"
                                        color="green-4"
                                  />
                                  <q-btn
                                        flat
                                        size="xs"
                                        icon="delete_forever"
                                        color="red-4"
                                  />
                                </div>
                                <br/>
                              </div>
                          </div>
                        </div>
                        <div v-else>
                          <p>Aucune demande pour cette date.</p>
                        </div>
                        </q-scroll-area>
                      </div>
                    </template>
                  </q-splitter>
                </q-card>
              </q-dialog>
            </q-card>
          </div>

          <div class="col-2 card-home offset-1 q-mt-sm">
            <q-card bordered>
              <q-img
                  src="../assets/img/controle2.jpg"
                  loading="lazy"
                  spinner-color="red-4"
              >
                <div class="absolute-top text-subtitle2 text-center hover-effect">
                  En attente contrôle
                  <div class="text-h5 text-center text-cyan-4">
                    {{ fichesControlCount }}
                  </div>
                </div>
                <template v-slot:loading>
                  <q-spinner-rings color="red-4" />
                </template>
              </q-img>
            </q-card>
          </div>
        </div>
      </div>
    </div>

    <div class="row justify-center q-mx-md q-pb-lg q-mt-lg bd-radius-10 bg-op-8" style="background-color:#1a2946;">
      <div class="col-12 text-center">
          <div class="text-h6 text-cyan-4">Tableau de bord</div>
        </div>
      <div class="col-md-5">
        <q-carousel
            animated
            v-model="carousel1"
            arrows
            infinite
            :autoplay="autoplay1"
            @mouseenter="autoplay1 = false"
            @mouseleave="autoplay1 = true"
            class="rounded-borders q-pb-sm"
            style="background-image: linear-gradient(to left, #263238, #3F6B79);"
          >
            <q-carousel-slide name="slide1">
              <q-scroll-area
                  :thumb-style="thumbStyle"
                  :bar-style="barStyle"
                  style="height: 350px;"
              >
              <q-card class="items-center" style="background-image: linear-gradient(to left, #263238, #3F6B79);">
                <q-card-section>
                  <q-card-section>
                    <div class="text-center text-cyan-1">Produits arrivant à expiration en {{ currentYear }}</div>
                  <q-list class="text-cyan-1">
                    <q-item v-for="(reception, index) in filteredMatieresExpire" :key="index" clickable v-ripple>
                      <q-item-section class="hover-effect">
                        <q-item-label class="text-cyan-1 text-no-wrap">{{ reception.matiere.nom }} {{ reception.matiere.qté_cdt }}{{ reception.matiere.unite_cdt }}</q-item-label>
                        <q-item-label class="text-cyan-1 text-subtitle2 text-no-wrap" caption>{{ reception.matiere.fournisseur.name }} {{ reception.lot }} {{ reception.peremption }}</q-item-label>
                      </q-item-section>
                      <q-item-section class="q-mr-md" top>
                        <div class="row justify-center">
                          <q-item-section>
                            <font-awesome-icon v-if="reception.matiere.froid" fade icon="fa-solid fa-snowflake" class="fa-2x" style="color: #4dd0e1;" />
                          </q-item-section>
                          <q-item-section>
                            <q-img v-if="reception.matiere.cmr" class="fade-blink" src="@/assets/img/health_hazard.png" :style="{ width: '30px', height: '30px' }"/>
                          </q-item-section>
                        </div>
                      </q-item-section>
                      <q-item-section side top>
                        <q-badge color="cyan-4"
                                 text-color="white">
                          {{ reception.stock_reception }}{{ reception.matiere.unite_mesure.nom }}<br/>{{ reception.matiere.qté_stock }}{{ reception.matiere.unite_mesure.nom }}
                        </q-badge>
                      </q-item-section>
                    </q-item>
                  </q-list>
              </q-card-section>
              </q-card-section>
              </q-card>
              </q-scroll-area>
            </q-carousel-slide>

            <q-carousel-slide name="slide2">
              <q-scroll-area
                  :thumb-style="thumbStyle"
                  :bar-style="barStyle"
                  style="height: 350px;"
              >
              <q-card class="items-center" style="background-image: linear-gradient(to left, #263238, #3F6B79);">
                <q-card-section>
                  <q-card-section>
                    <div class="text-center text-cyan-1">Produits en attente de commande</div>
                  <q-list class="text-cyan-1">
                    <q-item v-for="(matiere, index) in filteredMatieresCde" :key="index" clickable v-ripple>
                      <q-item-section class="hover-effect">
                        <q-item-label class="text-cyan-1 text-no-wrap">{{ matiere.nom }} {{ matiere.qté_cdt }}{{ matiere.unite_cdt }}</q-item-label>
                        <q-item-label class="text-cyan-1 text-subtitle2 text-no-wrap" caption>{{ matiere.fournisseur.name }} {{ matiere.code_fournisseur }}</q-item-label>
                      </q-item-section>
                      <q-item-section class="q-mr-md" top>
                        <div class="row justify-center">
                          <q-item-section>
                            <font-awesome-icon v-if="matiere.froid" fade icon="fa-solid fa-snowflake" class="fa-2x" style="color: #4dd0e1;" />
                          </q-item-section>
                          <q-item-section>
                            <q-img v-if="matiere.cmr" class="fade-blink" src="@/assets/img/health_hazard.png" :style="{ width: '30px', height: '30px' }"/>
                          </q-item-section>
                        </div>
                      </q-item-section>
                      <q-item-section side top>
                        <q-badge :color="matiere.qté_stock < matiere.stock_mini ? 'red' : 'green'"
                                 text-color="white">
                          {{ matiere.qté_stock }}{{ matiere.unite_mesure.nom }}
                        </q-badge>
                      </q-item-section>
                    </q-item>
                  </q-list>
              </q-card-section>
              </q-card-section>
              </q-card>
              </q-scroll-area>
            </q-carousel-slide>

            <q-carousel-slide name="slide3">
              <q-scroll-area
                  :thumb-style="thumbStyle"
                  :bar-style="barStyle"
                  style="height: 350px;"
              >
              <q-card class="items-center" style="background-image: linear-gradient(to left, #263238, #3F6B79);">
                <q-card-section>
                  <q-card-section>
                    <div class="text-center text-cyan-1">Produits en attente de livraison</div>
                  <q-list class="text-cyan-1">
                    <q-item v-for="(matiere, index) in filteredMatieresLivraison" :key="index" clickable v-ripple>
                      <q-item-section class="hover-effect">
                        <q-item-label class="text-cyan-1 text-no-wrap">{{ matiere.nom }} {{ matiere.qté_cdt }}{{ matiere.unite_cdt }}</q-item-label>
                        <q-item-label class="text-cyan-1 text-subtitle2 text-no-wrap" caption>{{ matiere.fournisseur.name }} {{ matiere.code_fournisseur }}</q-item-label>
                      </q-item-section>
                      <q-item-section class="q-mr-md" top>
                        <div class="row justify-center">
                          <q-item-section>
                            <font-awesome-icon v-if="matiere.froid" fade icon="fa-solid fa-snowflake" class="fa-2x" style="color: #4dd0e1;" />
                          </q-item-section>
                          <q-item-section>
                            <q-img v-if="matiere.cmr" class="fade-blink" src="@/assets/img/health_hazard.png" :style="{ width: '30px', height: '30px' }"/>
                          </q-item-section>
                        </div>
                      </q-item-section>
                      <q-item-section side top>
                        <q-badge :color="matiere.qté_stock < matiere.stock_mini ? 'red' : 'green'"
                                 text-color="white">
                          {{ matiere.qté_stock }}{{ matiere.unite_mesure.nom }}
                        </q-badge>
                      </q-item-section>
                    </q-item>
                  </q-list>
              </q-card-section>
              </q-card-section>
              </q-card>
              </q-scroll-area>
            </q-carousel-slide>

          </q-carousel>
      </div>
      <div class="col-md-5 offset-1">
        <q-carousel
            animated
            v-model="carousel2"
            arrows
            infinite
            :padding="padding"
            :autoplay="autoplay2"
            class="rounded-borders"
            @mouseenter="autoplay2 = false"
            @mouseleave="autoplay2 = true"
            style="background-image: linear-gradient(to right, #263238, #3F6B79);"
          >
            <!-- Carousel Slide 1 -->
            <q-carousel-slide name="slide2-1">
              <q-card class="text-subtitle2 text-center text-cyan-1" style="background-image: linear-gradient(to right, #263238, #3F6B79);">
                <q-card-section v-if="loadedBar">
                    <q-toggle
                       v-model="toggleMonth"
                       color="red-4"
                       icon="calendar_month"
                       label="Semaines/Mois"
                       size="md"
                    />
                    <q-toggle
                       v-model="toggleType"
                       color="purple-4"
                       icon="bar_chart"
                       label="Bar/Area"
                       size="md"
                    />
                    <q-toggle
                       v-model="toggleValue"
                       color="green-4"
                       icon="timeline"
                       label="Valeurs"
                       size="md"
                    />
                    <apexchart :key="graphKey" id="apex-bar" height="200" :type="toggleType ? 'area' : 'bar'" :options="chartOptions" :series="series"></apexchart>
                </q-card-section>
              </q-card>
            </q-carousel-slide>
            <!-- Carousel Slide 2 -->
            <q-carousel-slide name="slide2-2">
              <q-card class="items-center" style="background-image: linear-gradient(to right, #263238, #3F6B79);">
                <q-card-section>
                  <q-card-section>
                    <div class="text-center text-cyan-1">Evolution des 5 formules les plus utilisées en {{ currentYear }}</div>
                  <q-list class="text-cyan-1">
                    <q-item v-for="(fiche, index) in topFichesData" :key="index" clickable v-ripple>
                      <q-item-section class="hover-effect">
                        <q-item-label>{{ fiche.prep }}</q-item-label>
                        <q-item-label class="text-cyan-1 text-subtitle2" caption>{{ previousYear }}: {{ fiche.previousCount }} fiches - {{ currentYear }}: {{ fiche.count }} fiches</q-item-label>
                      </q-item-section>
                      <q-item-section side top>
                        <q-badge :color="calculateEvolution(fiche.count, fiche.previousCount) < 0 ? 'red' : 'green'"
                                 text-color="white">
                          {{ calculateEvolution(fiche.count, fiche.previousCount) }}%
                        </q-badge>
                      </q-item-section>
                    </q-item>
                  </q-list>
              </q-card-section>
              </q-card-section>
              </q-card>
            </q-carousel-slide>
            <!-- Carousel Slide 3 -->
            <q-carousel-slide name="slide2-3">
              <q-card class="items-center" style="background-image: linear-gradient(to right, #263238, #3F6B79);">
                <q-card-section class="text-subtitle2 text-center text-cyan-1">
                  <q-card-section v-if="loadedDonut">
                    <div>Répartition des fiches en {{ currentYear }}</div>
                    <apexchart :options="donutOptions" :series="donutSeries" type="donut" height="200"></apexchart>
                  </q-card-section>
                </q-card-section>
              </q-card>
            </q-carousel-slide>
          </q-carousel>
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
import api from '../../api';
import VueApexCharts from "vue3-apexcharts";
import {AtomSpinner} from 'epic-spinners'

export default {
  name: 'HomePage',
  components: {
    apexchart: VueApexCharts,
    AtomSpinner
  },

  data() {
    return {
      thumbStyle: {
        right: '4px',
        borderRadius: '5px',
        backgroundColor: '#027be3',
        width: '5px',
        opacity: 0.75
      },

      barStyle: {
        right: '2px',
        borderRadius: '9px',
        backgroundColor: '#027be3',
        width: '9px',
        opacity: 0.2
      },
      carousel1: 'slide1',
      carousel2: 'slide2-1',
      autoplay1: true,
      autoplay2: true,
      padding: false,
      loadedPage: false,
      calendarDialog: false,
      dateCalendar: new Date().toISOString().substr(0, 10).replace(/-/g, '/'),
      splitterModel: 62,
      currentYear: new Date().getFullYear(),
      previousYear: new Date().getFullYear() - 1,
      loadedBar: false,
      toggleMonth: true,
      loadedDonut: false,
      loadedTopFiches: false,
      topFichesData: null,
      tickAmountX: 2,
      toggleType: true,
      toggleValue: false,
      graphKey: 0,
      donutSeries: [],
      donutOptions: [],
      series: [],
      chartOptions: [],
    };

  },

  computed: {
    ...mapGetters('matieresPremieres', ['allMatieres', 'allReceptions', 'matieresCdeCount', 'matieresLivraisonCount']),
    ...mapGetters('demandes', ['nombreDemandes', 'demandeProche', 'nombreDemandesProche', 'demandesDates', 'demandesAll']),
    ...mapGetters('fiches', ['fichesControlCount', 'fichesSemaine']),

    filteredMatieresExpire() {
      const today = new Date(); // Date d'aujourd'hui
      const endOfYear = new Date(today.getFullYear(), 11, 31); // Date du 31 décembre de l'année en cours
      return this.allReceptions.filter(reception => {
        // Parse la date de péremption dans le format jj/mm/aaaa
        const [day, month, year] = reception.peremption.split('/'); // Supposant que la date est au format jj/mm/aaaa
        const peremptionDate = new Date(`${year}-${month}-${day}`); // Crée un objet Date avec le bon format
        return peremptionDate >= today && peremptionDate <= endOfYear; // Vérifie si la date de péremption est comprise entre aujourd'hui et le 31 décembre de l'année en cours
      });
    },

    filteredMatieresCde() {
      return this.allMatieres.filter(matiere => matiere.cde === true);
    },

    filteredMatieresLivraison() {
      return this.allMatieres.filter(matiere => matiere.attente_livraison === true);
    },

    demandesDates() {
      const data = this.$store.getters['demandes/demandesDates'];
      return data;
    },

    demandesGroupesParType() {
      let groupes = {};

      this.demandesDatesSelect.forEach(demande => {
        let type = demande.prep.type.nom;

        if (!groupes[type]) {
          groupes[type] = [];
        }

        groupes[type].push(demande);
      });

      return groupes;
    },

    demandesDatesSelect() {
    let dateSelectionneeFormatee = this.dateCalendar.replace(/\//g, '-');
    console.log('Date formatée pour comparaison:', dateSelectionneeFormatee);

    let demandesFiltrees = this.demandesAll.filter(demande => {
      console.log('Comparaison de dates:', demande.date_prevu, dateSelectionneeFormatee);
      return demande.date_prevu === dateSelectionneeFormatee;
    });

    console.log('Demandes filtrées:', demandesFiltrees);
    return demandesFiltrees;
  },

    formatDemandesDates() {
      return this.demandesDates.map(date => date.replace(/-/g, '/'));
    },

    totalFiches() {
      return this.donutSeries.reduce((acc, value) => acc + value, 0);
    },

  },

  async mounted() {
    try {
      await this.loadAllData();
    } catch (e) {
      console.error('Erreur lors du chargement des données :', e);
    } finally {
        setTimeout(() => {
        this.$nextTick(() => {
          this.loadedPage = true;
        });
      }, 1000);
    }
  },

  watch: {
    toggleMonth() {
      this.loadData();
      this.processData();
    },

    dateCalendar(newVal, oldVal) {
      console.log('Ancienne date:', oldVal, 'Nouvelle date:', newVal);
    },

    toggleType() {
      this.graphKey++; // cela change la clé, forçant le rechargement du composant graphique
    },

    toggleValue(newValue) {
      this.chartOptions = {
        ...this.chartOptions,
        dataLabels: {
          enabled: newValue
        }
      };
      this.graphKey++;
    },

  },

  methods: {
    ...mapActions('matieresPremieres', ['loadMatieresPremieres', 'loadReceptions']),
    ...mapActions('demandes', ['loadDemandes']),
    ...mapActions('fiches', ['loadFiches']),

  async loadAllData() {
    await this.loadMatieresPremieres();
    await this.loadDemandes();
    await this.loadFiches();
    await this.loadReceptions();
    await this.loadData();
    await this.loadTopFichesData();
    await this.loadDonutData();
    console.log('receptions : ', this.allReceptions)
  },

  async loadData() {
    try {
      const url = this.toggleMonth ? 'fiches-mois' : 'fiches-semaine';
      const response = await api.get(`/PPH/${url}`);
      // Passez le contexte comme un paramètre booléen
      this.processData(response.data, this.toggleMonth);
      this.loadedBar = true;
    } catch (error) {
      console.error('Erreur lors du chargement des données de l\'API:', error);
      this.loadedBar = false; // Assurez-vous de mettre à jour l'état en cas d'erreur
    }
  },

  processData(data) {
    // Configuration des catégories sur l'axe X en fonction des données reçues
    const xAxisTitleText = this.toggleMonth ? "Mois" : "Semaine";

    // Mise à jour des données de série
    const seriesData = [
      {
        name: "Fiches",
        data: data.map(item => item.count),
        color: '#4dd0e1', // Couleur spécifique pour cette série
      },
      {
        name: "Unités de conditionnement",
        data: data.map(item => item.qte),
        color: '#ffb74d', // Couleur spécifique pour cette série
      },
    ];

    // Mise à jour des options du graphique
    this.chartOptions = {
      chart: {
        id: "barChart",
        toolbar: {
          show: true,
          tools: {
            zoom: true,
            zoomin: true,
            zoomout: true,
            pan: true,
            reset: true,
          },
          autoSelected: 'zoom'
        },  // Par défaut, l'outil sélectionné est le zoom
      },
      tooltip: {
        theme: 'dark',
        // Autres configurations des tooltips...
      },
      dataLabels: {
        enabled: this.toggleValue // Active ou désactive les dataLabels basé sur toggleValue
      },
      xaxis: {
        labels: {
          style: {
            colors:"#e0f7fa"
          },
        },
        tickAmount: this.tickAmountX,
        title: {
          text: xAxisTitleText,
          style: {
            color: "#e0f7fa" // Couleur pour le titre de l'axe Y
          },
        },
      },
      yaxis: {
        labels: {
          style: {
            colors:["#e0f7fa"]
          }
        },
        title: {
          text: "Quantité",
          style: {
            color: "#e0f7fa" // Couleur pour le titre de l'axe Y
          },
        },
        axisBorder: {
          show: true,
          color: "#e0f7fa"
        }
      },
      grid: {
        xaxis: {
          lines: {
            show: false
          }
        },
        yaxis: {
          lines: {
            show: false,
          }
        }
      },
      legend: {
        position: 'top', // Position de la légende
        horizontalAlign: 'left',
        labels: {
          colors: '#e0f7fa', // Couleur du texte de la légende
          useSeriesColors: false
        }
      },
      plotOptions: {
        bar: {
          borderRadius: 2,
          columnWidth: '80%',
          borderRadiusApplication: 'end',
          backgroundBarOpacity: 0.8,
          fill:{
            type: "gradient",
            gradient:{
              shade: "light",
              type: "vertical",
              shadeIntensity: 0,
              gradientToColors: ['#ffb74d'],
              inverseColors: true,
              opacityFrom: 1,
              opacityTo: 0.6,
            }
          }
        }
      },
    };
    // Mise à jour de l'objet series du composant
    this.series = seriesData;
  },

  async loadDonutData() {
    try {
      const response = await api.get('/PPH/fiches/count_per_service');
      const donutData = this.DonutData(response.data);
      this.donutSeries = donutData.series;
      this.donutOptions = donutData.options; // Assurez-vous d'ajuster cette ligne en fonction de votre structure de données
      this.loadedDonut = true;
      console.log(this.donutSeries);
      console.log(this.donutOptions);
    } catch (e) {
      console.error('Erreur lors du chargement des données du donut :', e);
      this.loadedDonut = false;
    }
  },

  DonutData(data) {
    function getRandomColor() {
      const letters = '0123456789ABCDEF';
      let color = '#';
      for (let i = 0; i < 6; i++) {
        color += letters[Math.floor(Math.random() * 16)];
      }
      return color;
    }

    const colors = data.map(() => getRandomColor());

    return {
      series: data.map(c => c.count),
      options: {
        labels: data.map(s => s.service),
        colors: colors, // Vos couleurs générées
        plotOptions: {
          pie: {
            donut: {
              labels: {
                show: true,
                value: {
                  color: '#e0f7fa',
                },
                total: {
                  show: true,
                  label: 'Total',
                  formatter: () => this.totalFiches,
                  color: '#e0f7fa',
                }
              }
            }
          }
        },
        stroke: {
          width: 0
        },
        legend: {
          position: 'left',
          labels: {
            colors: "#e0f7fa",
          },
        },
        fill: {
          colors: colors
        }
      }
    };
  },

  async loadTopFichesData() {
    try {
      const response = await api.get('/PPH/fiches/top_fiches_annuelles');
      this.topFichesData = this.formatTopFichesData(response.data);
      this.loadedTopFiches = true;
    } catch (e) {
      console.error('Erreur lors du chargement des données des top fiches :', e);
      this.loadedTopFiches = false;
    }
  },

  formatTopFichesData(data) {
    const currentYearData = data.current_year.map(fiche => ({
      prep: fiche.prep__nom,
      count: fiche.count,
      previousCount: data.previous_year[fiche.prep__nom]?.count || 0
    }));

    return currentYearData;
  },

  calculateEvolution(current, previous) {
    if (previous === 0) {
      return current === 0 ? 0 : 100; // Gérer le cas où previous est 0
    }
    return (((current - previous) / previous) * 100).toFixed(2); // Arrondir à 2 décimales
  },

  getEvolutionClass(current, previous) {
    const evolution = this.calculateEvolution(current, previous);
    return evolution > 0 ? 'positive' : 'negative';
  },

  openCalendar() {
    this.calendarDialog = true;
  },

  },
};
</script>

<style>
.apexcharts-tooltip {
    background: #f3f3f3;
    color: orange;
  }
.scroll-container {
    max-height: 300px; /* ou toute autre valeur selon vos besoins */
    overflow-y: auto;
}
/* Définir l'animation keyframes */
@keyframes spin {
    from {
        transform: rotate(0deg);
    }
    to {
        transform: rotate(360deg);
    }
}

/* Appliquer l'animation au spinner */
.atom-spinner {
    animation: spin 10s linear infinite;
}

</style>


