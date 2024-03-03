<template>
  <div class="row">
    <div class="col-8">
    <div
      v-for="(row, index) in formRows"
      :key="index"
      class="row"
    >
      <q-select
        :label="row.article ? 'Article n° ' + (index + 1) : 'Ajouter un article'"
        v-model="row.article"
        color="cyan-4"
        class="col-6 hover-effect"
        :options="!formuleId && getArticles.length ? allArticlesStateLabel : allArticlesLabel"
        option-label="label"
        option-value="value"
      />
      <q-btn-group flat class="q-ml-lg">
        <q-btn flat size="sm" @click="addArticle(row)" icon="check_circle" color="green-4"/>
        <q-btn flat size="sm" @click="removeRow(row)" icon="delete_forever" color="red-4"/>
      </q-btn-group>
    </div>

    </div>
  </div>
</template>

<script>
import { mapActions, mapGetters, mapMutations } from 'vuex';

export default {
  props: ['newId', 'formuleId'],
  data() {
    return {
      selectedRowIndex: null,
      formRows: [
        {
          num_formule: null,
          articleId: null,
          article: null,
        }
      ],
    };
  },
  computed: {
    ...mapGetters('matieresPremieres', ['allMatieres']),
    ...mapGetters('formules', ['allArticlesFormules']),

    allArticlesLabel() {
        return this.allMatieres
            .filter(article => article.type.nom === "Matériel de laboratoire")
            .map(article => ({
              label: article.nom,
              value: article.id,
        }));
    },
    allArticlesStateLabel() {
        return this.allArticlesFormules
            .filter(article => article.num_formule === this.newId)
            .map(article => ({
              label: article.article,
              value: article.articleId,
        }));
    },
  },

  async created() {
    this.loadLastId();
    this.loadMatieresPremieres();
    this.fetchArticlesAndAddRow();
    if(this.formuleId){
      this.loadArticlesFormules();
      // Here we reset formRows and repopulate it if formuleId is set
      this.formRows = this.allArticlesFormules
        .filter(article => article.num_formule === this.formuleId)
        .map(article => ({
          num_formule: article.num_formule,
          articleId: article.article.id,
          article: article.article.nom,
        }));
      this.addRow();
    }
  },

  methods: {
    ...mapActions('matieresPremieres', ['loadMatieresPremieres']),
    ...mapActions('formules', ['loadArticlesFormules']),
    ...mapMutations('formules', ['ADD_ARTICLE', 'REMOVE_ARTICLE']),

    async fetchArticlesAndAddRow() {
        if (!this.formuleId) {
          try {
            const articles = await this.getArticles();
            if (articles.length > 0) {
              this.formRows = articles.map((article) => ({
                num_formule: article.num_formule,
                articleId: article.articleId,
                article: article.article,
              }));
              this.addRow();
            }
          } catch (error) {
            console.error('Erreur lors de la récupération des articles', error);
          }
        }
      },

    async loadLastId() {
      try {
        this.formRows[0].num_formule = this.newId;
      } catch (error) {
        console.error('Erreur lors de la récupération du dernier ID de la formule', error);
      }
    },

    async getArticles() {
      const numFormule = this.newId;

      return this.allArticlesFormules.filter(article => article.num_formule === numFormule);
    },

    addArticle(row) {
        this.ADD_ARTICLE({
          num_formule: row.num_formule,
          articleId: row.article.value,
          article: row.article.label,
        });
      if(this.formRows.indexOf(row) === this.formRows.length - 1) {
        this.addRow();
      }
    },

    async addRow() {
      // Récupérez l'ID du dernier enregistrement du modèle Formule depuis votre API Django
      try {
        if(this.formuleId){
          this.formRows.push({
          num_formule: this.formuleId,
          articleId: null,
          article: null,
        });
        }else {
          this.formRows.push({
            num_formule: this.newId,
            articleId: null,
            article: null,
          });
        }
      } catch (error) {
        console.error('Erreur lors de la récupération du dernier ID du modèle Formule', error);
      }
    },

    removeRow(row) {
      this.REMOVE_ARTICLE({
        num_formule: row.num_formule,
        articleId: row.articleId,
      });
      // Supprime la ligne qui contient le bouton
      const index = this.formRows.indexOf(row);
      this.formRows.splice(index, 1);
      console.log('allArticlesFormules', this.allArticlesFormules)
    },

  },
};
</script>


