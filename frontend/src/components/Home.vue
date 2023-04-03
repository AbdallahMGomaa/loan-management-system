<template>
    <v-app>
        <v-container>
        <v-row>
            <v-col cols="12">
                <h1>Welcome to our site {{ name }}</h1>
                <div>
                    <v-btn @click="login()">
                        Login
                    </v-btn>
                </div>
                <div>
                    <v-btn @click="signup()">
                        Signup
                    </v-btn>
                </div>
            </v-col>
        </v-row>
        </v-container>
    </v-app>
</template>

<script>
    export default {
        data() {
            return {
            name: 'My Website'
            }
        },
        mounted() {
            console.log('Component mounted.')
        },
        methods:{
            login(event){
                window.location.href = 'login/'
            },
            signup(event){
                window.location.href = 'signup/'
            }
        }
    }
</script>

<style scoped>
    h1 {
        font-size: 3rem;
    }
</style>
