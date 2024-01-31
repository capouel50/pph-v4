<template>

    <div class="row">
      <div class="q-col-2">
        <q-input
          label="Page de début"
          color="cyan-4"
        />
      </div>
      <div class="q-col-2">
        <q-input
          label="Page de fin"
          color="cyan-4"
        />
      </div>
      <div class="q-col-2">
        <q-input
          type="file"
          label="Catalogue PDF"
          color="cyan-4"
        />
      </div>
    </div>

</template>

<script>

export default {
  name: "MatieresImport",

  data() {
    return {

    };
  },

  methods: {


  },
}
</script>

<style scoped>

</style>