<template>
    <v-form>
        <v-text-field
        v-model="username"
        label="username"
        required
        class="mx-15"
        ></v-text-field>

        <v-text-field
        v-model="password"
        label="Password"
        type="password"
        required
        class="mx-15"
        ></v-text-field>

        <v-btn
        color="primary"
        @click="login"
        class = "mx-15"
        >
            Login
        </v-btn>
        <v-alert
            v-if="alert"
            v-model="alert"
            border="left"
            close-text="Close Alert"
            color="error"
            dark
            dismissible
            class="mx-15"
        >
            {{error}}
        </v-alert>
    </v-form>
</template>

<script>
import jwt_decode from 'jwt-decode'
export default {
  data() {
    return {
        username: '',
        password: '',
        alert: false,
        error: null
    }
  },
  methods: {
    async login() {
        const requestOptions = {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify(
                {
                    'username': this.username,
                    'password': this.password
                }
            )
        }
        const response = await fetch('http://127.0.0.1:8000/api/token/', requestOptions)
        const body = await response.json()
        if(body['error']){
            this.error = body['error']
            this.alert = true
        }
        else if(body['message']){
            this.error = body['message']
            this.alert = true
        }
        else if(body['detail']){
            this.error = body['detail']
            this.alert = true
        }
        else{
            this.error = null
            this.alert=false
        }
        const access_token = body['access']
        const refresh_token = body['refresh']
        const access_token_decoded = jwt_decode(access_token)
        localStorage.setItem('access', access_token)
        localStorage.setItem('refresh', refresh_token)
        const role = access_token_decoded['role']
        if(access_token_decoded['is_admin']){
            window.location.href = '../admin/'
        }
        else{
            if(role==1){
                window.location.href = '../provider/'
            }
            else if(role==2){
                window.location.href = '../customer/'
            }
            else if(role==3){
                window.location.href = '../employee/'
            }
        }
    }
  },
  mounted(){
    localStorage.access = null
    localStorage.refresh = null
  }
}
</script>
