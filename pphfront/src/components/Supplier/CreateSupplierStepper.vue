<template>
  <q-form @submit.prevent="onSubmit" enctype="multipart/form-data" class="q-pa-md">
    <q-stepper
      v-model="step"
      class="bg-op-8"
      vertical
      done-color="cyan-4"
      active-color="orange-4"
      header-nav
      animated
    >
      <div class="text-cyan-4 q-mb-lg text-h5 text-center">Fiche fournisseur</div>
      <q-step
        :name="1"
        title="Identification"
        icon="info"
        :done="step > 1"
      >
        <div class="row">
            <q-input
              class="col-2"
              ref="nameInput"
              v-model="name"
              label="Nom"
              color ='cyan-4'
              @mouseover="changeLabelColor('nameInput','#ffb74d')"
              @mouseleave="changeLabelColor('nameInput','')"
              @focus="onFocus('name','#4dd0e1')"
              @blur="onBlur('name')"
            >
              <template v-slot:before>
                <q-icon name="forklift" color="cyan-4"/>
              </template>
            </q-input>
          </div>

          <q-stepper-navigation>
            <q-btn flat @click="step = 2" color="cyan-4" label="Suivant" class="hover-effect" />
          </q-stepper-navigation>
      </q-step>

        <q-step
        :name="2"
        title="Localisation"
        icon="vaccines"
        :done="step > 2"
      >
          <div class="row">
            <q-input
                ref="countryInput"
                class="col-2"
                v-model="country"
                label="Pays"
                color ='cyan-4'
                @mouseover="changeLabelColor('countryInput', '#ffb74d')"
                @mouseleave="changeLabelColor('countryInput', '')"
                @focus="onFocus('country', '#4dd0e1')"
                @blur="onBlur('country')"
              >
                <template v-slot:before>
                  <q-icon name="flag" color="cyan-4"/>
                </template>
              </q-input>
            </div>
            <div class="row">
            <q-input
              ref="addressInput"
              class="col-3"
              v-model="address"
              label="Adresse"
              color ='cyan-4'
              @mouseover="changeLabelColor('addressInput', '#ffb74d')"
              @mouseleave="changeLabelColor('addressInput', '')"
              @focus="onFocus('address', '#4dd0e1')"
              @blur="onBlur('address')"
            >
              <template v-slot:before>
                <q-icon name="mail" color="cyan-4"/>
              </template>
            </q-input>
              <q-input
                ref="postalInput"
                class="col-2 q-ml-md"
                v-model="postal"
                label="Code postal"
                color ='cyan-4'
                @mouseover="changeLabelColor('postalInput', '#ffb74d')"
                @mouseleave="changeLabelColor('postalInput', '')"
                @focus="onFocus('postal', '#4dd0e1')"
                @blur="onBlur('postal')"
              >
                <template v-slot:before>
                  <q-icon name="contact_mail" color="cyan-4"/>
                </template>
              </q-input>
            </div>
            <div class="row">
              <q-input
                ref="cityInput"
                class="col-3"
                v-model="city"
                label="Ville"
                color ='cyan-4'
                @mouseover="changeLabelColor('cityInput', '#ffb74d')"
                @mouseleave="changeLabelColor('cityInput', '')"
                @focus="onFocus('city', '#4dd0e1')"
                @blur="onBlur('city')"
              >
                <template v-slot:before>
                  <q-icon name="location_city" color="cyan-4"/>
                </template>
              </q-input>
            </div>

          <q-stepper-navigation>
          <q-btn flat @click="step = 3" color="cyan-4" label="Suivant" class="hover-effect"/>
          <q-btn flat @click="step = 1" color="cyan-4" label="Précédent" class="hover-effect q-ml-sm" />
        </q-stepper-navigation>
      </q-step>

      <q-step
        :name="3"
        title="Contact"
        icon="ac_unit"
        :done="step > 3"
      >
            <div class="row">
              <q-input
                ref="phoneInput"
                class="col-3"
                v-model="phone"
                label="Téléphone"
                color ='cyan-4'
                @mouseover="changeLabelColor('phoneInput','#ffb74d')"
                @mouseleave="changeLabelColor('phoneInput','')"
                @focus="onFocus('phone','#4dd0e1')"
                @blur="onBlur('phone')"
              >
                <template v-slot:before>
                  <q-icon name="phone" color="cyan-4"/>
                </template>
              </q-input>
            </div>
          <div class="row">

            <q-input
              ref="emailInput"
              class="col-3"
              v-model="email"
              type="email"
              label="E-mail de contact"
              color ='cyan-4'
              @mouseover="changeLabelColor('emailInput', '#ffb74d')"
              @mouseleave="changeLabelColor('emailInput', '')"
              @focus="onFocus('email', '#4dd0e1')"
              @blur="onBlur('email')"
            >
              <template v-slot:before>
                <q-icon name="mail" color="cyan-4"/>
              </template>
            </q-input>
            <q-input
              ref="siteInput"
              class="col-3 q-ml-md"
              v-model="site"
              type="url"
              label="Site"
              color ='cyan-4'
              @mouseover="changeLabelColor('siteInput', '#ffb74d')"
              @mouseleave="changeLabelColor('siteInput', '')"
              @focus="onFocus('site', '#4dd0e1')"
              @blur="onBlur('site')"
            >
              <template v-slot:before>
                <q-icon name="web" color="cyan-4"/>
              </template>
            </q-input>
          </div>

        <q-stepper-navigation>
          <q-btn flat @click="step = 4" color="cyan-4" label="Suivant" class="hover-effect"/>
          <q-btn flat @click="step = 2" color="cyan-4" label="Précédent" class="hover-effect q-ml-sm" />
        </q-stepper-navigation>
      </q-step>

      <q-step
        :name="4"
        title="Identifiants"
        icon="settings"
        :done="step > 4"
      >
          <div class="row">
            <q-input
              ref="user_codeInput"
              class="col-2"
              v-model="user_code"
              label="Code client"
              color ='cyan-4'
              @mouseover="changeLabelColor('user_codeInput', '#ffb74d')"
              @mouseleave="changeLabelColor('user_codeInput', '')"
              @focus="onFocus('user_code', '#4dd0e1')"
              @blur="onBlur('user_code')"
            >
              <template v-slot:before>
                <q-icon name="sell" color="cyan-4"/>
              </template>
            </q-input>
            <q-input
              ref="passwordInput"
              class="col-2 q-ml-md"
              v-model="password"
              label="Mot de passe"
              color ='cyan-4'
              @mouseover="changeLabelColor('passwordInput', '#ffb74d')"
              @mouseleave="changeLabelColor('passwordInput', '')"
              @focus="onFocus('password', '#4dd0e1')"
              @blur="onBlur('password')"
            >
              <template v-slot:before>
                <q-icon name="password" color="cyan-4"/>
              </template>
            </q-input>
          </div>

        <q-stepper-navigation>
          <q-btn flat @click="step = 5" color="cyan-4" label="Suivant" class="hover-effect"/>
          <q-btn flat @click="step = 3" color="cyan-4" label="Précédent" class="hover-effect q-ml-sm" />
        </q-stepper-navigation>
      </q-step>

      <q-step
        :name="5"
        title="Logo"
        icon="list_alt"
        :done="step > 5"
      >
          <div class="row">
            <q-file
              ref="logoInput"
              type="file"
              class="col-3"
              v-model="logo"
              accept=".jpg,.jpeg,.png,.gif"
              label="Choisir un logo"
              color ='cyan-4'
              @mouseover="changeLabelColor('logoInput', '#ffb74d')"
              @mouseleave="changeLabelColor('logoInput', '')"
              @focus="onFocus('logo', '#4dd0e1')"
              @blur="onBlur('logo')"
              @input="handleFileChange"
            >
              <template v-slot:before>
                <q-icon name="branding_watermark" color="cyan-4"/>
              </template>
            </q-file>
          </div>

        <q-stepper-navigation>
          <q-btn flat @click="step = 7" color="cyan-4" label="Précédent" class="hover-effect q-ml-sm" />
        </q-stepper-navigation>
      </q-step>

    <div class="row justify-center">
      <q-btn-group>
        <q-btn flat type="submit" color="green-4" class="btn-flat-success-pph">
          <q-icon class="q-mx-sm" name="library_add"/>
          Enregistrer
        </q-btn>
      </q-btn-group>
    </div>

    </q-stepper>
  </q-form>
</template>

<script>
import { mapActions, mapGetters } from 'vuex';

export default {
  data() {
    return {
      step: 1,
      supplierId: this.$route.params.id,
      name: '',
      postal: '',
      address: '',
      city: '',
      country: '',
      logo: null,
      phone: '',
      email: '',
      site: '',
      user_code: '',
      password: '',
      is_activate: true,
      nameFocused: false,
      postalFocused: false,
      addressFocused: false,
      cityFocused: false,
      countryFocused: false,
      logoFocused: false,
      phoneFocused: false,
      emailFocused: false,
      siteFocused: false,
      user_codeFocused: false,
      passwordFocused: false,
      isEmailHovered: false,
      errorMessage: null,  // Pour gérer les erreurs
    };
  },
  methods: {
    ...mapActions('suppliers', ['addSupplier']),

    async onSubmit() {
      const formData = new FormData();
      formData.append('name', this.name);
      formData.append('postal', this.postal);
      formData.append('address', this.address);
      formData.append('city', this.city);
      formData.append('country', this.country);
      if (this.logo) {
        formData.append('logo', this.logo);
      }
      formData.append('phone', this.phone);
      formData.append('site', this.site);
      formData.append('email', this.email);
      formData.append('user_code', this.user_code);
      formData.append('password', this.password);
      formData.append('is_activate', this.is_activate);

      try {
        await this.addSupplier(formData);
        this.$emit('supplier-added-successfully');
        this.resetForm();
      } catch (error) {
        console.error("Error adding supplier:", error);
      }
    },

    resetForm() {
      this.name = '';
      this.postal = '';
      this.address = '';
      this.city = '';
      this.country = '';
      this.logo = null;
      this.phone = '';
      this.email = '';
      this.site = '';
      this.user_code = '';
      this.password = '';
      this.is_activate = true;
    },

    changeLabelColor(inputRef, color) {
      if (!this[inputRef.replace('Input', '')]) {
        this.$refs[inputRef].$el.querySelector('.q-field__label').style.color = color;
      }
    },

    redirectToLogin() {
      this.$router.push('/login');
    },

    onFocus(field, color) {
      this[`${field}Focused`] = true;
      this.changeLabelColor(`${field}Input`, color);
    },

    onBlur(field) {
      this[`${field}Focused`] = false;
    },

    handleFileChange(file) {
      this.logo = file;
    },
  },

  computed: {
    ...mapGetters('suppliers', ['currentSupplier']),
  },

  watch: {
    currentSupplier(newVal) {
      if (newVal) {
        this.name = newVal.name;
        this.address = newVal.address;
        this.postal = newVal.postal;
        this.city = newVal.city;
        this.country = newVal.country;
        this.phone = newVal.phone;
        this.site = newVal.site;
        this.email = newVal.email;
        this.user_code = newVal.user_code;
        this.password = newVal.password;
        this.logo = newVal.logo;
      }
    },
  },
};

</script>

