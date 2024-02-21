<template>
  <q-page v-if="loading">
    <div class="q-mt-sm ">
      <div class="row text-h6 text-cyan-4 justify-center">
        Fiche n°{{ fiche.id }}
      </div>
      <div class="row text-subtitle1 text-orange-4 justify-center">
        {{ fiche.prep.nom }}
      </div>
    </div>

    <div class="row justify-evenly q-mt-md">

      <div class="col-3">
        <div class="row justify-between">
          <div class="col-5">
            <q-card class="q-mb-md bg-op-8">
          <q-card-section>

            <div class="row">
              <div class="col-10  text-subtitle1 text-cyan-4 text-center">
                Matériel
              </div>
              <div class="col-1">
                <q-btn
                  color="grey"
                  round
                  flat
                  dense
                  :icon="materiel ? 'keyboard_arrow_up' : 'keyboard_arrow_down'"
                  @click="materiel = !materiel"
                />
              </div>
            </div>

          </q-card-section>

          <q-slide-transition>
            <div v-show="materiel">
              <q-separator />
              <q-card-section class="text-subtitle2">
                <div>Mortier</div>
                <div>Pilon</div>
              </q-card-section>
            </div>
          </q-slide-transition>

        </q-card>
          </div>

          <div class="col-5">
            <q-card class="q-mb-md bg-op-8">
          <q-card-section>

            <div class="row">
              <div class="col-10 text-subtitle1 text-cyan-4 text-center">
                Habillage
              </div>
              <div class="col-1">
                <q-btn
                  color="grey"
                  round
                  flat
                  dense
                  :icon="habillage ? 'keyboard_arrow_up' : 'keyboard_arrow_down'"
                  @click="habillage = !habillage"
                />
              </div>
            </div>

          </q-card-section>

          <q-slide-transition>
            <div v-show="habillage">
              <q-separator />
              <q-card-section class="text-subtitle2">
                <div>Surblouse</div>
                <div>Charlotte</div>
              </q-card-section>
            </div>
          </q-slide-transition>

        </q-card>
          </div>
        </div>
        <div>
          <q-card class="q-mb-md bg-op-8">
          <q-card-section>

            <div class="row">
              <div class="col-10 offset-1 text-subtitle1 text-cyan-4 text-center">
                EPI
              </div>
              <div class="col-1">
                <q-btn
                  color="grey"
                  round
                  flat
                  dense
                  :icon="expanded ? 'keyboard_arrow_up' : 'keyboard_arrow_down'"
                  @click="expanded = !expanded"
                />
              </div>
            </div>

          </q-card-section>

          <q-slide-transition>
            <div v-show="expanded">
              <q-separator />
              <q-card-section class="text-subtitle2">
                <div>Masque FFP2</div>
                <div>Gants vynil</div>
              </q-card-section>
            </div>
          </q-slide-transition>

        </q-card>
        </div>
        <div>
          <q-card class="bg-op-8">
          <q-card-section>

            <div class="row">
              <div class="col-10 offset-1 text-subtitle1 text-cyan-4 text-center">
                Mode opératoire
              </div>
              <div class="col-1">
                <q-btn
                  color="grey"
                  round
                  flat
                  dense
                  :icon="modeOp ? 'keyboard_arrow_up' : 'keyboard_arrow_down'"
                  @click="modeOp = !modeOp"
                />
              </div>
            </div>

          </q-card-section>

          <q-slide-transition>
            <div v-show="modeOp">
              <q-separator />
              <q-card-section class="text-subtitle2">
                <div>
                  {{ fiche.prep.mode_operatoire}}
                </div>
              </q-card-section>
            </div>
          </q-slide-transition>

        </q-card>
        </div>
      </div>

      <div class="col-6">
        <q-card class="bg-op-8">
          <q-card-section>

            <div class="text-subtitle1 text-cyan-4 text-center">
              Composition de la formule
            </div>

          </q-card-section>

          <q-separator/>

          <q-card-section>
            <q-list v-for="compo in composition" :key="compo.id">
              <q-item class="row">
                <q-item-section class="col-4 text-cyan-4">
                  {{ compo.matiere.nom}}
                </q-item-section>
                <q-item-section class="col-2 text-orange-4">
                  {{ compo.result }}{{ compo.matiere.unite_mesure.nom}}
                </q-item-section>
                <q-item-section class="col-2">
                  <q-input
                      v-model="num_reception"
                      label="N° réception"
                      color="cyan-4"
                  />
                </q-item-section>
                <q-item-section class="col-2 offset-1">
                  <q-input
                      v-model="compo.pesee"
                      label="Quantité"
                      color="cyan-4"
                      @focus="updateQteTheory(compo)"
                  >
                    <template v-slot:append>
                      <div class="text-cyan-4 text-subtitle2">{{ compo.matiere.unite_mesure.nom}}</div>
                    </template>
                  </q-input>
                </q-item-section>
              </q-item>
            </q-list>
          </q-card-section>

          <q-separator/>

          <q-card-section>
            <q-card-actions class="justify-center">
              <q-btn-group>
                <q-btn
                flat
                color="green-4"
                label="Valider"
                @click="saveData"
              />
                <q-btn
                flat
                color="red-4"
                label="Annuler"
                @click="resetData"
              />
              </q-btn-group>
            </q-card-actions>
          </q-card-section>

        </q-card>
      </div>

      <div class="col-2">
        <div>
          <q-card class="bg-op-8">
          <q-card-section>

            <div class="text-subtitle1 text-cyan-4 text-center">
              Pesée
            </div>

          </q-card-section>

          <q-separator/>

          <q-card-section>
            <div class="text-center text-orange-4 text-h6">
              {{ this.selectedCompoPesee }}{{ qteTheory.unite }} / {{ qteTheory.value }}{{ qteTheory.unite }}
            </div>
            <div class=" row justify-center">
              <div class="text-subtiltle1 text-cyan-4">
                Ecart :
              </div>
              <div class="text-subtiltle1" :class="getDeviationPercentageColor()">
                {{ calculateDeviationPercentage() }}%
              </div>
            </div>
          </q-card-section>

          <q-separator/>

          <q-card-section>
            <q-card-actions class="justify-center">
              <q-btn-group>
                <q-btn
                flat
                color="green-4"
                label="Valider"
                class="hover-effect-succes"
                @click="saveData"
              />
              <q-btn
                flat
                color="cyan-4"
                label="Tare"
                class="hover-effect"
                @click="Tare"
              />
              </q-btn-group>
            </q-card-actions>
          </q-card-section>

        </q-card>
        </div>
        <div class="q-mt-md">
          <q-card class="bg-op-8">
          <q-card-section>

            <div class="text-subtitle1 text-cyan-4 text-center">
              Impression
            </div>

          </q-card-section>

          <q-separator/>

          <q-card-section>
            <q-card-actions class="justify-center">
              <q-btn-group>
                <q-btn
                    flat
                    label="Fiche"
                    color="cyan-4"
                    class="hover-effect"
                    @click="imprimerFiche"
                ><q-tooltip class="bg-blue-grey-4">Imprimer la fiche de fabrication</q-tooltip>
                </q-btn>
                <q-btn
                    flat
                    label="Etiquettes"
                    color="cyan-4"
                    class="hover-effect"
                    @click="imprimerEtiquette"
                ><q-tooltip class="bg-blue-grey-4">Imprimer lees étiquettes</q-tooltip>
                </q-btn>
              </q-btn-group>
            </q-card-actions>
          </q-card-section>

        </q-card>
        </div>
      </div>

    </div>

  </q-page>
  <q-page v-else class="row items-center justify-center">
  <div class=" row justify-center">
      <atom-spinner
        class="bg-op-8"
        :animation-duration="1000"
        :size="100"
        :color="'#ff1d5e'"
      />
      </div>
  </q-page>
</template>

<script>
import { mapActions, mapGetters } from 'vuex';
import {AtomSpinner} from 'epic-spinners'
import { getCalculatedQty } from '@/utils/helpers'
export default {
  name: 'InfosFiche',
  components: {
    AtomSpinner
  },

  data() {
    return {
      loading: false,
      id: null,
      fiche: [],
      composition: [],
      parametres: [],
      result: [],
      expanded: false,
      modeOp: false,
      habillage: false,
      materiel: false,
      qteTheory: {
        value: null,
        unite: null,
      },
      selectedCompoPesee: null,
    };
  },

  computed: {
    ...mapGetters('fiches', ['allFiches', 'allParametresFiches']),
    ...mapGetters('formules', ['allCompositions', 'allParametresFormules']),
  },

  async created() {
    this.id = Number(this.$route.params.id);  // mise à jour de l'ID de l'URL

    await Promise.all([
      this.loadFiches(),
      this.loadCompositions(),
      this.loadParametresFormules(),
      this.loadParametresFiches()
    ]);

    this.fiche = this.allFiches.find(fiche => fiche.id === this.id);
    this.parametres = this.allParametresFiches.filter(param => param.num_fiche === this.fiche.id);
    console.log('parametres : ', this.allParametresFiches);
    this.composition = this.allCompositions
    .filter(compo => compo.num_formule === this.fiche.prep.id)
    .map(compo => {
      const updatedCompo = {...compo};

      // Initialisez pesee pour chaque compo
      updatedCompo.pesee = 0;

      const formula = compo.calcul;
      const params = this.parametres;
      const qte = compo.qté;
      const unitMeasureString = compo.matiere.unite_mesure.nom;

      updatedCompo.result = getCalculatedQty(formula, params, qte, unitMeasureString);

      if (updatedCompo.matiere.unite_mesure.nom === 'ml' && updatedCompo.matiere.densite) {
        updatedCompo.result = (updatedCompo.result * updatedCompo.matiere.densite).toFixed(2);
        updatedCompo.matiere.unite_mesure.nom = 'g';
      }

      return updatedCompo;
    });
    this.loading= true;
  },

  methods: {
    ...mapActions('fiches', ['loadFiches', 'loadParametresFiches']),
    ...mapActions('formules', ['loadCompositions', 'loadParametresFormules']),

    updateQteTheory(compo) {
      this.selectedCompoPesee = compo.pesee;
      this.qteTheory.value = compo.result;
      if(compo.matiere.densite) {
        this.qteTheory.unite = 'g';
      }else{
        this.qteTheory.unite = compo.matiere.unite_mesure.nom;
      }
    },

    calculateDeviationPercentage() {
      // Convert values to Number if they aren't
      const liveDataValue = Number(this.selectedCompoPesee);
      const qteTheoryValue = Number(this.qteTheory.value);

      // Calculate the percentage difference
      const percentageDifference = ((Math.abs(liveDataValue - qteTheoryValue)) / qteTheoryValue) * 100;

      // Return the result rounded to to two decimal places
      return percentageDifference.toFixed(2);
    },

    getDeviationPercentageColor() {
      // calculate deviation percentage
      const deviationPercentage = this.calculateDeviationPercentage();

      // return the color class depending on the percetage
      return deviationPercentage < 5 ? 'text-green-4' : 'text-red-4';
    },

  },
}

</script>

<style scoped>

</style>






