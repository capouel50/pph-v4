<template>
<q-btn
    glossy
    round
    class="floating-button shadow-5 btn-grey-primary-pph"
    icon="play_lesson"
  />
</template>

<script>
export default {
  name: "TutorialSequence"
}
</script>

<style scoped>
.floating-button {
  position: fixed;
  bottom: 10px; /* ou la marge que vous souhaitez depuis le bas de l'écran */
  right: 60px; /* ou la marge que vous souhaitez depuis le côté droit de l'écran */
  z-index: 10000; /* assurez-vous qu'il passe par-dessus les autres éléments, ajustez si nécessaire */
}
</style>