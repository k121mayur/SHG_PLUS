<template>
    <div class="container border col-md-6 rounded-5 col-sm-12 col-lg-6 col-xs-12 col-xl-6 d-flex flex-column justify-content-between" style="background-color: beige; height: 50vh;" >
        <div class="alert alert-danger mt-1 mb-0" v-if="loginError">
        {{ loginError }}
        </div>
        <form class="d-flex flex-column justify-content-top align-items-center col-md-12 mt-0"  @submit.prevent="login">
            <div class="form-group my-3 d-flex flex-row justify-content-start">
                <!-- label for="role" style="text-wrap: nowrap;" class="m-3" >Role</label>
                <select type="email" class="form-control" id="role" style="width: 70%;" required v-model="role" > 
                    <option value="admin" >Admin</option>
                    <option value="operator" selected>Data Entry Operator</option>
                    <option value="manager" >Project Manager</option>
                    </select -->

            </div>
            <div class="form-group my-3 d-flex flex-row justify-content-start col-md-10">
                <label for="exampleInputEmail1" style="text-wrap: nowrap;" class="my-3 col-md-4 mr-3" >Email address</label>
                <input type="text" v-model="email" class="rounded border col-md-6 p-1" id="exampleInputEmail1" aria-describedby="emailHelp" placeholder="Enter email" required>

            </div>
            <div class="form-group d-flex flex-row justify-content-start col-md-10">
                <label for="exampleInputPassword1" style="text-wrap: nowrap;" class="my-3 col-md-4 mr-3">Password</label>
                <input type="password" v-model="password" class="rounded border col-md-6 p-1" id="exampleInputPassword1" placeholder="Password" required>
            </div>
       
            <button type="submit" class="btn btn-primary col-md-4 col-sm-6 p-2 mt-4">Login</button>
        </form>
    </div>
</template>



<script>
import { server } from '@/main'
import axios from 'axios'
import store from '@/store'

export default {
  name: 'loginForm',
  data() {
    return {
      role: "", 
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