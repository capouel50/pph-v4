<template>
<q-drawer
        below
        overlay

        v-model="drawer"
        show-if-above

        :mini="miniState"
        @mouseover="miniState = false"
        @mouseout="miniState = true"

        :width="200"
        :breakpoint="500"
        bordered
        :class="$q.dark.isActive ? 'bg-grey-9' : 'bg-grey-3'"
      >
        <q-scroll-area class="fit" :horizontal-thumb-style="{ opacity: 0 }">
          <q-list padding style="margin-top: 80px;">
            <q-item clickable v-ripple class="hover-effect">
              <q-item-section avatar>
                <q-icon name="shopping_cart" />
              </q-item-section>

              <q-item-section>
                En commande
              </q-item-section>
            </q-item>

            <q-item clickable v-ripple class="hover-effect">
              <q-item-section avatar>
                <q-icon name="forklift" />
              </q-item-section>

              <q-item-section>
                Réception
              </q-item-section>
            </q-item>

            <q-item clickable v-ripple class="hover-effect">
              <q-item-section avatar>
                <q-icon name="local_pharmacy" />
              </q-item-section>

              <q-item-section>
                Fabrication
              </q-item-section>
            </q-item>

            <q-item clickable v-ripple class="hover-effect">
              <q-item-section avatar>
                <q-icon name="list_alt" />
              </q-item-section>

              <q-item-section>
                Demandes
              </q-item-section>
            </q-item>

            <q-separator />

            <q-item clickable v-ripple class="hover-effect">
              <q-item-section avatar>
                <q-icon name="check" />
              </q-item-section>

              <q-item-section>
                Contrôle
              </q-item-section>
            </q-item>
          </q-list>
        </q-scroll-area>
      </q-drawer>
</template>

<script>
import { ref } from 'vue'

export default {
  setup () {
    return {
      drawer: ref(true),
      miniState: ref(true)
    }
  }
}
</script>

<style scoped>

</style>