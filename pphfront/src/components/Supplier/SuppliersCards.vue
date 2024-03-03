<template>
  <q-page>
    <div class="row justify-center">
      <div class="col-md-12">
        <div class="row q-mx-sm">
          <div class="col-3 q-mt-md">
            <router-link to="/supplier/">
              <q-btn round class="glossy btn-cyan-pph" icon="add_box"/>
            </router-link>
          </div>
          <div class="col-6 q-mt-md text-cyan-4 text-h6">
            <div class="row justify-center">
            {{ countSuppliers }} fournisseurs référencées
            </div>
          </div>
          <div class="col-2 offset-1 q-mt-sm">
            <q-input
                ref="searchInput"
                v-model="searchQuery"
                label="Recherche..."
                @input="filterSuppliers"
                color="cyan-4"
                @mouseover="changeLabelColor('searchInput', '#ffb74d')"
                @mouseleave="changeLabelColor('searchInput', '')"
                @focus="onFocus('searchQuery', '#4dd0e1')"
                @blur="onBlur('searchQuery')"
            >
              <template v-slot:append>
                <q-icon name="search" color="cyan-4"/>
              </template>
            </q-input>
          </div>
        </div>
        <div class="row q-mt-sm">
          <div class="col col-12 justify-center">
            <div class="row justify-start">
              <div class="col-1 q-pa-sm" v-for="supplier in filteredSuppliers" :key="supplier.id" @click="redirectToLink(supplier.id)">
                <q-card bordered class="card-mini justify-center items-center text-center relative" :class="{ 'bd-red-4': !supplier.is_activate}">
                  <div @click="redirectToLink(supplier.id)" class="card-content">
                    <q-img
                        class="logo-card-mini"
                        src="@/assets/img/blanc.jpg"
                        loading="lazy"
                        spinner-color="red-4"
                        :alt="supplier.name">
                      <q-icon
                          name="factory"
                          size="md"
                          color="cyan-4"
                          class="icon-background"
                      />
                      <div class="absolute-top hover-effect q-my-none" :class="{ 'text-cyan-1': supplier.is_activate, 'text-red-4': !supplier.is_activate }">
                        {{ supplier.name }}
                      </div>
                      <template v-slot:loading>
                        <q-spinner-rings color="red-4" />
                      </template>
                    </q-img>
                    <q-btn flat color="white" class="absolute-top-right hover-effect q-pa-none q-ma-none" icon="more_vert" @click.stop="toggleMenu(supplier.id)" />
                    <q-menu fit anchor="top right" self="bottom middle" v-model="showMenu[supplier.id]">
                      <q-list style="min-width: 100px">
                        <q-item clickable v-close-popup @click.stop="deleteSupplier(supplier.id)">
                          <q-item-section class="hover-effect">Supprimer</q-item-section>
                        </q-item>
                        <q-item clickable v-close-popup @click.stop="toggleActivation({ supplierId: supplier.id, isActive: supplier.is_activate })">
                          <q-item-section class="hover-effect">
                            {{ supplier.is_activate ? 'Désactiver' : 'Activer' }}
                          </q-item-section>
                        </q-item>
                      </q-list>
                    </q-menu>
                  </div>
                  <q-btn
                    class="absolute-bottom-right hover-effect q-pa-none q-ma-none"
                    color="cyan-4"
                    round
                    flat
                    dense
                    icon="info"
                    size="xs"
                    @click.stop="toggleInfo(supplier.id)"
                  />
                  <q-menu fit anchor="bottom right" self="top middle" v-model="expanded[supplier.id]">
                    <q-list style="min-width: 100px">
                      <q-item v-if="supplier.phone">
                        <q-item-section avatar class="text-cyan-4">
                          Téléphone :
                        </q-item-section>
                        <q-item-section class="text-grey-7">
                          {{ supplier.phone }}
                        </q-item-section>
                      </q-item>
                      <q-item v-if="supplier.email">
                        <q-item-section avatar class="text-cyan-4">
                          E-mail :
                        </q-item-section>
                        <q-item-section class="text-grey-7">
                          {{ supplier.email }}
                        </q-item-section>
                      </q-item>
                      <q-item clickable class="hover-effect" v-if="supplier.site">
                        <q-item-section avatar class="text-cyan-4">
                          Site :
                        </q-item-section>
                        <a :href="supplier.site" target="_blank" rel="noopener noreferrer" class="pph-link">
                          <q-item-section class=" row items-center text-grey-7 hover-effect">
                            {{ supplier.site }}
                          </q-item-section>
                        </a>
                      </q-item>
                      <q-item v-if="supplier.user_code">
                        <q-item-section avatar class="text-cyan-4">
                          Code utilisateur :
                        </q-item-section>
                        <q-item-section class="text-grey-7">
                          {{ supplier.user_code }}
                        </q-item-section>
                      </q-item>
                      <q-item v-if="supplier.password">
                        <q-item-section avatar class="text-cyan-4">
                          Mot de passe :
                        </q-item-section>
                        <q-item-section class="text-grey-7">
                          {{ supplier.password }}
                        </q-item-section>
                      </q-item>
                    </q-list>
                  </q-menu>
                </q-card>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </q-page>
</template>

<script>
import { mapActions, mapGetters } from 'vuex';

export default {
  name: "SuppliersCards",

  data() {
    return {
      searchQuery: '',
    };
  },

  computed: {
    ...mapGetters('suppliers', ['allSuppliers', 'showMenu', 'expanded']),

    countSuppliers() {
      return Array.isArray(this.filteredSuppliers) ? this.filteredSuppliers.length : 0;
    },

    filteredSuppliers() {
      if (this.searchQuery) {
        return this.allSuppliers.filter(supplier =>
          supplier.name.toLowerCase().startsWith(this.searchQuery.toLowerCase())
        );
      }
      return this.allSuppliers;
    }
  },

  created() {
    this.loadSuppliers();
    console.log(this.allSuppliers);
  },

  methods: {
    ...mapActions('suppliers', ['loadSuppliers', 'toggleActivation', 'deleteSupplier', 'toggleMenu', 'toggleInfo']),

    filterSuppliers() {
    if (!this.searchQuery) {
      return this.allSuppliers;
    } else {
      return this.allSuppliers.filter(supplier => {
        return supplier.name.toLowerCase().startsWith(this.searchQuery.toLowerCase());
      });
    }
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

    redirectToLink(id) {
      this.$router.push(`/supplier/${id}`);
    }
  }
};
</script>



