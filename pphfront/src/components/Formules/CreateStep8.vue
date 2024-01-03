<template>
  <div class="row">
        <q-input
        ref="publicationsInput"
        class="my-0 col-3"
        v-model="publications"
        label="Publications, données de stabilité..."
        color ='cyan-4'
        autogrow
        @mouseover="changeLabelColor('nameInput','#ffb74d')"
        @mouseleave="changeLabelColor('nameInput','')"
        @focus="onFocus('name','#4dd0e1')"
        @blur="onBlur('name')"
      >
        <template v-slot:before>
          <q-icon name="article" color="cyan-4"/>
        </template>
      </q-input>
      </div>
</template>

<script>
export default {
  name: "CreateStep8"
}
</script>

<style scoped>

</style>