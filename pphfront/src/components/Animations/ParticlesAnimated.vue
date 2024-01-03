<template>
  <div>
    <div id="particles-js"></div>
  </div>
</template>

<script>
import { mapState } from 'vuex';
import 'particles.js/particles';
const particlesJS = window.particlesJS;


export default {
  name: "ParticlesAnimated",

 computed: {
    ...mapState('auth', ['isLoggedIn'])
  },

  watch: {
    isLoggedIn: 'loadParticlesConfig'
  },

  mounted() {
    this.loadParticlesConfig();
  },

  methods: {
    loadParticlesConfig() {
      const configPath = this.isLoggedIn ? '/particlesjs-config.json' : '/guest-particlesjs-config.json';
      particlesJS.load('particles-js', configPath, function() {
        console.log('Particles.js config loaded');
      });
    }
  }
};
</script>

<style>

#particles-js {
  position: absolute;
  width: 100%;
  height: 100%;
  z-index: 0; /* ou 0, selon ce qui fonctionne dans votre cas */
}

</style>
