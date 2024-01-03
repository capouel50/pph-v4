<template>
<div>
<q-btn :class="{ 'text-cyan-1': !menuOpen, 'text-cyan-4': menuOpen, 'hover-effect': true }" flat label="Aide">
  <q-menu transition-show="jump-down" transition-hide="jump-up" @show="menuOpen = true" @hide="menuOpen = false">
    <q-list class="bg-blue-grey-4" dense style="min-width: 100px">
      <q-item clickable v-close-popup>
        <q-item-section class="text-cyan-1 hover-effect">Documentation</q-item-section>
      </q-item>
      <q-item clickable v-close-popup>
        <q-item-section class="text-cyan-1 hover-effect">Signaler un bug</q-item-section>
      </q-item>
    </q-list>
  </q-menu>
</q-btn>
</div>
</template>

<script>
export default {
  name: 'AideBtn',
  data() {
    return {
      menuOpen: false,
    };
  },
}
</script>