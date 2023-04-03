<template>
    <v-data-table
      :headers="headers"
      :items="loanRequests"
      :sort-by="[{ key: 'id', order: 'asc' }]"
    >
      <template v-slot:top>
        <v-toolbar
          flat
        >
          <v-toolbar-title>Loan Requests</v-toolbar-title>
          <v-divider
            class="mx-4"
            inset
            vertical
          ></v-divider>
          <v-spacer></v-spacer>
          <v-dialog
            v-model="dialog"
            max-width="700px"
          >
            <v-card>
              <v-card-title>
                <span class="text-h5">Add fund</span>
              </v-card-title>

              <v-card-text>
                <v-container>
                  <v-row>
                    <v-col
                      cols="12"
                      sm="6"
                      md="4"
                    >
                      <v-text-field
                        v-model="approveRequest.interestRate"
                        label="interest rate"
                      ></v-text-field>
                      <v-text-field
                        v-model="approveRequest.deadline"
                        label="deadline"
                      ></v-text-field>
                      <!-- <div class="d-flex justify-center mt-2">
                        <v-date-picker></v-date-picker>
                      </div> -->
                    </v-col>
                    <v-col>
                      <v-text-field
                        v-model="approveRequest.providerId"
                        label="provider id"
                      ></v-text-field>
                      <v-text-field
                        v-model="approveRequest.minimumPayment"
                        label="minimum payment"
                      ></v-text-field>
                    </v-col>
                    <v-col>
                      <v-text-field
                        v-model="approveRequest.maximumPayment"
                        label="maximum payment"
                      ></v-text-field>
                    </v-col>
                  </v-row>
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
                </v-container>
              </v-card-text>

              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn
                  color="blue-darken-1"
                  variant="text"
                  @click="close"
                >
                  Cancel
                </v-btn>
                <v-btn
                  color="blue-darken-1"
                  variant="text"
                  @click="approveLoan"
                >
                  Save
                </v-btn>
              </v-card-actions>
            </v-card>
          </v-dialog>
        </v-toolbar>
      </template>
      <template v-slot:item.actions="{ item }">
        <v-icon
          size="small"
          @click="approve(item.raw)"
        >
          mdi-plus-box
        </v-icon>
      </template>
    </v-data-table>
  </template>

  <script>
    export default {
      data: () => ({
        menu: false,
        date: null,
        error: null,
        alert: false,
        dialog: false,
        headers: [
            {
                title: 'id',
                align: 'start',
                sortable: true,
                key: 'id',
            },
            { title: 'date', key: 'date' },
            { title: 'amount', key: 'amount' },
            { title: 'terms', key: 'terms' },
            { title: 'Actions', key: 'actions', sortable: false },
        ],
        loanRequests: [],
        approveRequest:{
            loanRequestId: null,
            interestRate: 0,
            deadline: null,
            providerId: null,
            minimumPayment: 0,
            maximumPayment: 0
        },
        defaultRequest:{
            loanRequestId: null,
            interestRate: 0,
            deadline: null,
            providerId: null,
            minimumPayment: 0,
            maximumPayment: 0
        },
      }),


      watch: {
        dialog (val) {
          val || this.close()
        },
      },

      created () {
        this.initialize()
      },
      computed:{

      },
      methods: {
        async initialize(){
            const access = localStorage.getItem('access')
            const requestOptions = {
                method: "GET",
                headers: {
                    "Content-Type": "application/json",
                    'Authorization': 'Bearer '+access
                }
            }
            const response = await fetch('http://127.0.0.1:8000/api/loan/approve/', requestOptions)
            const body = await response.json()
            this.loanRequests = body
        },
        approve(item){
            this.dialog = true
            this.approveRequest['loanRequestId'] = item['id']
        },

        close () {
          this.dialog = false
          this.$nextTick(() => {
            this.approveRequest = this.defaultRequest
          })
        },


        async approveLoan () {
            const access = localStorage.getItem('access')
            const requestOptions = {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    'Authorization': 'Bearer '+access
                },
                body: JSON.stringify(
                    this.approveRequest
                )
            }
            this.approveRequest = this.defaultRequest
            const response = await fetch('http://127.0.0.1:8000/api/loan/approve/', requestOptions)
            const body = await response.json()
            if(body['error']){
                this.error = body['error']
                this.alert = true
            }
            else{
                this.error = null
                this.alert=false
                this.close()
            }
        },
      },
      mounted(){
            this.initialize()
      }
    }
  </script>

