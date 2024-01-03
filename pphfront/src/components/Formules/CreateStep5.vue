<template>
  <div class="row">
        <q-input
        ref="modeOpInput"
        class="my-0 col-3"
        v-model="modeOperatoire"
        label="Mode opératoire"
        color ='cyan-4'
        autogrow
        @mouseover="changeLabelColor('nameInput','#ffb74d')"
        @mouseleave="changeLabelColor('nameInput','')"
        @focus="onFocus('name','#4dd0e1')"
        @blur="onBlur('name')"
      >
        <template v-slot:before>
          <q-icon name="menu_book" color="cyan-4"/>
        </template>
      </q-input>
      </div>
</template>

<script>
export default {
  name: "CreateStep5"
}
</script>

<style scoped>

</style>