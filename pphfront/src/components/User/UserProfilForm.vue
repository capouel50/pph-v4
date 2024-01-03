<template>
  <q-form @submit.prevent="handleSubmit" enctype="multipart/form-data">
    <div class="row justify-center items-center">
      <q-card class="col-6 shadow-5" style="background-color: #e6e5e8;">
        <q-card-section class="q-mb-lg justify-center row">
          <CustomInput class="col-4"
            :inputModel="userFormData.last_name"
            @update:inputModel="updateField('userFormData', 'last_name', $event)"
            label="Nom"
            inputRef="last_nameRef"
            iconName="portrait"
            modelName="last_name"
          />

          <CustomInput class="col-4 offset-2"
            :inputModel="userFormData.first_name"
            @update:inputModel="updateField('userFormData', 'first_name', $event)"
            label="Prénom"
            inputRef="first_nameRef"
            iconName="portrait"
            modelName="first_name"
          />
        </q-card-section>

        <q-card-section class="q-mb-lg justify-center row">
          <CustomInput class="col-4"
            :inputModel="userFormData.email"
            @update:inputModel="updateField('userFormData', 'email', $event)"
            label="E-mail"
            inputRef="emailRef"
            iconName="email"
            modelName="email"
          />

          <CustomInput class="col-4 offset-2"
            :inputModel="userFormData.user_name"
            @update:inputModel="updateField('userFormData', 'user_name', $event)"
            label="Nom d'utilisateur"
            inputRef="usernameRef"
            iconName="portrait"
            modelName="username"
          />
        </q-card-section>

        <q-card-section class="q-mb-lg row">
          <CustomSelect class="col-4 offset-1"
            label="Fonction"
            :options="userFunctions"
            inputRef="dropdownInput"
            inputName="dropdown"
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
import CustomInput from '../FormField/CustomInput.vue';
import CustomSelect from '../FormField/CustomSelect.vue';
import { mapState, mapActions } from 'vuex';
import api from '../../../api';

export default {
  components: {
    CustomInput,
    CustomSelect
  },
  data() {
    return {
      userFunctions: [],
    };
  },
  computed: {
    ...mapState('forms', ['userFormData'])
  },
  mounted() {
  api.get('/PPH/user-functions/')
    .then(response => {
      console.log(response.data);
      this.userFunctions = response.data.map(item => ({
        label: item.title,
        value: item.title
      }));
    })
    .catch(error => {
      console.error('Erreur lors de la récupération des fonctions utilisateur:', error);
    });
  },
  methods: {
    ...mapActions('forms', ['updateField']),

    async handleSubmit() {
      try {
        // Lancer la requête API pour soumettre les données du formulaire
        const response = await api.post('PPH/user/update/', this.userFormData);

        // Gérer la réponse API ici
        console.log('Réponse API:', response.data);

        // Afficher une notification de succès
        this.$store.dispatch('notifications/showNotification', {
          message: 'Soumission réussie',
          type: 'success'
        });

        // Réinitialiser le formulaire si nécessaire
        this.userFormData = {
          email: '',
          password: ''
          // autres champs
        };

      } catch (error) {
        // Gérer les erreurs ici
        console.error('Erreur lors de la soumission du formulaire:', error);

        // Afficher une notification d'erreur
        this.$store.dispatch('notifications/showNotification', {
          message: 'Erreur lors de la soumission du formulaire',
          type: 'error'
        });

        // Mettre à jour le state d'erreur
        this.$store.commit('errorModule/SET_ERROR', error.response?.data?.detail || 'Une erreur est survenue.');
      }
    }
  }
};
</script>
