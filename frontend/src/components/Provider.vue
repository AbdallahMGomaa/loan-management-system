<template>
    <v-card>
        <v-card-title>
            <span class="text-h5">total fund: </span>
            <span class="text-h5">{{ budget }}$</span>
        </v-card-title>

    </v-card>

    <v-data-table
      :headers="headers"
      :items="loans"
      :sort-by="[{ key: 'id', order: 'asc' }]"
    >

      <template v-slot:top>
        <v-toolbar
          flat
        >
          <v-toolbar-title>Loans</v-toolbar-title>
          <v-divider
            class="mx-4"
            inset
            vertical
          ></v-divider>
          <v-spacer></v-spacer>
          <v-dialog
            v-model="dialog"
            max-width="500px"
          >
            <template v-slot:activator="{ props }">
              <v-btn
                color="primary"
                dark
                class="mb-2"
                v-bind="props"
              >
                Add fund
              </v-btn>
            </template>
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
                        v-model="addedBudget"
                        label="budget"
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
                  @click="save"
                >
                  Save
                </v-btn>
              </v-card-actions>
            </v-card>
          </v-dialog>
          <v-dialog v-model="dialogDelete" max-width="500px">
            <v-card>
              <v-card-title class="text-h5">Are you sure you want to delete this User?</v-card-title>
              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn color="blue-darken-1" variant="text" @click="closeDelete">Cancel</v-btn>
                <v-btn color="blue-darken-1" variant="text" @click="deleteItemConfirm">OK</v-btn>
                <v-spacer></v-spacer>
              </v-card-actions>
            </v-card>
          </v-dialog>
        </v-toolbar>
      </template>
      <template v-slot:item.actions="{ item }">
        <v-icon
          size="small"
          @click="deleteItem(item.raw)"
        >
          mdi-delete
        </v-icon>
      </template>
    </v-data-table>
  </template>

  <script>
    export default {
      data: () => ({
        error: null,
        alert: false,
        dialog: false,
        dialogDelete: false,
        headers: [
          {
            title: 'id',
            align: 'start',
            sortable: true,
            key: 'id',
          },
          { title: 'date', key: 'date' },
          { title: 'amount', key: 'amount' },
          { title: 'isApproved', key: 'isApproved' },
          { title: 'approvalDate', key: 'approvalDate' },
          { title: 'deadline', key: 'deadline' },
          { title: 'interestRate', key: 'interestRate' },
          { title: 'payday', key: 'payday' },
          { title: 'isPaid', key: 'isPaid' },
          { title: 'minimumPayment', key: 'minimumPayment' },
          { title: 'maximumPayment', key: 'maximumPayment' },
        ],
        loans: [],
        budget: 0,
        addedBudget: 0
      }),


      watch: {
        dialog (val) {
          val || this.close()
        },
        dialogDelete (val) {
          val || this.closeDelete()
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
            const response = await fetch('http://127.0.0.1:8000/api/fund/', requestOptions)
            const body = await response.json()
            this.fund = body['fund']
            this.budget = this.fund['budget']
            this.loans = body['loans']
            this.loans.forEach((loan) => {
                loan['isPaid'] = String(loan['isPaid'])
                loan['isApproved'] = String(loan['isApproved'])
            })
        },


        close () {
          this.dialog = false
          this.$nextTick(() => {
            this.editedItem = Object.assign({}, this.defaultItem)
            this.editedIndex = -1
          })
        },


        async save () {
            const access = localStorage.getItem('access')
            const requestOptions = {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    'Authorization': 'Bearer '+access
                },
                body: JSON.stringify(
                    {
                        'budget': this.addedBudget
                    }
                )
            }
            const response = await fetch('http://127.0.0.1:8000/api/fund/', requestOptions)
            const body = await response.json()
            if(body['error']){
                this.error = body['error']
                this.alert = true
            }
            else{
                this.error = null
                this.budget = body['budget']
                this.alert=false
                this.close()
            }
            this.addedBudget = 0
        },
      },
      mounted(){
            this.initialize()
      }
    }
  </script>

