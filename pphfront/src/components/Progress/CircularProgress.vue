<template>
  <div class="q-pa-md flex flex-center relative-position">
    <q-circular-progress
      indeterminate
      rounded
      reverse
      v-for="size in sizes"
      :key="size"
      :size="size"
      :value="value"
      color="orange"
      :class="['q-ma-md', `circle-${size}`, { 'reverse-rotation': index % 2 === 1 }]"
    />
  </div>
</template>

<script>
export default {
  data() {
    return {
      sizes: ['xl'],
      value: 50
    };
  }
};
</script>

<style scoped>
.relative-position {
  position: relative;
}

.circle-xs,
.circle-sm,
.circle-md,
.circle-lg,
.circle-xl {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}
.reverse-rotation {
  transform: scaleX(-1);
}

</style>
