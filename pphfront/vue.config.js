const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  publicPath: '/',
  transpileDependencies: [
    'quasar'
  ],

  pwa: {
    manifestOptions: {
      name: "PPH",
      short_name: "PPH",
      description: "Gérér vos préparations tout le long du circuit des matières premières",
      icons: [{
        src: "favicon.ico",
        sizes: "192x192",
        type: "image/png"
      }],
      start_url: "/login/",
      display: "fullscreen"
    }
  },

  pluginOptions: {
    quasar: {
      importStrategy: 'kebab',
      rtlSupport: false
    }
  }
})
