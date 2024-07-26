<template>

<div class="container border mx-auto custom d-flex flex-column" style="width: auto;">
        <h1 class="text-center py-3 bg-success col-md-12 text-light rounded-5 mt-1" style="width: 100%; ">Change Password</h1>
        <form @submit.prevent="changePassword" class="p-3 form ">

            <div class="form-group d-flex flex-row justify-content-between">
                <label for="email" class="form-label m-3">Email ID: </label>
                <input type="email" class="form-control m-3" id="email" v-model="Email" required>
            </div>

            <div class="form-group d-flex flex-row justify-content-between">
                <label for="old_password" class="form-label m-3">Old Password: </label>
                <input type="password" class="form-control m-3" id="old_password" v-model="oldPassword" required>
            </div>


            <div class="form-group d-flex flex-row justify-content-between">
                <label for="new_password" class="form-label m-3">New Password: </label>
                <input type="password" class="form-control m-3" id="new_password" v-model="newPassword" required>
            </div>

            <button type="submit" class="btn btn-danger" v-show="Email && (oldPassword != newPassword) && (oldPassword != '') && (newPassword != '')">Update Password</button>
        
        </form>
    </div>
</template>
<script>
import axios from 'axios';


export default {
    name: 'adminChangePassword', 

    data() {
        return {
            Email: '',
            oldPassword: '',
            newPassword: ''
        }
    }, 

    methods: {
        changePassword() {
            axios.put('/api/v1/user/' + this.Email, { old_password: this.oldPassword, new_password: this.newPassword}, {headers: { 'Token': localStorage.getItem('token') } }).then((response) => {
            if (response.data == true) {
                alert("Password changed successfully")
            } else {
                alert("Email Id or password is incorrect")
            }
        })
        }
    }
}

</script>