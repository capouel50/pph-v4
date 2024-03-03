<template>
  <div class="q-pa-md">
      <q-stepper
          v-model="step"
          class="bg-op-8"
          vertical
          done-color="cyan-4"
          active-color="orange-4"
          header-nav
          animated
        >
        <div class="text-h5 text-center text-cyan-4">Profil de {{ user.first_name }} {{ user.last_name }}</div>
        <q-step
          :name="1"
          title="Identité"
          icon="person"
          :done="step > 1"
        >
          <div class="row">
            <q-input
                v-model="nom"
                color="cyan-4"
                label="Nom"
                class="col-2"
            >
              <template v-slot:before>
                <q-icon name="person" color="cyan-4" size="sm"/>
              </template>
            </q-input>
          </div>

          <div class="row">
            <q-input
                v-model="prenom"
                color="cyan-4"
                label="Prenom"
                class="col-2"
            >
              <template v-slot:before>
                <q-icon name="person" color="cyan-4" size="sm"/>
              </template>
            </q-input>
          </div>

          <q-stepper-navigation>
            <q-btn flat @click="step = 2" color="cyan-4" label="Suivant" class="hover-effect" />
          </q-stepper-navigation>
        </q-step>

        <q-step
          :name="2"
          title="Identifiants"
          icon="person"
          :done="step > 2"
        >
          <div class="row">
            <q-input
                type="email"
                v-model="email"
                color="cyan-4"
                label="E-mail"
                class="col-2"
            >
              <template v-slot:before>
                <q-icon name="person" color="cyan-4" size="sm"/>
              </template>
            </q-input>
          </div>
          <div class="row">
            <q-input
                v-model="username"
                color="cyan-4"
                label="Nom d'utilisateur"
                class="col-2"
            >
              <template v-slot:before>
                <q-icon name="person" color="cyan-4" size="sm"/>
              </template>
            </q-input>
          </div>

          <q-stepper-navigation>
            <q-btn flat @click="step = 1" color="cyan-4" label="Précédent" class="hover-effect q-ml-sm" />
            <q-btn flat @click="step = 3" color="cyan-4" label="Suivant" class="hover-effect"/>
          </q-stepper-navigation>
        </q-step>

        <q-step
          :name="3"
          title="Fonction"
          icon="person"
          :done="step > 3"
        >
          <div class="row">
            <q-select
                v-model="user_function"
                color="cyan-4"
                label="Nom"
                class="col-2"
                :options="allFunctionsLabel"
                option-label="label"
                option-value="id"
            >
              <template v-slot:before>
                <q-icon name="person" color="cyan-4" size="sm"/>
              </template>
            </q-select>
          </div>
          <q-stepper-navigation>
            <q-btn flat @click="step = 2" color="cyan-4" label="Précédent" class="hover-effect q-ml-sm" />
            <q-btn flat @click="step = 4" color="cyan-4" label="Terminer" class="hover-effect"/>
          </q-stepper-navigation>
        </q-step>
        <div class="row justify-center">
          <q-btn-group>
            <q-btn flat @click="callSubmit" color="green-4" label="Enregistrer" class="btn-flat-success-pph"/>
          </q-btn-group>
        </div>
      </q-stepper>
  </div>
</template>

<script>
import { mapActions, mapGetters } from 'vuex';
export default {
  components: {

  },
  data() {
    return {
      step: 1,
      nom: '',
      prenom: '',
      username:'',
      user_function: '',
      user_function_id: '',
      email: '',
      user: [],
      id: '',
    };
  },

  async created() {
    this.userId = Number(this.$route.params.id);
    this.loadUsers();
    this.loadFunctions();
    this.user = this.allUsers.find(user => user.id === this.userId);
    console.log('allFunctions', this.allFunctions);
    console.log('User', this.user);
    if(this.userId){
      this.nom = this.user.last_name;
      this.prenom = this.user.first_name;
      this.username = this.user.username;
      this.user_function = this.user.function.title;
      this.user_function_id = this.user.function.id;
      this.email = this.user.email;
    }
  },

  computed: {
  ...mapGetters('users', ['allUsers', 'allFunctions']),

    allFunctionsLabel() {
      return this.allFunctions.map(f => ({
        ...f,
        label: `${f.title}`,
        id: f.id,
      }));
    }
  },

  methods: {
  ...mapActions('users', ['loadUsers', 'updateUser', 'addUser', 'loadFunctions']),

    async callSubmit() {
    console.log('User', this.user);
      const formData = {
        last_name: this.nom,
        first_name: this.prenom,
        username: this.username,
        function: this.user_function_id,
        email: this.email,
      }
      console.log('formDataEnvoyé', formData);
      if(this.userId){
        this.updateSubmit(formData);
      }else{
        this.onSubmit(formData);
      }
    },

    async updateSubmit(formData) {
        const id = this.userId;
        await this.updateUser({id, formData});
      this.resetForm();
    },

    async onSubmit(formData) {
      try {
        await this.addUser(formData);
        this.resetForm();
      } catch (error) {
        console.error("Error adding supplier:", error);
      }
    },

    resetForm() {
      this.nom = '';
      this.prenom = '';
      this.username = '';
      this.user_function = null;
      this.email = '';
      this.step = 1;
    },

  },
}
</script>

