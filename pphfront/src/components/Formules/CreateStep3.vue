<template>
<div class="row">
      <q-input
        ref="dureeInput"
        class="my-0 col-1"
        v-model="duree"
        label="Durée (j)"
        color ='cyan-4'
        @mouseover="changeLabelColor('nameInput','#ffb74d')"
        @mouseleave="changeLabelColor('nameInput','')"
        @focus="onFocus('name','#4dd0e1')"
        @blur="onBlur('name')"
      >
        <template v-slot:before>
          <q-icon name="alarm" color="cyan-4"/>
        </template>
      </q-input>
      </div>
      <div class="q-pa-md q-gutter-sm">
        <div>
          <q-toggle
            v-model="froid"
            color="cyan-4"
            icon="ac_unit"
            label="4°C - 8°C"
            size="md"
          />
          <q-toggle
             v-model="lumiere"
             color="yellow-4"
             icon="light_mode"
             label="Abris de la lumiere"
             size="md"
          />
          <q-toggle
             v-model="agiter"
             color="red-4"
             icon="waving_hand"
             label="Agiter avant emploi"
             size="md"
          />
         </div>
      </div>
</template>

<script>
export default {
  name: "CreateStep3"
}
</script>

<style scoped>

</style>