<template>
  <q-toolbar class="bg-blue-grey-13 q-pa-md row">
  <a href="home/">
    <font-awesome-icon icon="fa-solid fa-mortar-pestle" beat-fade size="xl" :color="tokenColor" />
  </a>
  <q-toolbar-title class="text-cyan-4" style="max-width:100px;">PPH</q-toolbar-title>

  <q-btn-group flat>
    <FichierBtn />
    <PlanificationBtn/>
    <FabricationBtn/>
    <TracabiliteBtn/>
    <GestionBtn/>
  </q-btn-group>

  <q-space />

  <q-btn-group>
    <q-btn flat size="sm" color="cyan-4" @click="toggleFullscreen" icon="minimize" />
    <q-btn flat size="sm" color="cyan-4" @click="toggleFullscreen" icon ="crop_square" />
    <q-btn flat size="sm" color="orange-4" @click="logout" icon="logout" v-if="isLoggedIn" />
    <q-btn flat size="sm" color="red-4" @click="close" icon="close" v-if="isLoggedIn" />
  </q-btn-group>

</q-toolbar>

</template>

<script>
import { mapActions, mapState } from 'vuex'
import FichierBtn from './FichierBtn.vue'
import PlanificationBtn from './PlanificationBtn.vue'
import FabricationBtn from './FabricationBtn.vue'
import TracabiliteBtn from './TracabiliteBtn.vue'
import GestionBtn from './GestionBtn.vue'
// importez les autres boutons ici

export default {
  components: {
    FichierBtn,
    PlanificationBtn,
    FabricationBtn,
    TracabiliteBtn,
    GestionBtn,
    // ajoutez les autres boutons ici
  },
  computed: {
    ...mapState('screen', ['isFullscreen']),
    ...mapState('auth', ['isLoggedIn']),
    ...mapState('auth', ['tokenStatus']),

    tokenColor() {
        switch (this.tokenStatus) {
            case 'valid':
              default:
                return "#81c784";
            case 'nearExpiry':
                return "#ffb74d";
            case 'nearInvalid':
                return "#e57373";
        }
    }
  },
  methods: {
    ...mapActions('auth', ['logout']),
    ...mapActions('screen', ['toggleFullscreen'])
  },

}

</script>







