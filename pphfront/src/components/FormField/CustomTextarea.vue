<template>
  <q-input
    type="textarea"
    class="my-0"
    :value="textareaModel"
    @input="updateValue($event)"
    :ref="textareaRef"
    :label="label"
    color="cyan-4"
    @mouseover="changeLabelColor(textareaRef, hoverColor)"
    @mouseleave="changeLabelColor(textareaRef, '')"
    @focus="onFocus(modelName, focusColor)"
    @blur="onBlur(modelName)"
  >
    <template v-slot:before>
      <q-icon :name="iconName" color="cyan-4"/>
    </template>
  </q-input>
</template>

<script>
export default {
  props: {
    textareaModel: {
      type: String,
      required: true
    },
    label: {
      type: String,
      required: true
    },
    textareaRef: {
      type: String,
      required: true
    },
    iconName: {
      type: String,
      required: true
    },
    modelName: {
      type: String,
      required: true
    },
    hoverColor: {
      type: String,
      default: "#ffb74d"
    },
    focusColor: {
      type: String,
      default: "#4dd0e1"
    }
  },
  methods: {
    updateValue(value) {
       this.$emit('update:textareaModel', value);
    },

    changeLabelColor(textareaRef, color) {
      this.$refs[textareaRef].$el.querySelector('.q-field__label').style.color = color;
    },

    onFocus() {
      this.isFocused = true;
      this.$emit('update:focused', true);
    },
    onBlur() {
      this.isFocused = false;
      this.$emit('update:focused', false);
    }
  }
};
</script>
