<template>
  <q-page class="flex flex-center">
    <div v-if="loading">
      <q-spinner />
      <p>Validation en cours...</p>
    </div>
    <div v-else>
      <p v-if="success">Votre compte a été validé avec succès!</p>
      <p v-else>Une erreur est survenue lors de la validation de votre compte.</p>
    </div>
  </q-page>
</template>

<script>
import { ref } from 'vue'
import { useRoute } from 'vue-router'
import axios from 'axios'

export default {
  setup () {
    const route = useRoute()
    const loading = ref(true)
    const success = ref(false)

    const validateAccount = async () => {
      try {
        const token = route.params.token
        await axios.post('/api/account/validate', { token })  // Remplacez ceci par votre propre endpoint
        success.value = true
      } catch (error) {
        console.error(error)
      } finally {
        loading.value = false
      }
    }

    validateAccount()

    return { loading, success }
  }
}
</script>
