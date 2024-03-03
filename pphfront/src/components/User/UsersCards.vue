<template>
  <q-page>
    <div class="row justify-center">
      <div class="col-md-12">
        <div class="row">
          <div class="col-1 q-mx-sm q-mt-sm">
            <router-link to="/user/">
              <q-btn round class="btn-cyan-pph" icon="add"/>
            </router-link>
          </div>
        </div>
        <div class="row q-mt-sm">
          <div class="col col-12 justify-center">
            <div class="row justify-start">
              <div class="col-1 q-pa-sm" v-for="user in allUsers" :key="user.id" @click="redirectToLink(user.id)">
                <q-card bordered class="card-mini justify-center items-center text-center relative" :class="{ 'bd-red-4': !user.is_active}">
                  <div @click="redirectToLink(user.id)" class="card-content">
                    <q-img class="logo-card-mini"
                           :src="user.function.logo"
                           :alt="user.function.title"
                           loading="lazy"
                           spinner-color="red-4"
                    >
                      <div class="absolute-top hover-effect q-my-none text-no-wrap" :class="{ 'text-cyan-1': user.is_active, 'text-red-4': !user.is_active }">
                        {{ user.last_name }} {{ user.first_name[0] }}
                      </div>
                      <template v-slot:loading>
                        <q-spinner-rings color="red-4" />
                      </template>
                    </q-img>
                    <q-btn flat color="white" class="absolute-top-right hover-effect q-pa-none q-ma-none" icon="more_vert" @click.stop="toggleMenu(user.id)" />
                    <q-menu fit anchor="top right" self="bottom middle" v-model="showMenu[user.id]">
                      <q-list style="min-width: 100px">
                        <q-item clickable v-close-popup @click.stop="deleteUser(user.id)">
                          <q-item-section class="hover-effect">Supprimer</q-item-section>
                        </q-item>
                        <q-item clickable v-close-popup @click.stop="toggleActivation({ userId: user.id, isActive: user.is_active })">
                          <q-item-section class="hover-effect">
                            {{ user.is_active ? 'Désactiver' : 'Activer' }}
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
                    @click.stop="toggleInfo(user.id), showMenuLog(user.id)"

                  />
                  <q-menu fit anchor="bottom right" self="top middle" v-model="expanded[user.id]">
                    <q-list style="min-width: 100px">
                      <q-item>
                        <q-item-section avatar class="text-cyan-4">
                          Nom :
                        </q-item-section>
                        <q-item-section class="text-grey-7">
                          {{ user.last_name }}
                        </q-item-section>
                      </q-item>
                      <q-item>
                        <q-item-section avatar class="text-cyan-4">
                          Prénom :
                        </q-item-section>
                        <q-item-section class="text-grey-7">
                          {{ user.first_name }}
                        </q-item-section>
                      </q-item>
                      <q-item>
                        <q-item-section avatar class="text-cyan-4">
                          E-mail :
                        </q-item-section>
                        <q-item-section class="text-grey-7">
                          {{ user.email }}
                        </q-item-section>
                      </q-item>
                      <q-item>
                        <q-item-section avatar class="text-cyan-4">
                          Fonction :
                        </q-item-section>
                        <q-item-section class="text-grey-7">
                          {{ user.function.title }}
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
  name: "UsersCards",

  computed: {
    ...mapGetters('users', ['allUsers', 'showMenu', 'expanded'])
  },

  created() {
    this.loadUsers();
    console.log(this.allUsers);
  },

  methods: {
    ...mapActions('users', ['loadUsers', 'toggleActivation', 'deleteUser', 'toggleMenu', 'toggleInfo']),

    redirectToLink(id) {
      this.$router.push(`/user/${id}`);
    }
  }
};
</script>



