<template>
<div>
<q-btn :class="{ 'text-cyan-1': !menuOpen, 'text-cyan-4': menuOpen, 'hover-effect': true }" flat label="Tracabilite">
  <q-menu transition-show="jump-down" transition-hide="jump-up" @show="menuOpen = true" @hide="resetMenu">
    <q-list class="bg-blue-grey-4" dense style="min-width: 100px">
      <q-item clickable class="hover-effect">
        <q-item-section :class="{ 'text-cyan-1': !submenuOpen, 'text-cyan-4': submenuOpen, 'hover-effect': true }">Certificats d'analyse</q-item-section>
        <q-item-section side>
          <q-icon name="keyboard_arrow_right" />
        </q-item-section>

        <q-menu anchor="top end" self="top start" @show="submenuOpen = true" @hide="submenuOpen = false">
          <q-list class="bg-blue-grey-3">
            <q-item clickable class="hover-effect" v-close-popup>
              <q-item-section class="text-cyan-1 hover-effect-2">Télécharger</q-item-section>
            </q-item>
            <q-item clickable class="hover-effect" v-close-popup>
              <q-item-section class="text-cyan-1 hover-effect-2">Rechercher</q-item-section>
            </q-item>
          </q-list>
        </q-menu>
      </q-item>
      <q-item clickable class="hover-effect" v-close-popup>
        <q-item-section class="text-cyan-1 hover-effect">Ordonnancier</q-item-section>
      </q-item>
      <q-item clickable class="hover-effect">
        <q-item-section :class="{ 'text-cyan-1': !submenuOpen2, 'text-cyan-4': submenuOpen2, 'hover-effect': true }">Historiques</q-item-section>
        <q-item-section side>
          <q-icon name="keyboard_arrow_right" />
        </q-item-section>

        <q-menu anchor="top end" self="top start" @show="submenuOpen2 = true" @hide="submenuOpen2 = false">
          <q-list class="bg-blue-grey-3">
            <q-item clickable class="hover-effect" v-close-popup>
              <q-item-section class="text-cyan-1 hover-effect-2">Patient</q-item-section>
            </q-item>
            <q-item clickable class="hover-effect" v-close-popup>
              <q-item-section class="text-cyan-1 hover-effect-2">Matière première</q-item-section>
            </q-item>
            <q-item clickable class="hover-effect" v-close-popup>
              <q-item-section class="text-cyan-1 hover-effect-2">Préparation</q-item-section>
            </q-item>
          </q-list>
        </q-menu>

      </q-item>
    </q-list>
  </q-menu>
</q-btn>
</div>
</template>

<script>
export default {
  name: 'TracabiliteBtn',
  data() {
    return {
      menuOpen: false,
      submenuOpen: false,
      submenuOpen2: false,
    };
  },
  methods: {
    resetMenu() {
      this.menuOpen = false;
      this.submenuOpen = false;
      this.submenuOpen2 = false;
    }
  }
}
</script>