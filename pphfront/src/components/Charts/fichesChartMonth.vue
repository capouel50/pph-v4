<template>
  <bar v-if="loaded" :chartData="chartDataMonth" :options="chartOptions"/>
</template>

<script>
import api from '../../../api';
import { Bar } from 'vue-chartjs';
import { Chart as ChartJS, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale } from 'chart.js';

ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale);

export default {
  name: "fichesChartYear",
  components: { Bar },
  data() {
    return {
      currentYear: new Date().getFullYear(),
      loaded: false,
      chartDataMonth: {
        labels: [],
        datasets: [
          {
            label: 'Fiches de fabrication/mois',
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

      try {
        const { data } = await api.get(apiUrl);

        const currentYear = new Date().getFullYear();
        const countByMonth = {};
        const filteredData = data.filter((fiche) => new Date(fiche.date_fab).getFullYear() === currentYear);

        filteredData.forEach((fiche) => {
          const date = new Date(fiche.date_fab);
          const monthNumber = date.getMonth() + 1;

          countByMonth[monthNumber] = (countByMonth[monthNumber] || 0) + 1;
        });

        this.chartDataMonth.labels = Object.keys(countByMonth).map(month => {
          return this.getMonthName(month);
        });
        this.chartDataMonth.datasets[0].data = Object.values(countByMonth);
        this.loaded = true;
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    },
    getMonthName(monthNumber) {
      const months = [
        'Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin',
        'Juillet', 'Août', 'Septembre', 'Octobre', 'Novembre', 'Décembre'
      ];
      return months[monthNumber - 1];
    },
  },
};
</script>
