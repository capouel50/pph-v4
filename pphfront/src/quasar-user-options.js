import './styles/quasar.scss'
import lang from 'quasar/lang/fr.js'
import '@quasar/extras/material-icons/material-icons.css'
import {Notify, Loading, QSpinnerRings} from 'quasar'
// To be used on app.use(Quasar, { ... })
export default {
  plugins: {
    Loading,
    Notify
  },
  config: {
    loading: {
      spinner: QSpinnerRings,
      spinnerColor: 'red',
    },
  },
  lang: lang
}