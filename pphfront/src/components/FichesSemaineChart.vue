<template>
  <div class="container">
    <Bar v-if="loaded" :chart-data="chartData" />
  </div>
</template>

<script>
import { Bar } from 'vue-chartjs';
import { Chart as ChartJS, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale } from 'chart.js';
import api from '../../api';
ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale);

export default {
  name: 'FichesSemaineChart',
  components: { Bar },
  data() {
    return {
      loaded: false,
      chartData: null
    };
  },
  async mounted() {
    try {
      const response = await api.get('/PPH/fiches-semaine'); // URL de votre API
      this.chartData = this.formatChartData(response.data);
      this.loaded = true;
    } catch (e) {
      console.error('Erreur lors du chargement des données :', e);
      this.loaded = true;
    }
  },
  methods: {
    formatChartData(data) {
      return {
        labels: data.map(item => `Semaine ${item.week}`),
        datasets: [{
          label: 'Nombre de fiches',
          backgroundColor: '#f87979',
          data: data.map(item => item.count)
        }]
      };
    }
  }
}
</script>
