<template>
  <q-page>
    <div class="row">
      <div class="q-col-2">
        <q-input
          type="file"
          @change="readExcelFile"
        />
      </div>
    </div>
  </q-page>
</template>

<script>
export default {
  name: "MatieresImport"

  data() {
    return {
      excelHeaders: []
    };
  },

  methods: {
    readExcelFile(event) {
      const file = event.target.files[0];
      const reader = new FileReader();

      reader.onload = (e) => {
        const data = new Uint8Array(e.target.result);
        const workbook = XLSX.read(data, { type: 'array' });
        const firstSheetName = workbook.SheetNames[0];
        const worksheet = workbook.Sheets[firstSheetName];
        const json = XLSX.utils.sheet_to_json(worksheet, { header: 1 });
        const headers = json[0]; // Prendre la première ligne comme en-têtes
        this.processHeaders(headers);
      };

      reader.readAsArrayBuffer(file);
    },

    processHeaders(headers) {
      // Traiter les en-têtes ici, par exemple, les stocker dans une variable de données
      this.excelHeaders = headers;
    }
  },
}
</script>

<style scoped>

</style>