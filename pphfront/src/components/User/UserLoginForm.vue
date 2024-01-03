<template>
  <q-form @submit.prevent="onSubmit">
    <div class="q-pa-sm row">
      <div class="q-gutter-sm col-md-12">
        <q-input
          ref="usernameInput"
          class="my-0"
          v-model="username"
          label="Nom d'utilisateur"
          color="cyan-4"
          @mouseover="changeLabelColor('usernameInput','#ffb74d')"
          @mouseleave="changeLabelColor('usernameInput','')"
          @focus="onFocus('username', '#4dd0e1')"
          @blur="onBlur('username')"
        >
          <template v-slot:before>
            <q-icon name="portrait" color="cyan-4"/>
          </template>
        </q-input>
      <div class="row">
        <div class="col-md-12">
        <q-input
          ref="password1Input"
          class="my-0"
          v-model="password1"
          color="cyan-4"
          label="Mot de passe"
          type="password"
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
      </div>
      <div class="row justify-center q-mt-sm">
        <div class="col-md-10">
          <q-btn type="submit" class="q-mt-lg glossy full-width btn-grey-success-pph">
            <q-icon class="q-mx-sm" name="login" v-if="!isLoggedIn" />
            Se connecter
          </q-btn>
        </div>
        <div class="row justify-center q-mt-sm text-cyan-4 pph-link">
          <router-link class="q-mx-md text-cyan-4 hover-effect pph-link" to="/password-reset">Mot de passe oublié ?</router-link>
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
            <q-btn class="glossy full-width btn-grey-success-pph" @click="redirectToRegister">
              <q-icon class="q-mr-sm" name="person_add"/>
              S'inscrire
            </q-btn>
          </div>
        </div>
      </div>
    </div>
  </q-form>
</template>

<script>
export default {
  data() {
    return {
      username: '',
      password1: '',
      usernameFocused: false,
      passwordFocused: false,
    }
  },
  methods: {
    onSubmit() {
      this.$emit('submit', {
        username: this.username,
        password: this.password1
      });
    },
    changeLabelColor(inputRef, color) {
      if (!this[inputRef.replace('Input', '')]) {
        this.$refs[inputRef].$el.querySelector('.q-field__label').style.color = color;
      }
    },
    redirectToRegister(){
      this.$router.push('/Register');
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


