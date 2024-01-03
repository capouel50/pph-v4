<template>
  <q-select
    class="my-0 custom-select"
    :ref="inputRef"
    :label="label"
    :options="options"
    v-model="selectedValue"
    @mouseover="changeLabelColor(inputRef, hoverColor)"
    @mouseleave="changeLabelColor(inputRef, '')"
    @focus="onFocus(inputName, focusColor)"
    @blur="onBlur(inputName)"
  >
  <template v-slot:before>
    <q-icon :name="iconName" color="cyan-4"/>
  </template>
  </q-select>
</template>

<script>
export default {
  props: {
    iconName: String,
    label: String,
    options: Array,
    hoverColor: {
      type: String,
      default: '#ffb74d'
    },
    focusColor: {
      type: String,
      default: '#4dd0e1'
    },
    inputRef: String,
    inputName: String
  },
  data() {
    return {
      selectedValue: null
    };
  },
  methods: {
    changeLabelColor(inputRef, color) {
      this.$refs[inputRef].$el.querySelector('.q-field__label').style.color = color;
    },
    onFocus(name, color) {
      this.$emit('focus', name, color);
    },
    onBlur(name) {
      this.$emit('blur', name);
    }
  },
  watch: {
    selectedValue(val) {
      this.$emit('input', val);
    }
  }
};
</script>

<style scoped>
.custom-select .q-select__option--active.q-item--clickable.q-hoverable:hover {
  color: #ffb74d !important;
}
</style>

