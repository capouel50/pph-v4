<template>
  <q-page>
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
         <div class="col-12 justify-center">
        <div class="text-h6 text-cyan-4">Tableau de bord</div>
           </div>
        <div class="row">
        <div class="q-col-3 q-mx-sm items-center">
          <div class="text-subtitle2 items-center text-center text-cyan-1">
          <q-toggle
             v-model="toggleMonth"
             color="red-4"
             icon="bar_chart"
             label="semaines - mois année "
             size="md"
          /> {{ currentYear }}
          </div>
          <div class="container">
            <Bar v-if="loadedBar" :data="barData" style="height: 200px;"/>
          </div>
        </div>
        <div class="q-col-3 items-center">
          <div class="container">
          <table v-if="loadedTopFiches" class="table-style" style="height: 200px;">
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
          <div v-else class="text-cyan-4">
            Chargement des données...
          </div>
        </div>
        </div>
        <div class="q-col-3 q-mx-sm items-center">
          <div class="text-subtitle2 text-center text-cyan-1">
            Répartition des fiches
          </div>
          <div class="container">
            <Doughnut v-if="loadedDonut" :data="donutData" style="width: 250px; height: 200px;"/>
          </div>
        </div>
        <div class="q-col-3 q-mr-sm items-center">
          <div class="text-subtitle2 text-center text-cyan-1">
            Coût annuel
          </div>
          <div class="container">
            <Bar />
          </div>
        </div>
        </div>
      </div>
  </q-page>
</template>

<script>
import { mapActions, mapGetters } from 'vuex';
import { Bar, Doughnut } from 'vue-chartjs';
import { Chart as ChartJS, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale, DoughnutController, ArcElement } from 'chart.js';
ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale, DoughnutController, ArcElement);
import api from '../../api';

export default {
  name: 'HomePage',
  components: { Bar, Doughnut },

  data() {
    return {
      currentYear: new Date().getFullYear(),
      previousYear: new Date().getFullYear() - 1,
      loadedBar: false,
      barData: null,
      toggleMonth: false,
      loadedDonut: false,
      donutData: null,
      loadedTopFiches: false,
      topFichesData: null,
    };
  },

  computed: {
    ...mapGetters('matieresPremieres', ['matieresCdeCount', 'matieresLivraisonCount']),
    ...mapGetters('demandes', ['nombreDemandes', 'demandeProche', 'nombreDemandesProche']),
    ...mapGetters('fiches', ['fichesControlCount', 'fichesSemaine']),

  },

  async mounted() {
    this.loadMatieresPremieres();
    this.loadDemandes();
    this.loadFiches();
    await this.loadbarData();
    await this.loadTopFichesData();
    try {
      const response = await api.get('/PPH/fiches/count_per_service'); // URL de votre API
      this.donutData = this.DonutData(response.data);
      this.loadedDonut= true;
    } catch (e) {
      console.error('Erreur lors du chargement des données :', e);
      this.loadedDonut = true;
    }// Appel de la méthode loadChartData
  },

  watch: {
    toggleMonth() {
      this.loadbarData();
      this.barDataSet();
    },
  },

  methods: {
    ...mapActions('matieresPremieres', ['loadMatieresPremieres']),
    ...mapActions('demandes', ['loadDemandes']),
    ...mapActions('fiches', ['loadFiches', 'loadFichesSemaine',]),

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

</style>


