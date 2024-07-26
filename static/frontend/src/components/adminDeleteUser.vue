<template>

    <div class="container border mx-auto custom d-flex flex-column" style="width: auto;">
        <h1 class="text-center py-3 bg-light col-md-12 text-danger rounded-5 mt-1" style="width: 100%; "> Delete User</h1>
        <form @submit.prevent="deleteUser" class="p-3 form ">

            <div class="form-group d-flex flex-row">
                <label for="email" class="form-label m-3">Email ID: </label>
                <input type="email" class="form-control m-3" id="email" v-model="Email" required>
            </div>

            <button type="submit" class="btn btn-danger" v-show="Email">Delete User</button>
        
        </form>
    </div>

</template>
<script>
import axios from 'axios';

export default {
    name: 'adminDeleteUser',

    data() {
        return {
            Email: ''
        }
    },
    methods: {
        deleteUser() {
            axios.delete("/api/v1/user/" + this.Email, { headers: { 'Token': localStorage.getItem('token') } }).then((response) => {
                if (response.data == true) {
                    alert("User deleted successfully")
                } else {
                    alert("User does not exist")
                }
            })
        }
    }
}
</script>