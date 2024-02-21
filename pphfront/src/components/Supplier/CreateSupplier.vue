<template>
  <q-form class="q-pa-md">
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
          <q-btn flat @click="step = 1" color="cyan-4" label="Précédent" class="hover-effect q-ml-sm" />
          <q-btn flat @click="step = 3" color="cyan-4" label="Suivant" class="hover-effect"/>
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
          <q-btn flat @click="step = 2" color="cyan-4" label="Précédent" class="hover-effect q-ml-sm" />
          <q-btn flat @click="step = 4" color="cyan-4" label="Suivant" class="hover-effect"/>
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
          <q-btn flat @click="step = 3" color="cyan-4" label="Précédent" class="hover-effect q-ml-sm" />
          <q-btn flat @click="step = 5" color="cyan-4" label="Terminer" class="hover-effect"/>
        </q-stepper-navigation>
      </q-step>

    <div class="row justify-center">
      <q-btn-group>
        <q-btn flat @click="callSubmit" color="green-4" class="btn-flat-success-pph">
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
      supplierId: null,
      supplier: [],
      name: '',
      postal: '',
      address: '',
      city: '',
      country: '',
      phone: '',
      email: '',
      site: '',
      user_code: '',
      password: '',
      is_activate: true,
    };
  },

  async mounted() {
    this.supplierId = Number(this.$route.params.id);

    await Promise.all([
      this.loadSuppliers(),
    ]);

    if (this.supplierId) {
      this.supplier = this.allSuppliers.find(supplier => supplier.id === this.supplierId);
      this.name = this.supplier.name;
      this.postal = this.supplier.postal;
      this.address = this.supplier.address;
      this.city = this.supplier.city;
      this.country =this. supplier.country;
      this.phone = this.supplier.phone;
      this.email = this.supplier.email;
      this.site = this.supplier.site;
      this.user_code = this.supplier.user_code;
      this.password = this.supplier.password;
    }
  },

  computed: {
    ...mapGetters('suppliers', ['allSuppliers']),
  },

  methods: {
    ...mapActions('suppliers', ['addSupplier', 'loadSuppliers', 'updateSupplier']),

    async callSubmit() {
      const formData = {
        name: this.name,
        postal: this.postal,
        address: this.address,
        city: this.city,
        country: this.country,
        phone: this.phone,
        email: this.email,
        site: this.site,
        user_code: this.user_code,
        password: this.password,
      };
      if(!this.supplierId) {
        this.onSubmit(formData);
      }else{
        this.updateSubmit(formData)
      }
    },
    async updateSubmit(formData) {
      const id = this.supplierId;
      await this.updateSupplier({id, formData});
      this.resetForm();
    },

    async onSubmit(formData) {
      try {
        await this.addSupplier(formData);
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
    },

    changeLabelColor(inputRef, color) {
      if (!this[inputRef.replace('Input', '')]) {
        this.$refs[inputRef].$el.querySelector('.q-field__label').style.color = color;
      }
    },

    onFocus(field, color) {
      this[`${field}Focused`] = true;
      this.changeLabelColor(`${field}Input`, color);
    },

    onBlur(field) {
      this[`${field}Focused`] = false;
    },

  },

};

</script>

