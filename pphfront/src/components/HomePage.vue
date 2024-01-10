<template>
  <q-page>
    <div class="row justify-center">
      <div class="col-md-8">
        <div class="row">
          <div class="col-6 text-h5 text-center text-cyan-4">
            Matières premières
          </div>
          <div class="col-6 text-h5 text-center text-cyan-4">
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
  </q-page>
</template>

<script>
import {mapActions, mapGetters} from 'vuex';

export default {
  name: "HomePage",

  computed: {
    ...mapGetters('matieresPremieres', ['matieresCdeCount', 'matieresLivraisonCount']),
    ...mapGetters('demandes', ['nombreDemandes', 'demandeProche', 'nombreDemandesProche']),
    ...mapGetters('fiches', ['fichesControlCount']),
  },

  created() {
    this.loadMatieresPremieres();
    this.loadDemandes();
    this.loadFiches();
  },

  methods: {
    ...mapActions('matieresPremieres', ['loadMatieresPremieres']),
    ...mapActions('demandes', ['loadDemandes']),
    ...mapActions('fiches', ['loadFiches']),
  },
};
</script>

<style scoped>

</style>