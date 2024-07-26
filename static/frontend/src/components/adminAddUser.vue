<template>
    <!--  first_name='Mayur', last_name='Kharade', email='operator@shgplus.in', password=hash_password('password'), last_login=datetime.datetime.now(), roles=['operator'], date_created=datetime.datetime.now() -->
    <div class="container d-flex flex-column my-1 mx-auto border rounded-5 col-md-9 bg-dark" style="background-color: lightblue"> 
        <h1 class="text-center py-3 bg-warning col-md-12 text-dark rounded mt-1" style="width: inherit; ">Add User</h1>
        <form @submit.prevent="createUser" class="p-3 form ">

            <div class="mb-3">
                <label for="firstName" class="form-label text-white">First Name: </label>
                <input type="text" class="form-control col-md-4" id="firstName" v-model="FirstName" required>
            </div>
            <div class="mb-3">
                <label for="lastName" class="form-label text-white">Last Name: </label>
                <input type="text" class="form-control col-md-4" id="lastName" v-model="LastName" required>
            
            </div>

            <div class="mb-3">
                <label for="role" class="form-label text-white">Role: </label>
                <select class="form-select form-control" id="role" v-model="Role" required>
                    <option value="manager">Manager</option>
                    <option value="operator">Operator</option>
                </select>
            
            </div>

            <div class="mb-3">
                <label for="email" class="form-label text-white">Email ID: </label>
                <input type="text" class="form-control" id="email" v-model="Email" required>
            </div>

            <div class="mb-3">
                <label for="password" class="form-label text-white">Set Password: </label>
                <input type="password" class="form-control" id="password" v-model="Password" required>
            </div>

            <div class="mb-3">
                <label for="password" class="form-label text-white">Confirm Password: </label>
                <input type="password" class="form-control" id="password" v-model="ConfirmPassword" required>
            </div>
            <div v-if="Password != ConfirmPassword"> <p class="text-danger bg-light">The password and confirm password should match</p></div>
            <button type="submit" class="btn btn-success" v-show="Password == ConfirmPassword">Create User</button>
        
        </form>
    </div>

</template>

<script>


import axios from 'axios'

export default {
    name: 'adminAddUser', 

    data() {
        return {
            FirstName: '',
            LastName: '',
            Email: '',
            Password: '',
            ConfirmPassword: '', 
            Role: null

        }
    },

    methods: {
        createUser() {
            axios.post('/api/v1/user', { 
                first_name: this.FirstName,
                last_name: this.LastName,
                email: this.Email,
                role : this.Role,
                password: this.Password
            }, {headers: { 'Token': localStorage.getItem('token') } }).then((response) => {
                if (response.data == true){
                    alert("User created successfully")
                }else {
                    alert("email_id already exists")
                }
        }).catch((error) => {
            alert(error.data)
        })
     }

    }
}
</script>

<style scoped>
.mb-3 {
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
}

label {
    margin-right: 10px;
}


</style>