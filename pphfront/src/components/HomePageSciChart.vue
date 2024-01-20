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
      <div class="row q-mx-md q-mt-lg bd-radius-10 bg-op-8 justify-center" style="background-color:#1a2946;">
        <div class="text-h6 text-cyan-4">Tableau de bord</div>
        <div class="row">
        <div class="q-col-3 q-ml-sm">
          <div class="text-subtitle2 items-center text-center text-cyan-1" style="background-color:#1a2946;">
          <q-toggle
             class="text-cyan-1"
             v-model="toggleMonth"
             color="red-4"
             icon="bar_chart"
             label="semaines - mois"
             size="md"
          /> année {{ currentYear }}
          </div>
          <div class="container">
            <div id="lineChart"  class="bd-radius-10" style="width: 300px; height: 200px;"></div>
          </div>
        </div>
        <div class="q-col-3 q-mx-sm">
          <div class="text-subtitle2 text-center text-cyan-1">
            {{ currentYear }}
          </div>
          <div class="container">
            <div id="columnChart"  class="bd-radius-10" style="width: 300px; height: 200px;"></div>
          </div>
        </div>
        <div class="q-col-3">
          <div class="text-subtitle2 text-center text-cyan-1">
            Répartition des fiches
          </div>
          <div class="container">
            <div id="pieChart"  class="bd-radius-10" style="width: 300px; height: 200px; background-color:#1a2946;"></div>
          </div>
        </div>
        <div class="q-col-3 q-mx-sm">
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
import { Bar } from 'vue-chartjs';
import { Chart as ChartJS, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale, ArcElement } from 'chart.js';
ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale, ArcElement);
import api from '../../api';
import { chartBuilder } from "scichart/Builder/chartBuilder";

import {
  ESeriesType,
  EThemeProviderType,
  SciChartSurface,
  NumericAxis,
  FastLineRenderableSeries,
  XyDataSeries,
  EllipsePointMarker,
  SweepAnimation,
  SciChartJsNavyTheme,
  NumberRange,
  EAxisAlignment,
} from "scichart";

export default {
  name: 'HomePage',
  components: { Bar },

  data() {
    return {
      currentYear: new Date().getFullYear(),
      lineChart: null,
      toggleMonth: false,
      pieChart: null,
      columnChart: null,
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
    this.loadChartData();
    this.pieChartData();
    this.lineChart = this.initlineChart();
    this.pieChart = this.createPieChart();
    this.columnChart = this.initColumnChart();
    try {
      const response = await api.get('/PPH/fiches/count_per_service');
      this.createPieChart(response.data);
    } catch (e) {
      console.error('Erreur lors du chargement des données pour le pie chart:', e);
    }
  },

  beforeUnmount() {
    this.lineChart.then((sciChartSurface) => {
      sciChartSurface.delete();
    });
  },

  watch: {
    toggleMonth() {
      this.loadChartData();
    },
  },

  methods: {
    ...mapActions('matieresPremieres', ['loadMatieresPremieres']),
    ...mapActions('demandes', ['loadDemandes']),
    ...mapActions('fiches', ['loadFiches', 'loadFichesSemaine',]),

    async initColumnChart(data) {
      const xValues = this.toggleMonth ? data.map(item => item.month) : data.map(item => item.week);
      const yValues = data.map(item => item.count);

      await chartBuilder.build2DChart("columChart", {
        surface: { theme: { type: EThemeProviderType.Dark } },
        series: [
          {
            type: ESeriesType.ColumnSeries,
            xyData: {
              xValues,
              yValues,
            },
            options: {
              fill: "rgba(176, 196, 222, 0.5)",
              stroke: "rgba(176, 196, 222, 1)",
              strokeThickness: 2,
              dataPointWidth: 0.7,
            }
          }
        ]
      });
    },

    async createPieChart(data) {
      // Vérifier si data est défini
      if (!data) return;

      function getRandomColor() {
        const letters = '0123456789ABCDEF';
        let color = '#';
        for (let i = 0; i < 6; i++) {
          color += letters[Math.floor(Math.random() * 16)];
        }
        return color;
      }

      const segments = data.map(item => ({
        text: item.service,
        value: item.count,
        color: getRandomColor()
      }));

      await chartBuilder.buildPieChart("pieChart", {
        segments: segments
      });
    },


    async pieChartData() {
      try {
        const response = await api.get('/PPH/fiches/count_per_service'); // URL de votre API
        this.pieChart = this.createPieChart(response.data);
      } catch (e) {
        console.error('Erreur lors du chargement des données :', e);
      }
    },

    async initlineChart(data) {
      // SciChartSurface.setRuntimeLicenseKey("VOTRE_CLÉ_DE_LICENCE");

      // Initialisation de SciChartSurface. N'oubliez pas d'utiliser await!
      const { sciChartSurface, wasmContext } = await SciChartSurface.create("lineChart", {
        theme: new SciChartJsNavyTheme(),
        title: this.toggleMonth ? 'Fiches/mois' : 'Fiches/semaines',
        titleStyle: { fontSize: 12, color: '#4dd0e1' }
      });

      // Création d'un axe X et Y avec un padding growBy
      const growBy = new NumberRange(1, 1);

      sciChartSurface.xAxes.add(new NumericAxis(wasmContext, {
        axisTitle: this.toggleMonth ? 'Mois' : 'Semaines',
        growBy,
        axisTitleStyle:{fontSize:10, color: '#ffb74d'},
        labelStyle:{color: '#ffb74d'},
      }));
      sciChartSurface.yAxes.add(new NumericAxis(wasmContext, {
        axisTitle: "Nombre de fiches",
        growBy,
        axisAlignment: EAxisAlignment.Left,
        axisTitleStyle:{fontSize:10, color: '#4dd0e1'},
        labelStyle:{color: '#4dd0e1'},
      }));

      // Création d'une série en ligne avec des données initiales
      // Remplacez ces données par vos données réelles
      const lineSeries = new FastLineRenderableSeries(wasmContext, {
        stroke: "steelblue",
        strokeThickness: 3,
        dataSeries: new XyDataSeries(wasmContext, {
          xValues: this.toggleMonth ? data.map(item => item.month) : data.map(item => item.week),
          yValues: data.map(item => item.count)
        }),
        pointMarker: new EllipsePointMarker(wasmContext, { width: 11, height: 11, fill: "#fff" }),
        animation: new SweepAnimation({ duration: 300, fadeEffect: true })
      });

      sciChartSurface.renderableSeries.add(lineSeries);

      return sciChartSurface;
    },

    async loadChartData() {
      try {
        const url = this.toggleMonth ? 'fiches-mois' : 'fiches-semaine';
        const response = await api.get(`/PPH/${url}`);
        this.lineChart = this.initlineChart(response.data);
      } catch (e) {
        console.error('Erreur lors du chargement des données :', e);
      }
    },
  },
};
</script>





