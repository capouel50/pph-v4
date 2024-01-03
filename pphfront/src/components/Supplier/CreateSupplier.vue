<template>
  <q-page class="container">
    <div class="row justify-center">
      <div class="col-12">
        <h5 class="text-cyan-4 q-mb-lg text-center">Fiche fournisseur</h5>
        <CreateSupplierForm @submit="saveSupplier" />
      </div>
    </div>
  </q-page>
</template>

<script>
import CreateSupplierForm from './CreateSupplierForm.vue';
import api from '../../../api';

export default {
  components: {
    CreateSupplierForm
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
          this.formSubmitted = true;
          console.log(response.data);

        })
        .catch((error) => {
          console.error(error);
        });
    },
  },
};
</script>



