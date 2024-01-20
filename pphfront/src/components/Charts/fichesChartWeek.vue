<template>
  <bar v-if="loaded" :chartData="chartData"/>
</template>

<script>
import api from '../../../api';
import { Bar } from 'vue-chartjs'
import { Chart as ChartJS, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale } from 'chart.js'

ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale)

export default {
  components: {
    Bar
  },
  data() {
    return {
      currentYear: new Date().getFullYear(),
      loaded: false,
      chartData: {
        labels: [],
        datasets: [
          {
            label: 'Fiches de fabrication/semaine',
            data: [],
            backgroundColor: 'rgba(54, 162, 235, 0.2)'
          }
        ]
      },
      chartOptions: {
        responsive: true
      }
    };
  },

  async mounted() {
    this.loadData();
  },

  methods: {
    async loadData() {
      const apiUrl = 'PPH/fiches';

      await api.get(apiUrl)
          .then(({data}) => {
            console.log('Response Data:', data);

            // Obtenir l'année en cours
            const currentYear = new Date().getFullYear();

            // Utiliser un objet pour stocker le nombre d'enregistrements pour chaque semaine
            const countByWeek = {};

            // Filtrer les fiches pour l'année en cours
            const filteredData = data.filter((fiche) => new Date(fiche.date_fab).getFullYear() === currentYear);

            filteredData.forEach((fiche) => {
              const date = new Date(fiche.date_fab);
              const weekNumber = getWeekNumber(date);

              // Si le numéro de semaine existe déjà dans l'objet, incrémenter le compteur, sinon initialiser à 1
              countByWeek[weekNumber] = (countByWeek[weekNumber] || 0) + 1;
            });

            // Mettre à jour le graphique avec les données de comptage par semaine
            this.chartData.labels = Object.keys(countByWeek);
            this.chartData.datasets[0].data = Object.values(countByWeek);
            this.loaded = true;
          })
          .catch((error) => {
            console.error('Error fetching data:', error);
          });

      // Fonction pour obtenir le numéro de semaine à partir d'une date
      function getWeekNumber(date) {
        const d = new Date(Date.UTC(date.getFullYear(), date.getMonth(), date.getDate()));
        const dayNum = d.getUTCDay() || 7;
        d.setUTCDate(d.getUTCDate() + 4 - dayNum);
        const yearStart = new Date(Date.UTC(d.getUTCFullYear(), 0, 1));
        return Math.ceil((((d - yearStart) / 86400000) + 1) / 7);
      }
    }
  }
};

</script>

