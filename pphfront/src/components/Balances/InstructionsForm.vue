<template>
  <div class="row">
    <div class="col-12">

    <div
      v-for="(row, index) in formRows"
      :key="index"
      class="row"
    >
      <div class="col-2 q-mr-md">
        <q-input
        v-model="row.action"
        color="cyan-4"
        label="Action"
      />
      </div>
      <div class="col-5 q-mr-md">
        <q-input
        v-model="row.description"
        color="cyan-4"
        label="Description"
      />
      </div>
      <div class="col-1 q-mr-md">
        <q-input
        v-model="row.nom"
        color="cyan-4"
        label="Nom"
      />
      </div>
      <div class="col-1 q-mr-md">
        <q-input
        v-model="row.instruction"
        color="cyan-4"
        label="Instruction"
      />
      </div>
      <div class="col-1 q-mr-md">
        <q-input
        v-model="row.reponse"
        color="cyan-4"
        label="Réponse"
      />
      </div>

      <q-btn-group flat class="q-ml-lg">
        <q-btn flat size="sm" @click="addInstructionState(row)" icon="check_circle" color="green-4"/>
        <q-btn flat size="sm" @click="removeRow(row)" icon="delete_forever" color="red-4"/>
      </q-btn-group>
    </div>

    </div>
  </div>
</template>

<script>
import {mapActions, mapGetters, mapMutations} from 'vuex';

export default {
  props: ['newId', 'balanceId'],
  data() {
    return {
      formRows: [
        {
          num_balance: null,
          instructionId: null,
          nom: null,
          action: null,
          instruction: null,
          description: null,
          reponse: null,
        }
      ],
    };
  },
  computed: {
    ...mapGetters('balances', ['allBalances', 'allInstructionsBalances']),

  },

  async created() {
      this.loadLastId();
      this.fetchInstructionsAndAddRow();
      if(this.balanceId){
        this.loadInstructionsBalances();
        // Here we reset formRows and repopulate it if formuleId is set
          this.formRows = this.allInstructionsBalances
            .filter(instruction => instruction.modele_balance === this.balanceId)
            .map(instruction => ({
              num_balance: instruction.modele_balance,
              instructionId: instruction.id,
              instruction: instruction.instruction,
              nom: instruction.nom,
              action: instruction.action,
              description: instruction.description,
              reponse: instruction.format_reponse,
            }));
          this.addRow();
        }
      console.log('instructions', this.allInstructionsBalances);
    },

  methods: {
    ...mapActions('balances', ['loadBalances', 'loadInstructionsBalances']),
    ...mapMutations('balances', ['ADD_INSTRUCTION', 'REMOVE_INSTRUCTION']),

    async fetchInstructionsAndAddRow() {
        if (!this.balanceId) {
          try {
            const instructions = await this.getInstructions();
            if (instructions.length > 0) {
              this.formRows = instructions.map((instruction) => ({
                num_balance: instruction.modele_balance,
                instructionId: instruction.id,
                instruction: instruction.instruction,
                nom: instruction.nom,
                action: instruction.action,
                description: instruction.description,
                reponse: instruction.format_reponse,
              }));
              this.addRow();
            }
          } catch (error) {
            console.error('Erreur lors de la récupération des instructions', error);
          }
        }
      },

    async getInstructions() {
      const numBalance = this.newId;

      return this.allInstructionsBalances.filter(instruction => instruction.modele_balance === numBalance);
    },

    async loadLastId() {
      try {
        this.formRows[0].num_balance = this.newId;
        console.log('NewId', this.newId)
      } catch (error) {
        console.error('Erreur lors de la récupération du dernier ID de la formule', error);
      }
    },

    async addRow() {
      try {
        if(this.balanceId){
          this.formRows.push({
          num_balance: this.balanceId,
          instructionId: null,
          nom: null,
          action: null,
          instruction: null,
          description: null,
          reponse: null,
        });
        }else {
          this.formRows.push({
          num_balance: this.newId,
          instructionId: null,
          nom: null,
          action: null,
          instruction: null,
          description: null,
          reponse: null,
          });
        }
      } catch (error) {
        console.error('Erreur lors de la récupération du dernier ID du modèle Formule', error);
      }
    },

    addInstructionState(row) {
        this.ADD_INSTRUCTION({
          num_balance: this.balanceId,
          instructionId: null,
          nom: null,
          action: null,
          instruction: null,
          description: null,
          reponse: null,
        });
      if(this.formRows.indexOf(row) === this.formRows.length - 1) {
        this.addRow();
      }
    },

    removeRow(row) {
      this.REMOVE_INSTRUCTION({
        num_balance: row.num_balance,
        instructionId: row.instructionId,
      });
      // Supprime la ligne qui contient le bouton
      const index = this.formRows.indexOf(row);
      this.formRows.splice(index, 1);
    },

  },
};
</script>


