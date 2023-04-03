<template>
    <v-data-table
      :headers="headers"
      :items="users"
      :item-key="id"
      :sort-by="[{ key: 'id', order: 'asc' }]"
      class="elevation-1"
    >

      <template v-slot:top>
        <v-toolbar
          flat
        >
          <v-toolbar-title>Users</v-toolbar-title>
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
                New User
              </v-btn>
            </template>
            <v-card>
              <v-card-title>
                <span class="text-h5">Add new user</span>
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
                        v-model="newUser.username"
                        label="username"
                      ></v-text-field>
                    </v-col>
                    <v-col
                      cols="12"
                      sm="6"
                      md="4"
                    >
                      <v-text-field
                        v-model="newUser.password"
                        label="password"
                      ></v-text-field>
                    </v-col>
                    <v-col
                      cols="12"
                      sm="6"
                      md="4"
                    >
                      <v-select
                        v-model="newUser.role"
                        label="role"
                        :items="['provider', 'customer', 'employee']"
                      ></v-select>
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
          { title: 'username', key: 'username' },
          { title: 'role', key: 'role' },
          { title: 'Actions', key: 'actions', sortable: false },
        ],
        users: [],
        editedIndex: -1,
        newUser: {
          username: '',
          password: '',
          role: 1,
        },
        defaultItem: {
            username: '',
            password: '',
            role: 1,
        },
        deleteUserId: -1,
        error: null
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
            const response = await fetch('http://127.0.0.1:8000/api/user/', requestOptions)
            const body = await response.json()
            this.users = body
            const roles = {
              '1': 'provider',
              '2': 'customer',
              '3': 'employee'
            }
            this.users.forEach((user)=>{
              user.role = roles[user.role]
            })
        },
        deleteItem (item) {
          this.editedIndex = this.users.indexOf(item)
          this.deleteUserId = this.users[this.editedIndex]['id']
          this.editedItem = Object.assign({}, item)
          this.dialogDelete = true
        },

        async deleteItemConfirm () {
            this.users.splice(this.editedIndex, 1)
            const access = localStorage.getItem('access')
            const requestOptions = {
                method: "DELETE",
                headers: {
                    "Content-Type": "application/json",
                    'Authorization': 'Bearer '+access
                },
                body: JSON.stringify(
                    {
                        'id': this.deleteUserId
                    }
                )
            }
            this.deleteUserId = -1
            const response = await fetch('http://127.0.0.1:8000/api/user/', requestOptions)
            const body = await response.json()
            this.closeDelete()
        },

        close () {
          this.dialog = false
          this.$nextTick(() => {
            this.editedItem = Object.assign({}, this.defaultItem)
            this.editedIndex = -1
          })
        },

        closeDelete () {
          this.dialogDelete = false
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
                        'username': this.newUser.username,
                        'password': this.newUser.password,
                        'role': this.newUser.role
                    }
                )
            }
            const response = await fetch('http://127.0.0.1:8000/api/user/', requestOptions)
            const body = await response.json()
            this.editedItem = body
            if (this.editedIndex > -1) {
                Object.assign(this.users[this.editedIndex], this.editedItem)
            } else {
                this.users.push(this.editedItem)
            }
            if(body['error']){
                this.error = body['error']
                this.alert = true
            }
            else{
                this.error = null
                this.alert=false
                this.close()
            }
        //   if (this.editedIndex > -1) {
        //     Object.assign(this.desserts[this.editedIndex], this.editedItem)
        //   } else {
        //     this.desserts.push(this.editedItem)
        //   }
        },
      },
      mounted(){
            this.initialize()
      }
    }
  </script>
