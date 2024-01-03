export function changeLabelColor(inputRef, color) {
  if (!this[inputRef.replace('Input', '')]) {
    this.$refs[inputRef].$el.querySelector('.q-field__label').style.color = color;
  }
}

export function redirectTo(url) {
  this.$router.push(url);
}

export function onFocus(field, color) {
  this[`${field}Focused`] = true;
  this.changeLabelColor(`${field}Input`, color);
}

export function onBlur(field) {
  this[`${field}Focused`] = false;
}
