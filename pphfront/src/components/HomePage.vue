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
              <q-img src="../assets/img/commande.jpg">
                <div class="absolute-top text-subtitle2 text-center hover-effect">
                  En attente commande
                  <div class="text-h5 text-center text-cyan-4">
                  {{ matieresCdeCount }}
                  </div>
                </div>
              </q-img>
            </q-card>
          </div>

          <div class="col-2 card-home offset-1 q-mt-sm">
            <q-card bordered>
              <q-img src="../assets/img/livrer.jpg">
                <div class="absolute-top text-subtitle2 text-center hover-effect">
                  En attente livraison
                  <div class="text-h5 text-center text-cyan-4">
                    {{ matieresLivraisonCount }}
                  </div>
                </div>
              </q-img>
            </q-card>
          </div>

          <div class="col-2 card-home offset-1 q-mt-sm">
            <q-card bordered>
              <q-img src="../assets/img/demande3.jpg">
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
              <q-img src="../assets/img/controle2.jpg">
                <div class="absolute-top text-subtitle2 text-center hover-effect">
                  En attente contrôle
                  <div class="text-h5 text-center text-cyan-4">
                    {{ fichesControlCount }}
                  </div>
                </div>
              </q-img>
            </q-card>
          </div>
        </div>
      </div>
    </div>

       <div class="row q-mx-md q-pb-lg q-mt-lg bd-radius-10 bg-op-8" style="background-color:#1a2946;">
         <div class="col-12 text-center">
           <div class="text-h6 text-cyan-4">Tableau de bord</div>
         </div>
        <div class="row justify-evenly">
        <q-card class="q-col-3 q-mx-sm items-center text-subtitle2 text-center text-cyan-1"
                style="background-image: linear-gradient(to right, #263238, #3F6B79);">
            <q-card-section v-if="loadedBar">
                <q-toggle
                   v-model="toggleMonth"
                   color="red-4"
                   icon="bar_chart"
                   label="semaines - mois année "
                   size="md"
                /> {{ currentYear }}
                <apexchart id="apex-bar" height="200" type="bar" :options="chartOptions" :series="series"></apexchart>
            </q-card-section>
        </q-card>
        <q-card class="q-col-3 items-center" style="background-image: linear-gradient(to right, #3F6B79, #263238);">
          <q-card-section>
            <q-card-section>
            <table v-if="loadedTopFiches" class="table-style" >
              <thead>
                <tr>
                  <th class="text-cyan-1 text-center">Préparation</th>
                  <th class="text-cyan-1 text-center">{{ currentYear }}</th>
                  <th class="text-cyan-1 text-center">{{ previousYear }}</th>
                  <th class="text-cyan-1 text-center">Evolution</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(fiche, index) in topFichesData" :key="index">
                  <td class="text-cyan-4">{{ fiche.prep }}</td>
                  <td class="text-cyan-4 text-center">{{ fiche.count }}</td>
                  <td class="text-cyan-4 text-center">{{ fiche.previousCount }}</td>
                  <td class="text-center" :class="getEvolutionClass(fiche.count, fiche.previousCount)">
                    {{ calculateEvolution(fiche.count, fiche.previousCount) }}%
                  </td>
                </tr>
              </tbody>
            </table>
        </q-card-section>
        </q-card-section>
        </q-card>
        <q-card class="q-col-3 q-mx-sm items-center" style="background-image: linear-gradient(to right, #263238, #3F6B79);">
          <q-card-section class="text-subtitle2 text-center text-cyan-1">
            <q-card-section v-if="loadedDonut">
              <div>Répartition des fiches</div>
              <Doughnut :data="donutData" style="height: 200px"/>
            </q-card-section>
          </q-card-section>
        </q-card>
        <q-card class="q-col-3 q-mr-sm items-center" style="background-image: linear-gradient(to left, #263238, #3F6B79);">
          <q-card-section class="text-subtitle2 text-center text-cyan-1" v-if="loadedDonut">
            Coût annuel
            <Doughnut :data="donutData" style="height: 200px"/>
          </q-card-section>
        </q-card>
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
import { Doughnut } from 'vue-chartjs';
import { Chart as ChartJS, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale, DoughnutController, ArcElement } from 'chart.js';
ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale, DoughnutController, ArcElement);
import api from '../../api';
import VueApexCharts from "vue3-apexcharts";
import {AtomSpinner} from 'epic-spinners'

export default {
  name: 'HomePage',
  components: {
    Doughnut,
    apexchart: VueApexCharts,
    AtomSpinner
  },

  data() {
    return {
      loadedPage: false,
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
      calendarDialog: false,
      dateCalendar: new Date().toISOString().substr(0, 10).replace(/-/g, '/'),
      splitterModel: 62,
      currentYear: new Date().getFullYear(),
      previousYear: new Date().getFullYear() - 1,
      loadedBar: false,
      barData: null,
      toggleMonth: false,
      loadedDonut: false,
      donutData: null,
      loadedTopFiches: false,
      topFichesData: null,
      chartOptions: {
        chart: {
          id: "barChart",
        },
        tooltip: {
          hideEmptySeries: false,
        },
        xaxis: {
          categories: [],
          labels: {
            style: {
              colors:["#e0f7fa"]
            }
          }
        },
        yaxis: {
          labels: {
            style: {
              colors:["#e0f7fa"]
            }
          },
          title: {
            text: "Fiches",
            colors: "#e0f7fa"
          },
          axisBorder: {
            show: true,
            color: "#e0f7fa"
          }
        },
        grid: {
          show: true,
          borderColor: "#e0f7fa",
          strokeDashArray: 20,
          position: "back",
          xaxis: {
            lines: {
            show: false
            }
          },
          yaxis: {
            lines: {
              show: true,
            }
          }
        },
        markers: {
          shape: 'circle', // ou 'square', etc.
          radius: 5 // Ajustez le rayon si nécessaire
        },
        labels: {
          colors: '#e0f7fa', // Définissez la couleur du texte de la légende
          useSeriesColors: false // Mettez sur true pour utiliser les couleurs des séries
        },
        plotOptions: {
          bar: {
              borderRadius: 10,
              columnWidth: '50%',
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
          }
        },
        dataLabels: {
          enabled: true,
        },
      series: [
        {
          name: "Fiches",
          data: [],
          color: '#4dd0e1',
        },
        {
          name: "Unités de conditionnement",
          data: [],
          color: '#ffb74d',
        },
      ],
    };
  },

  computed: {
    ...mapGetters('matieresPremieres', ['matieresCdeCount', 'matieresLivraisonCount']),
    ...mapGetters('demandes', ['nombreDemandes', 'demandeProche', 'nombreDemandesProche', 'demandesDates', 'demandesAll']),
    ...mapGetters('fiches', ['fichesControlCount', 'fichesSemaine']),

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

  },

  async mounted() {
    try {
      await this.loadMatieresPremieres();
      await this.loadDemandes();
      await this.loadFiches();
      await this.loadData();
      await this.loadbarData();
      await this.loadTopFichesData();
      try {
        const response = await api.get('/PPH/fiches/count_per_service'); // URL de votre API
        this.donutData = this.DonutData(response.data);
        this.loadedDonut = true;
      } catch (e) {
        console.error('Erreur lors du chargement des données du donut :', e);
        this.loadedDonut = true;
      }
    } catch (e) {
      console.error('Erreur lors du chargement des données des cartes :', e);
    } finally {
          this.$nextTick(() => {

      this.loadedPage = true;
    });
    }
  },

  watch: {
    toggleMonth() {
      this.loadbarData();
      this.barDataSet();
      this.loadData();
      this.processData();
    },
    dateCalendar(newVal, oldVal) {
      console.log('Ancienne date:', oldVal, 'Nouvelle date:', newVal);
    }
  },
  methods: {
    ...mapActions('matieresPremieres', ['loadMatieresPremieres']),
    ...mapActions('demandes', ['loadDemandes']),
    ...mapActions('fiches', ['loadFiches']),

    openCalendar() {
      this.calendarDialog = true;

      console.log('Formatée pour comparaison:', this.dateCalendar.replace(/\//g, '-'));
      console.log('Demandes pour date sélectionnée:', this.demandesDatesSelect);
    },

    async loadData() {
      try {
        const url = this.toggleMonth ? 'fiches-mois' : 'fiches-semaine';
        const response = await api.get(`/PPH/${url}`); // Remplacez par l'URL de votre API
        this.processData(response.data);
        this.loadedBar = true;
      } catch (error) {
        console.error('Erreur lors du chargement des données de l\'API:', error);
      }
      this.loadedBar = true;
    },
    processData(data) {
      // Traitez ici les données de l'API et mettez à jour chartOptions et series
      // Exemple :
      this.chartOptions.xaxis.categories = data.map(item => item.week);
      this.series[0].data = data.map(item => item.count);
      this.series[1].data = data.map(item => item.qte);
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

   DonutData(data) {
      function getRandomColor() {
        const letters = '0123456789ABCDEF';
        let color = '#';
        for (let i = 0; i < 6; i++) {
          color += letters[Math.floor(Math.random() * 16)];
        }
        return color;
      }

      // Générer un tableau de couleurs, une pour chaque élément de 'data'
      const backgroundColors = data.map(() => getRandomColor());

      return {
        labels: data.map(s => s.service), // Les noms des services
        datasets: [{
          data: data.map(c => c.count), // Les nombres de fiches par service
          backgroundColor: backgroundColors,
          borderWidth: 0
        }],
        options: {
          plugins: {
            legend: {
              position: "left",
              labels: {
                color: '#4dd0e1' // Modifiez 'votre_couleur' selon la couleur désirée
              }
            }
          }
        },
      };
    },

    async loadbarData() {
    this.loadedBar = false;
      try {
        const url = this.toggleMonth ? 'fiches-mois' : 'fiches-semaine';
        const response = await api.get(`/PPH/${url}`);
        this.barData = this.barDataSet(response.data);
        this.createBarChart(this.barData);
        this.loadedBar = true;
      } catch (e) {
        console.error('Erreur lors du chargement des données :', e);
        this.loadedBar = true;
      }
    },

    barDataSet(data) {
      return {
        labels: this.toggleMonth ? data.map(item => item.month) : data.map(item => item.week),
        datasets: [
        {
          label: this.toggleMonth ? 'Fiches/mois' : 'Fiches/semaines',
          backgroundColor: '#4dd0e1',
          data: data.map(item => item.count)
        },
        {
          label: this.toggleMonth ? 'UnCdt/mois' : 'UnCdt/semaines',
          backgroundColor: '#ffb74d',
          data: data.map(nb => nb.qte)
        }],
        options: {
          scales: {
            y: {
              ticks: {
                color: ['rgba(255, 39, 45, 1)'],
              },
              border: {
                display: true,
                color: "red",
              },
            },
            x: {
              ticks: {
                color: "red",
              },
              border: {
                display: true,
                color: "#4dd0e1",
              },
            }
          },
          plugins: {
            legend: {
              labels: {
                color: "#4dd0e1" // Couleur du label de la légende
              }
            }
          }
        }
      }
    },
  },
};
</script>

<style>
.positive {
  color: #81c784;
}

.negative {
  color: #e57373;
}

.scroll-container {
    max-height: 300px; /* ou toute autre valeur selon vos besoins */
    overflow-y: auto;
}
</style>


