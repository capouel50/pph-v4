const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  publicPath: process.env.NODE_ENV === 'production' ? '/frontend/' : '/',
  transpileDependencies: [
    'quasar'
  ],

  pwa: {
    manifestOptions: {
      name: "PPH",
      short_name: "PPH",
      description: "Gérér vos préparations tout le long du circuit des matières premières",
      icons: [{
        src: "img/icons/android-chrome-192x192.png",
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
