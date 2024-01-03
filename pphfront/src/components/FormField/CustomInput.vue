<template>
  <q-input
    clearable
    class="my-0"
    :value="inputModel"
    @input="updateValue"
    :ref="inputRef"
    :label="label"
    color="cyan-4"
    @mouseover="changeLabelColor(inputRef, hoverColor)"
    @mouseleave="changeLabelColor(inputRef, '')"
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
  data() {
    return {
      isFocused: false,
    };
  },
  props: {
    inputModel: {
      type: [String, Number],
      default: '',
      required: true
    },
    label: {
      type: String,
      required: true
    },
    inputRef: {
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
    updateValue(event) {
      console.log("updateValue is called with:", event.target.value);
      this.$emit('update:inputModel', event.target.value);
    },

    changeLabelColor(inputRef, color) {
      this.$refs[inputRef].$el.querySelector('.q-field__label').style.color = color;
    },

    onFocus() {
      this.isFocused = true;
      this.$emit('update:focused', true);
    },
    onBlur(name) {
      this.$emit('blur', name);
      this.isFocused = false;
      this.$emit('update:focused', false);
    }
  }
};
</script>
