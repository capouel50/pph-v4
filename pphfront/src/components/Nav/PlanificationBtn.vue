<template>
<div>
<q-btn :class="{ 'text-cyan-1': !menuOpen, 'text-cyan-4': menuOpen, 'hover-effect': true }" flat label="Planification">
  <q-menu transition-show="jump-down" transition-hide="jump-up" @show="menuOpen = true" @hide="menuOpen = false">
    <q-list class="bg-blue-grey-4" dense style="min-width: 100px">
      <q-item clickable class="hover-effect" v-close-popup>
        <router-link to="/demande/" class="pph-link">
          <q-item-section class="text-cyan-1 hover-effect">Nouvelle demande</q-item-section>
        </router-link>
      </q-item>
      <q-item clickable class="hover-effect" v-close-popup>
        <router-link to="/demandes/" class="pph-link">
          <q-item-section class="text-cyan-1 hover-effect">Demandes en attentes</q-item-section>
        </router-link>
      </q-item>
    </q-list>
  </q-menu>
</q-btn>
</div>
</template>

<script>
export default {
  name: 'PlanificationBtn',
  data() {
    return {
      menuOpen: false,
    };
  },
}
</script>