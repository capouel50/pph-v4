<template>
  <q-page>
    <div class="row justify-center">
      <div class="col-md-12">
        <div class="row q-mx-sm">
          <div class="col-1 q-mt-sm">
            <router-link to="/formules/">
              <q-btn round class="glossy btn-grey-primary-pph" icon="add"/>
            </router-link>
          </div>
          <div class="col-2 offset-9">
            <q-input
                ref="searchInput"
                v-model="searchQuery"
                label="Recherche..."
                @input="filterFormules"
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
              <div class="col-2 q-pa-sm" v-for="formule in filteredFormules" :key="formule.id" @click="redirectToLink(formule.id)">
                <q-card bordered class="card-maxi justify-center items-center text-center relative" :class="{ 'bd-red-4': !formule.is_activate}">
                  <div @click="redirectToLink(formule.id)" class="card-content">
                    <q-img class="logo-card-mini" src="../../assets/img/blanc.jpg" :alt="formule.nom">
                      <q-icon
                          v-if="formule.is_valid"
                          name="done_all"
                          color="green-4"
                          class="icon-background"
                      />
                      <q-icon
                          v-if="!formule.is_valid"
                          name="remove_done"
                          color="red-4"
                          class="icon-background"
                      />
                      <div class="absolute-top hover-effect q-my-none" :class="{ 'text-cyan-1': formule.is_activate, 'text-red-4': !formule.is_activate }">
                        <div>{{ formule.nom }}</div>
                        <div>{{ formule.type.nom }}</div>
                      </div>
                    </q-img>
                    <q-btn flat color="white" class="absolute-top-right hover-effect q-pa-none q-ma-none" icon="more_vert" @click.stop="toggleMenu(formule.id)" />
                    <q-menu fit anchor="top right" self="bottom middle" v-model="showMenu[formule.id]">
                      <q-list style="min-width: 100px">
                        <q-item clickable v-close-popup @click.stop="toggleActivation({ formuleId: formule.id, isActive: formule.is_activate })">
                          <q-item-section class="hover-effect">
                            {{ formule.is_activate ? 'Désactiver' : 'Activer' }}
                          </q-item-section>
                        </q-item>
                      </q-list>
                    </q-menu>
                  </div>
                  <div class="absolute-bottom-left">
                    <div class="row">
                      <font-awesome-icon v-if="formule.froid" fade icon="fa-solid fa-snowflake" class="q-ml-xs q-mb-xs fa-2x" style="color: #4dd0e1;" />
                      <q-icon v-if="formule.agiter" name="waving_hand" class="q-ml-xs q-mb-xs" color="cyan-4" size="md"/>
                      <q-icon v-if="formule.lumiere" name="light_mode" class="q-ml-xs q-mb-xs" color="red-4" size="md"/>
                    </div>
                  </div>
                  <q-btn-group class="absolute-bottom-right q-pa-none q-ma-none">
                    <q-btn
                       class="q-pa-none hover-effect"
                       flat
                       color="cyan-4"
                       icon="bar_chart"
                    />
                    <q-btn
                       class="q-pa-none hover-effect"
                       flat
                       color="cyan-4"
                       icon="list"
                       @click.stop="toggleCompo(formule.id)"
                    />
                    <q-btn
                       class="q-pa-none hover-effect"
                       flat
                       color="cyan-4"
                       icon="settings"
                       @click.stop="toggleSettings(formule.id)"
                    />
                    <q-btn
                      class="hover-effect"
                      color="cyan-4"
                      round
                      flat
                      dense
                      icon="info"
                      @click.stop="toggleInfo(formule.id)"
                    />
                  </q-btn-group>
                  <q-menu fit anchor="bottom right" self="top middle" v-model="expanded[formule.id]">
                    <q-list style="min-width: 100px">
                      <q-item v-if="formule.voie">
                        <q-item-section avatar class="text-cyan-4">
                          Voie :
                        </q-item-section>
                        <q-item-section class="text-grey-7">
                          {{ formule.voie.nom }}
                        </q-item-section>
                      </q-item>
                      <q-item v-if="formule.liste">
                        <q-item-section avatar class="text-cyan-4">
                          Liste :
                        </q-item-section>
                        <q-item-section class="text-grey-7">
                          {{ formule.liste.nom }} €
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
  name: "formulaCards",

  data() {
    return {
      searchQuery: '',
    };
  },

  computed: {
    ...mapGetters('formules', ['allFormules', 'showMenu', 'expanded']),

    filteredFormules() {
      if (this.searchQuery) {
        return this.allFormules.filter(formule =>
          formule.nom.toLowerCase().startsWith(this.searchQuery.toLowerCase())
        );
      }
      return this.allFormules;
    }
  },

  created() {
    this.loadFormules();
    console.log(this.allFormules);
  },

  methods: {
    ...mapActions('formules', ['loadFormules', 'toggleActivation', 'validFormule', 'toggleInfo', 'toggleMenu']),

    filterFormules() {
    if (!this.searchQuery) {
      return this.allFormules;
    } else {
      return this.allFormules.filter(formule => {
        return formule.nom.toLowerCase().startsWith(this.searchQuery.toLowerCase());
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



