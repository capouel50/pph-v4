<template>
<div class=" row justify-center">
      <atom-spinner
        class="bg-op-8"
        :animation-duration="1000"
        :size="200"
        :color="'#ff1d5e'"
      />
      </div>
</template>

<script>
import {AtomSpinner} from 'epic-spinners'
export default {
  name: "AtomSpinner",
  components: {
    AtomSpinner
  },
}
</script>

<style scoped>
/* Définir l'animation keyframes */
@keyframes spin {
    from {
        transform: rotate(0deg);
    }
    to {
        transform: rotate(360deg);
    }
}

/* Appliquer l'animation au spinner */
.atom-spinner {
    animation: spin 10s linear infinite;
}
</style>