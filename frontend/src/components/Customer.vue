<template>
    <v-card>
        <v-tabs v-model="tab" bg-color="primary">
            <v-tab value="one">loan requests</v-tab>
            <v-tab value="two">loans</v-tab>
        </v-tabs>
    <v-window v-model="tab">
        <v-window-item value="one">
            <v-data-table
                :headers="loanRequestHeaders"
                :items="loanRequests"
                :sort-by="[{ key: 'id', order: 'asc' }]"
            >

                <template v-slot:top>
                    <v-toolbar
                    flat
                    >
                        <v-toolbar-title>Loan requests</v-toolbar-title>
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
                                Request a new loan
                            </v-btn>
                        </template>
                        <v-card>
                        <v-card-title>
                            <span class="text-h5">New loan request</span>
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
                                v-model="newLoanRequest.amount"
                                label="amount"
                            ></v-text-field>
                            </v-col>
                            <v-col
                            cols="12"
                            sm="6"
                            md="4"
                            >
                            <v-text-field
                                v-model="newLoanRequest.terms"
                                label="terms"
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
                        @click="loanRequestSubmit"
                        >
                        Save
                        </v-btn>
                    </v-card-actions>
                    </v-card>
                </v-dialog>
                <v-dialog v-model="dialogDelete" max-width="500px">
                    <v-card>
                    <v-card-title class="text-h5">Are you sure you want to delete this Loan request?</v-card-title>
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
                    <v-card-actions>
                        <v-spacer></v-spacer>
                        <v-btn color="blue-darken-1" variant="text" @click="closeDelete">Cancel</v-btn>
                        <v-btn color="blue-darken-1" variant="text" @click="deleteLoanRequestConfirm">OK</v-btn>
                        <v-spacer></v-spacer>
                    </v-card-actions>
                    </v-card>
                </v-dialog>
                </v-toolbar>
            </template>
            <template v-slot:item.actions="{ item }">
                <v-icon
                size="small"
                @click="deleteLoanRequest(item.raw)"
                >
                mdi-delete
                </v-icon>
            </template>
            </v-data-table>
        </v-window-item>

        <v-window-item value="two">
            <v-data-table
                :headers="loanHeaders"
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
                    <v-dialog v-model="viewPaymentsDialog" max-width="500px">
                        <v-card>
                            <v-card-title>Payments</v-card-title>
                            <v-data-table
                                :headers="paymentHeaders"
                                :items="payments"
                                :sort-by="[{ key: 'id', order: 'asc' }]"
                            ></v-data-table>
                        <v-card-actions>
                            <v-spacer></v-spacer>
                            <v-btn color="blue-darken-1" variant="text" @click="closeViewPayments">Cancel</v-btn>
                            <v-spacer></v-spacer>
                        </v-card-actions>
                        </v-card>
                    </v-dialog>
                    <v-dialog v-model="viewPayDialog" max-width="500px">
                        <v-card>
                            <v-card-title>New payment</v-card-title>
                            <v-card-text>
                        <v-container>
                        <v-row>
                            <v-col
                            cols="12"
                            sm="6"
                            md="4"
                            >
                            <v-text-field
                                v-model="paymentAmount"
                                label="amount"
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
                            <v-btn color="blue-darken-1" variant="text" @click="pay">Pay</v-btn>
                            <v-btn color="blue-darken-1" variant="text" @click="closeViewPay">Cancel</v-btn>
                            <v-spacer></v-spacer>
                        </v-card-actions>
                        </v-card>
                    </v-dialog>
                </v-toolbar>

            </template>
            <template v-slot:item.actions="{ item }">
                <v-icon
                size="medium"
                @click="viewPaymentsList(item.raw)"
                >
                mdi-view-list
                </v-icon>
                <v-icon
                size="medium"
                @click="payment(item.raw)"
                >
                mdi-cash-sync
                </v-icon>
            </template>
            </v-data-table>
        </v-window-item>

    </v-window>

    </v-card>
</template>

  <script>
    export default {
      data: () => ({
        newLoanRequest: {
            amount:0,
            terms: null,
        },
        defaultLoanRequest: {
            amount:0,
            terms: null,
        },
        error: null,
        tab: null,
        alert: false,
        dialog: false,
        dialogDelete: false,
        loanHeaders: [
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
            { title: 'terms', key: 'terms' },
            { title: 'Actions', key: 'actions', sortable: false },


        ],
        loanRequestHeaders: [
          {
            title: 'id',
            align: 'start',
            sortable: true,
            key: 'id',
          },
          { title: 'date', key: 'date' },
          { title: 'amount', key: 'amount' },
          { title: 'isApproved', key: 'isApproved' },
          { title: 'terms', key: 'terms' },
          { title: 'Actions', key: 'actions', sortable: false },
        ],
        loans: [],
        loanRequests: [],
        budget: 0,
        addedBudget: 0,
        deleteIndex: -1,
        deleteLoanRequestId: -1,
        deletedItem: -1,
        dialogDelete: false,
        viewPaymentsDialog: false,
        viewPayDialog: false,
        paymentHeaders: [
            {
            title: 'id',
            align: 'start',
            sortable: true,
            key: 'id',
          },
          { title: 'date', key: 'date' },
          { title: 'amount', key: 'amount' },
          {title: 'loan', key: 'loan'},
        ],
        payments: [],
        paymentAmount: 0,
        loanId: -1,
      }),


      watch: {
        dialog (val) {
          val || this.close()
        },
        dialogDelete (val) {
          val || this.closeDelete()
        },
        viewPaymentsDialog(val){
            val || this.closeViewPayments()
        },
        viewPaymentDialog(val){
            val || this.cloneViewPay()
        }
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
            const response = await fetch('http://127.0.0.1:8000/api/loan/request/', requestOptions)
            const body = await response.json()
            this.loans = body['loans']
            this.loanRequests = body['loanRequests']
            this.loans.forEach((loan) => {
                loan['isPaid'] = String(loan['isPaid'])
                loan['isApproved'] = String(loan['isApproved'])
            })
            this.loanRequests.forEach((loanRequest) => {
                loanRequest['isApproved'] = String(loanRequest['isApproved'])
            })
        },




        async loanRequestSubmit () {
            const access = localStorage.getItem('access')
            const requestOptions = {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    'Authorization': 'Bearer '+access
                },
                body: JSON.stringify(
                    {
                        'amount': this.newLoanRequest['amount'],
                        'terms': this.newLoanRequest['terms']
                    }
                )
            }
            const response = await fetch('http://127.0.0.1:8000/api/loan/request/', requestOptions)
            const body = await response.json()
            body['isApproved'] = String(body['isApproved'])
            const loanRequest = body
            this.loanRequests.push(loanRequest)
            this.newLoanRequest = this.defaultLoanRequest
            if(body['error']){
                this.alert = true
                this.error = body['error']
            }
            else{
                this.alert=false
                this.close()
            }
            this.addedBudget = 0
        },

        deleteLoanRequest (item) {
          this.deleteIndex = this.loanRequests.indexOf(item)
          this.deleteLoanRequestId = this.loanRequests[this.deleteIndex]['id']
          this.deletedItem = Object.assign({}, item)
          this.dialogDelete = true
        },

        async deleteLoanRequestConfirm () {
            const access = localStorage.getItem('access')
            const requestOptions = {
                method: "DELETE",
                headers: {
                    "Content-Type": "application/json",
                    'Authorization': 'Bearer '+access
                },
                body: JSON.stringify(
                    {
                        'loanRequestId': this.deleteLoanRequestId
                    }
                )
            }
            const response = await fetch('http://127.0.0.1:8000/api/loan/request/', requestOptions)
            const body = await response.json()
            if(body['error']){
                this.alert = true
                this.error = body['error']
            }
            else{
                this.deleteLoanRequestId = -1
                this.loanRequests.splice(this.deleteIndex, 1)
                this.alert=false
                this.closeDelete()
            }
        },

        close () {
          this.dialog = false
          this.$nextTick(() => {
            this.deletedItem = Object.assign({}, this.defaultItem)
            this.editedIndex = -1
          })
          this.error = null
        },

        closeDelete () {
          this.dialogDelete = false
          this.$nextTick(() => {
            this.deletedItem = Object.assign({}, this.defaultItem)
            this.editedIndex = -1
          })
          this.error = null
        },
        async viewPaymentsList(){
            this.viewPaymentsDialog = true

            const access = localStorage.getItem('access')
            const requestOptions = {
                method: "GET",
                headers: {
                    "Content-Type": "application/json",
                    'Authorization': 'Bearer '+access
                },
            }
            const response = await fetch('http://127.0.0.1:8000/api/loan/payment/', requestOptions)
            const body = await response.json()
            this.payments = body
            if(body['error']){
                this.alert = true
                this.error = body['error']
            }
            else{
                this.alert=false
            }
        },
        payment(item){
            this.loanId = item['id']
            this.viewPayDialog = true

        },
        async pay(){
            const access = localStorage.getItem('access')
            const requestOptions = {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    'Authorization': 'Bearer '+access
                },
                body: JSON.stringify({
                    'loanId': this.loanId,
                    'paymentAmount': this.paymentAmount,
                })
            }
            this.loanId = -1
            this.paymentAmount = 0
            const response = await fetch('http://127.0.0.1:8000/api/loan/payment/', requestOptions)
            const body = await response.json()
            console.log(body)
            if(body['error']){
                this.alert = true
                this.error = body['error']
            }
            else{
                this.alert=false
                this.closeViewPay()
            }
        },
        closeViewPay(){
            this.viewPayDialog = false
            this.error = null
        },
        closeViewPayments(){
            this.viewPaymentsDialog = false
            this.error = null
        }
      },
      mounted(){
            this.initialize()
      }
    }
  </script>

