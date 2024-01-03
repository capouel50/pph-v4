<template>
  <q-form @submit.prevent="onSubmit">
    <div class="q-pa-sm row">
      <div class="q-gutter-sm col-md-12">
        <CustomInput
          v-model="email"
          label="E-mail"
          icon="mail"
          @update:focused="emailFocused = $event"
        />
        <div class="row">
          <div class="col-md-6">
            <CustomInput
              v-model="last_name"
              label="Nom"
              icon="portrait"
              @update:focused="last_nameFocused = $event"
            />
          </div>
          <div class="col-md-6">
            <CustomInput
              v-model="first_name"
              label="Prénom"
              icon="portrait"
              @update:focused="first_nameFocused = $event"
            />
          </div>

        </div>
        <div class="row">
          <div class="col-md-6">
            <CustomInput
              v-model="password1"
              label="Mot de passe"
              icon="password"
              @update:focused="password1Focused = $event"
            />
          </div>
          <div class="col-md-6">
            <CustomInput
              v-model="password2"
              label="Confirmation"
              icon="password"
              @update:focused="password2Focused = $event"
            />
          </div>
        </div>

        <!-- autres champs ici -->

        <div class="row justify-center q-mt-sm">
          <div class="col-md-10">
            <q-btn type="submit" class="q-mt-lg glossy full-width btn-grey-success-pph">
              <q-icon class="q-mx-sm" name="person_add"/>
              S'inscrire
            </q-btn>
          </div>
        </div>

        <div class="row q-pa-sm items-center">
          <div class="offset-2 col-md-3">
            <q-separator color="grey-8"/>
          </div>
          <p class="text-cyan-4 col-2 text-center q-mt-sm">Ou</p>
          <div class="col-md-3">
            <q-separator color="grey-8"/>
          </div>
        </div>

        <div class="row justify-center">
          <div class="col-md-10">
            <q-btn class="glossy full-width btn-grey-success-pph">
              <q-icon class="q-mr-sm" name="login"/>
              Se connecter
            </q-btn>
          </div>
        </div>

      </div>
    </div>
  </q-form>
</template>

<script>
import CustomInput from '../FormField/CustomInput.vue';

export default {
  components: {
    CustomInput
  },
  props: {
    register: {
      type: Function,
      required: true
    }
  },
  data() {
    return {
      email: '',
      first_name: '',
      last_name: '',
      password1: '',
      password2: '',
      emailFocused: false,
      first_nameFocused: false,
      last_nameFocused: false,
      password1Focused: false,
      password2Focused: false,
    }
  },
  methods: {
    onSubmit() {
      this.register({
        email: this.email,
        first_name: this.first_name,
        last_name: this.last_name,
        password1: this.password1,
        password2: this.password2
      });
    },
  }
}
</script>

