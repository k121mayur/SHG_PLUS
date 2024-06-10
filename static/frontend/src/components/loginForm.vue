<template>
    <div class="container border mx-auto custom">
        <div class="alert alert-danger mt-3 mb-0" v-if="loginError">
        {{ loginError }}
        </div>
        <form class=" p-3 flex" @submit.prevent="login">
            <div class="form-group my-3 d-flex flex-row justify-content-end">
                <!-- label for="role" style="text-wrap: nowrap;" class="m-3" >Role</label>
                <select type="email" class="form-control" id="role" style="width: 70%;" required v-model="role" > 
                    <option value="admin" >Admin</option>
                    <option value="operator" selected>Data Entry Operator</option>
                    <option value="manager" >Project Manager</option>
                    </select -->

            </div>
            <div class="form-group my-3 d-flex flex-row justify-content-end">
                <label for="exampleInputEmail1" style="text-wrap: nowrap;" class="m-3" >Email address</label>
                <input type="text" v-model="email" class="form-control" id="exampleInputEmail1" style="width: 70%;" aria-describedby="emailHelp" placeholder="Enter email" required>

            </div>
            <div class="form-group d-flex flex-row justify-content-end">
                <label for="exampleInputPassword1" style="text-wrap: nowrap;" class="m-3">Password</label>
                <input type="password" v-model="password" class="form-control" style="width: 70%;" id="exampleInputPassword1" placeholder="Password" required>
            </div>
       
            <button type="submit" class="btn btn-primary my-3">Login</button>
        </form>
    </div>
</template>

<style>
    .custom {
        width: 40%;
        border-radius: 20px;
    }
</style>



<script>
import { server } from '@/main'
import axios from 'axios'
import store from '@/store'

export default {
  name: 'loginForm',
  data() {
    return {
      role: "operator", // This might not be ideal, see note below
      email: "",
      password: "",
      server,
      loginError: "",
      store,
    }
  },
  methods: {
    async login() {
      localStorage.setItem('role', "");
      localStorage.setItem('token', "");
      try {
        axios.get("/logout")
        const response = await axios.post('/login?include_auth_token', {
          email: this.email,
          password: this.password,
        });

        if (response.status === 400) {
          this.loginError = response.response.errors[0];
        } else if (response.status === 200) {
          localStorage.setItem('token', response.data.response.user.authentication_token);
          const roleResponse = await this.fetchRole(); // Call fetchRole and store response
          localStorage.setItem('role', roleResponse.data);
          this.$router.push('/dashboard');
        }
      } catch (error) {
        this.loginError = "Email or Password is incorrect";
      }
    },
    async fetchRole() {
      const roleResponse = await axios.get('/role', { headers: { 'Token': localStorage.getItem('token') } });
      return roleResponse; // Return the response data
    },
  },
};
</script>