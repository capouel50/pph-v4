<template>
  <div class="row">
      <q-input
        ref="emploiInput"
        class="my-0 col-3"
        v-model="emploi"
        label="Entrez les informations"
        color ='cyan-4'
        autogrow
        @mouseover="changeLabelColor('nameInput','#ffb74d')"
        @mouseleave="changeLabelColor('nameInput','')"
        @focus="onFocus('name','#4dd0e1')"
        @blur="onBlur('name')"
      >
        <template v-slot:before>
          <q-icon name="info" color="cyan-4"/>
        </template>
      </q-input>
      </div>
</template>

<script>
export default {
  name: "CreateStep7"
}
</script>

<style scoped>

</style>