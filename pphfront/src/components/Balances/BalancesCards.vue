<template>
  <q-page >
    <div class="row justify-center">
      <div class="col-md-12">
        <div class="row q-mx-sm q-mt-sm">
          <div class="col-3">
            <div class="row">
              <q-fab glossy class="glossy btn-cyan-pph" icon="add_box" direction="right">
                <router-link :to="{ name: 'CreateBalancesSupplier' }">
                  <q-fab-action flat color="cyan-4" icon="forklift" class="hover-effect">
                    <q-tooltip>Fournisseur</q-tooltip>
                  </q-fab-action>
                </router-link>
                <router-link :to="{ name: 'CreateBalances' }">
                  <q-fab-action flat color="cyan-4" icon="balance" class="hover-effect">
                    <q-tooltip>Balance</q-tooltip>
                  </q-fab-action>
                </router-link>
              </q-fab>
            </div>
          </div>
          <div class="col-6 q-mt-md text-cyan-4 text-h6">
            <div class="row justify-center">
            {{ countBalances }} balances référencées
            </div>
          </div>
          <div class="col-2 offset-1">
            <q-input
                ref="searchInput"
                v-model="searchQuery"
                label="Recherche..."
                @input="filterBalances"
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
          <div class="col-12 justify-center">
            <div class="row justify-start">
              <div class="col-2 q-pa-sm" v-for="balance in filteredBalances" :key="balance.id">
                <q-card bordered
                        class="card-maxi justify-center items-center text-center relative"
                        :class="{ 'bd-red-4': !balance.is_activate}"
                        @click.stop="redirectToLink(balance.id)"
                >
                  <div class="card-content">
                    <q-img class="logo-card-mini"
                           src="../../assets/img/blanc.jpg"
                           loading="lazy"
                           spinner-color="red-4"
                           :alt="balance.nom">
                      <div class="absolute-top hover-effect q-my-none" :class="{ 'text-cyan-1': balance.is_activate, 'text-red-4': !balance.is_activate }">
                        <div>{{ balance.nom }}</div>
                        <div>{{ balance.modele }}</div>
                        <div>
                          <font-awesome-icon v-if="(new Date(balance.prochaine) - new Date(balance.calibration)) < 30 * 24 * 60 * 60 * 1000"
                                             icon="fa-solid fa-triangle-exclamation"
                                             beat-fade
                                             size="fa-xs"
                                             style="color: #e57373;"
                          />
                          Prochaine calibration :
                        </div>
                        <div>
                          {{ balance.prochaineFormatted }}
                        </div>
                      </div>
                      <template v-slot:loading>
                        <q-spinner-rings color="red-4" />
                      </template>
                    </q-img>
                    <q-btn flat color="white" class="absolute-top-right hover-effect q-pa-none q-ma-none"
                           icon="more_vert" @click.stop="toggleMenu(balance.id)"
                    />
                    <q-menu fit anchor="top right" self="bottom middle" v-model="showMenu[balance.id]">
                      <q-list style="min-width: 100px">
                        <q-item clickable v-close-popup @click.stop="toggleActivation({ balanceId: balance.id, isActive: balance.is_activate, balanceName: balance.nom })">
                          <q-item-section :class="{ 'hover-effect-warning': balance.is_activate, 'hover-effect-success': !balance.is_activate }">
                            {{ balance.is_activate ? 'Désactiver' : 'Activer' }}
                          </q-item-section>
                        </q-item>
                      </q-list>
                    </q-menu>
                  </div>

                  <q-btn-group class="absolute-bottom-right q-pa-none q-ma-none">
                    <q-btn
                      class="hover-effect"
                      :color="expanded[balance.id] ? 'orange-4' : 'cyan-4'"
                      round
                      flat
                      dense
                      icon="info"
                      size="sm"
                      @click.stop="toggleInfo(balance.id)"
                    />
                  </q-btn-group>

                  <q-menu fit anchor="bottom right" self="top middle" v-model="expanded[balance.id]">
                    <q-list style="min-width: 100px">
                      <q-item class="justify-center">
                        <q-item-section avatar class="text-cyan-4">
                          Détails
                        </q-item-section>
                      </q-item>
                      <q-item>
                        <q-item-section avatar class="text-orange-4">
                          Fournisseur :
                        </q-item-section>
                        <q-item-section class="text-grey-7">
                          {{ balance.fabricant.name }}
                        </q-item-section>
                      </q-item>
                      <q-item>
                        <q-item-section avatar class="text-orange-4">
                          Calibration :
                        </q-item-section>
                        <q-item-section class="text-grey-7">
                          {{ balance.calibration }}
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
import {FontAwesomeIcon} from "@fortawesome/vue-fontawesome";
import {formatDate} from '@/utils/helpers'


export default {
  name: "MatieresCards",
  components: {
    FontAwesomeIcon,
  },

  data() {
    return {
      searchQuery: '',
      balanceId: '',
    };
  },

  computed: {
    ...mapGetters('balances', ['allBalances', 'showMenu', 'expanded']),

    countBalances() {
      return Array.isArray(this.filteredBalances) ? this.filteredBalances.length : 0;
    },

    filteredBalances() {
      if (!Array.isArray(this.allBalances)) {
        return [];
      }

      if (this.searchQuery) {
        return this.allBalances.filter(balance =>
            balance.nom.toLowerCase().includes(this.searchQuery.toLowerCase()) &&
            balance.fabricant.name.toLowerCase().includes(this.searchQuery.toLowerCase())
        );
      }

      return this.allBalances.map(balance => {
        balance.prochaineFormatted = formatDate(new Date(balance.prochaine));
        return balance;  // Return modified balance object
      });
    },
  },

  async created() {
    await this.loadBalances();
    console.log('allBalance', this.allBalances);
  },

  methods: {
    ...mapActions('balances', ['loadBalances', 'toggleMenu', 'toggleInfo', 'toggleActivation']),

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
      this.$router.push(`/modifier-balances/${id}`);
    }

  }
};
</script>



