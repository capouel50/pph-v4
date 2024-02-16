<template>
<div>
<q-btn :class="{ 'text-cyan-1': !menuOpen, 'text-cyan-4': menuOpen, 'hover-effect': true }" flat label="Fabrication">
  <q-menu transition-show="jump-down" transition-hide="jump-up" @show="menuOpen = true" @hide="menuOpen = false">
    <q-list class="bg-blue-grey-4" dense style="min-width: 100px">
      <q-item clickable class="hover-effect" v-close-popup>
        <router-link to="/fiches/" class="pph-link">
          <q-item-section class="text-cyan-1 hover-effect">Fiche de fabrication</q-item-section>
        </router-link>
      </q-item>
      <q-item clickable class="hover-effect" v-close-popup>
        <router-link to="/controles/" class="pph-link">
          <q-item-section class="text-cyan-1 hover-effect">Attente contrôle</q-item-section>
        </router-link>
      </q-item>
      <q-item clickable class="hover-effect" v-close-popup>
        <router-link to="/archives/" class="pph-link">
          <q-item-section class="text-cyan-1 hover-effect">Terminées</q-item-section>
        </router-link>
      </q-item>
    </q-list>
  </q-menu>
</q-btn>
</div>
</template>

<script>
export default {
  name: 'FabricationBtn',
  data() {
    return {
      menuOpen: false,
    };
  },
}
</script>