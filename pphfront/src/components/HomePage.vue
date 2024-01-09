<template>
  <q-page>
    <div class="row justify-center">
      <div class="col-md-8">
        <div class="row justify-center">

          <div class="col-2 card-home q-ml-sm q-mt-sm">
            <q-card bordered>
              <q-img src="../assets/img/commande.jpg">
                <div class="absolute-top text-subtitle2 text-center hover-effect">
                  En attente commande
                </div>
              </q-img>
            </q-card>
          </div>

          <div class="col-2 card-home offset-1 q-mt-sm">
            <q-card bordered>
              <q-img src="../assets/img/livrer.jpg">
                <div class="absolute-top text-subtitle2 text-center hover-effect">
                  En attente livraison
                </div>
              </q-img>
            </q-card>
          </div>

          <div class="col-2 card-home offset-1 q-mt-sm">
            <q-card bordered>
              <q-img src="../assets/img/demande3.jpg">
                <div class="absolute-top text-subtitle2 text-center hover-effect">
                  En attente préparation
                </div>
              </q-img>
            </q-card>
          </div>

          <div class="col-2 card-home offset-1 q-mt-sm">
            <q-card bordered>
              <q-img src="../assets/img/controle2.jpg">
                <div class="absolute-top text-subtitle2 text-center hover-effect">
                  En attente controle
                </div>
              </q-img>
            </q-card>
          </div>

        </div>
      </div>
    </div>
  </q-page>
</template>

<script>


export default {
  name: "HomePage",

}
</script>

<style scoped>

</style>