<template>
  <q-form @submit.prevent="onSubmit">
    <div class="q-pa-sm row">
      <div class="q-gutter-sm col-md-12">
        <q-input
          ref="emailInput"
          class="my-0"
          v-model="email"
          label="E-mail"
          color ='cyan-4'
          @mouseover="changeLabelColor('emailInput','#ffb74d')"
          @mouseleave="changeLabelColor('emailInput','')"
          @focus="onFocus('email','#4dd0e1')"
          @blur="onBlur('email')"
        >
          <template v-slot:before>
            <q-icon name="mail" color="cyan-4"/>
          </template>
        </q-input>
      <div class="row">
        <div class="col-md-6">
        <q-input
          ref="last_nameInput"
          class="my-0"
          v-model="last_name"
          label="Nom"
          color ='cyan-4'
          @mouseover="changeLabelColor('last_nameInput', '#ffb74d')"
          @mouseleave="changeLabelColor('last_nameInput', '')"
          @focus="onFocus('last_name', '#4dd0e1')"
          @blur="onBlur('last_name')"
        >
          <template v-slot:before>
            <q-icon name="portrait" color="cyan-4"/>
          </template>
        </q-input>
        </div>
        <div class="col-md-6">
        <q-input
          ref="first_nameInput"
          class="my-0"
          v-model="first_name"
          label="Prénom"
          color ='cyan-4'
          @mouseover="changeLabelColor('first_nameInput', '#ffb74d')"
          @mouseleave="changeLabelColor('first_nameInput', '')"
          @focus="onFocus('first_name', '#4dd0e1')"
          @blur="onBlur('first_name')"
        >
          <template v-slot:before>
            <q-icon name="portrait" color="cyan-4"/>
          </template>
        </q-input>
        </div>
      </div>
      <div class="row">
        <div class="col-md-6">
        <q-input
          ref="password1Input"
          class="my-0"
          v-model="password1"
          label="Mot de passe"
          type="password"
          color ='cyan-4'
          @mouseover="changeLabelColor('password1Input', '#ffb74d')"
          @mouseleave="changeLabelColor('password1Input', '')"
          @focus="onFocus('password1', '#4dd0e1')"
          @blur="onBlur('password1')"
        >
          <template v-slot:before>
            <q-icon name="password" color="cyan-4"/>
          </template>
        </q-input>
        </div>
        <div class="col-md-6">
        <q-input
          ref="password2Input"
          class="my-0"
          v-model="password2"
          label="Confirmation"
          type="password"
          color ='cyan-4'
          @mouseover="changeLabelColor('password2Input', '#ffb74d')"
          @mouseleave="changeLabelColor('password2Input', '')"
          @focus="onFocus('password2', '#4dd0e1')"
          @blur="onBlur('password2')"
        >
          <template v-slot:before>
            <q-icon name="password" color="cyan-4"/>
          </template>
        </q-input>
        </div>
      </div>
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
            <q-btn class="glossy full-width btn-grey-success-pph" @click="redirectToLogin">
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
export default {
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
      isEmailHovered: false,
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
    changeLabelColor(inputRef, color) {
      if (!this[inputRef.replace('Input', '')]) {
        this.$refs[inputRef].$el.querySelector('.q-field__label').style.color = color;
        }
    },
    redirectToLogin(){
      this.$router.push('/login');
    },
    onFocus(field, color) {
      this[`${field}Focused`] = true;
      this.changeLabelColor(`${field}Input`, color);
    },
    onBlur(field) {
      this[`${field}Focused`] = false;
    }
  }
}
</script>
