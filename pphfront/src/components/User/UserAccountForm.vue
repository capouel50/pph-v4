<template>
  <q-form @submit.prevent="onSubmit" enctype="multipart/form-data">
    <div class="row justify-center items-center">
      <q-card class="col-6 shadow-5" style="background-color: #e6e5e8;">
        <q-card-section class="q-mb-lg justify-center row">
          <CustomInput class="col-4"
            :inputModel="last_name"
            @update:inputModel="value => last_name = value"
            label="Nom"
            inputRef="last_nameInput"
            iconName="portrait"
            modelName="last_name"
          />

          <CustomInput class="col-4 offset-2"
            :inputModel="first_name"
            @update:inputModel="value => first_name = value"
            label="Prénom"
            inputRef="first_nameInput"
            iconName="portrait"
            modelName="first_name"
          />
        </q-card-section>

        <q-card-section class="q-mb-lg justify-center row">
          <CustomInput class="col-4"
            :inputModel="email"
            @update:inputModel="value => email = value"
            label="E-mail"
            inputRef="emailInput"
            iconName="email"
            modelName="email"
          />

          <CustomInput class="col-4 offset-2"
            :inputModel="user_name"
            @update:inputModel="value => user_name = value"
            label="Nom d'utilisateur"
            inputRef="usernameInput"
            iconName="portrait"
            modelName="username"
          />
        </q-card-section>

        <q-card-section class="q-mb-lg row">
          <CustomSelect class="col-4 offset-1"
            label="Fonction"
            :options="userFunctions"
            inputRef="dropDownInput"
            inputName="dropDown"
            iconName="badge"
            @input="onSelectChange"
          />
        </q-card-section>

      </q-card>
    </div>

    <div class="row justify-center q-my-md">
      <div class="col-2">
        <q-btn type="submit" class="q-mt-lg glossy full-width btn-grey-success-pph">
          <q-icon class="q-mx-sm" name="library_add"/>
          Enregistrer
        </q-btn>
      </div>
    </div>

  </q-form>
</template>

<script>
import { mapGetters } from 'vuex';
import CustomInput from '../FormField/CustomInput.vue';
import CustomSelect from '../FormField/CustomSelect.vue';
import api from '../../../api';

export default {
  components: {
    CustomInput,
    CustomSelect
  },
  props: {
  userData: Object
  },
  data() {
    return {
      last_name: this.userData.lastName,
      first_name: this.userData.firstName,
      email: this.userData.email,
      username: this.userData.username,
      function: this.userData.function,
      // ...
    };
  },
  computed: {
    ...mapGetters({
      user: 'user'
    })
  },
  watch: {
    user(newUser) {
      this.last_name = newUser.lastName;
      this.first_name = newUser.firstName;
      this.email = newUser.email;
      this.username = newUser.username;
      this.function = newUser.function;
    }
  },
  mounted() {
  api.get('/PPH/user-functions/') // Remplacez par l'URL exacte de votre API
    .then(response => {
      console.log(response.data);
      this.userFunctions = response.data.map(item => ({
        label: item.title, // 'title' correspond à la propriété dans votre modèle backend
        value: item.title
      }));
    })
    .catch(error => {
      console.error('Erreur lors de la récupération des fonctions utilisateur:', error);
    });
  },
  methods: {
    onSubmit() {
    // Mettez à jour les données de l'utilisateur dans votre base de données backend
    // Puis mettez à jour le store avec les nouvelles informations
      this.$store.commit('SET_USER_DATA', {
        lastName: this.last_name,
        firstName: this.first_name,
        email: this.email,
        userName: this.username,
        function: this.function
      });
    }
  }
};
</script>
