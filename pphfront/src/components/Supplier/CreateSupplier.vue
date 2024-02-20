<template>
  <q-page class="container">
    <div class="row justify-center">
      <div class="col-12">
        <CreateSupplierStepper @submit="saveSupplier" />
      </div>
    </div>
  </q-page>
</template>

<script>
import CreateSupplierStepper from './CreateSupplierStepper.vue';
import api from '../../../api';

export default {
  components: {
    CreateSupplierStepper
  },
  data() {
    return {
      error: null,
      formSubmitted: false,
    };
  },
  methods: {
    saveSupplier(formData) {
      console.log(formData);
      api.post('PPH/suppliers/', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        }
      })
        .then((response) => {
          console.log(response);
          this.formSubmitted = true;
          this.step= 1;

        })
        .catch((error) => {
          console.error(error);
        });
    },
  },
};
</script>



