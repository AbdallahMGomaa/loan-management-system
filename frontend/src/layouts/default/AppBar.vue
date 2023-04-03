<template>
  <v-app-bar flat>
    <v-app-bar-title>
      <v-icon icon="mdi-circle-slice-4" />

      Loan Bank
    </v-app-bar-title>
    <v-spacer></v-spacer>
    <v-btn
      text
      @click="logout"
      color="blue-darken-1"
    >
      Logout
    </v-btn>
  </v-app-bar>
</template>

<script>
  export default{
    data: () => {
      return {
      }
    },
    methods: {
      logout(){
        localStorage.access = null
        localStorage.refresh = null
        window.location.href = '../login/'
      }
    },
  }
</script>
