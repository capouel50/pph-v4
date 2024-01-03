<template>
  <q-form @submit.prevent="onSubmit">
    <div class="q-pa-sm row">
      <div class="q-gutter-sm col-md-12">
        <q-input
          ref="emailInput"
          class="my-0"
          v-model="email"
          label="E-mail"
          color="cyan-4"
          @mouseover="changeLabelColor('emailInput','#ffb74d')"
          @mouseleave="changeLabelColor('emailInput','')"
          @focus="onFocus('email', '#4dd0e1')"
          @blur="onBlur('email')"
        >
          <template v-slot:before>
            <q-icon name="portrait" color="cyan-4"/>
          </template>
        </q-input>

      <div class="row justify-center q-mt-sm">
        <div class="col-md-10">
          <q-btn type="submit" class="q-mt-lg glossy full-width btn-grey-primary-pph">
            <q-icon class="q-mx-sm" name="restart_alt"/>
            Réinitialiser
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
  data() {
    return {
      email: '',
      emailFocused: false,
    }
  },
  methods: {
    onSubmit() {
      this.$emit('submit', {
        email: this.email
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