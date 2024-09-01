<template>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
        <a class="navbar-brand mx-2" href="#">
            <img src="/img/AKRSP.png" width="40" height="40" class="d-inline-block align-top" alt="">
        </a>
        <h4 class="m-2 text-white">SHG +</h4>
    <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
    </button>


    <div class="collapse navbar-collapse justify-content-end" id="navbarSupportedContent">
        <ul class="navbar-nav mr-auto">
        <li class="nav-item active">
            <RouterLink class="nav-link text-white" to ="/Dashboard">Dashboard</RouterLink>
        </li>
        <li class="nav-item active">
            <a class="nav-link text-white" @click="logout">Logout</a>
        </li>
        <li class="nav-item">
            <a class="nav-link" href="#"></a>
        </li>
        <!-- li class="nav-item dropdown">  
            <a class="nav-link dropdown-toggle" href="#" id="navbarDropdown" role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
            Dropdown
            </a>
            <div class="dropdown-menu" aria-labelledby="navbarDropdown">
            <a class="dropdown-item" href="#">Action</a>
            <a class="dropdown-item" href="#">Another action</a>
            <div class="dropdown-divider"></div>
            <a class="dropdown-item" href="#">Something else here</a>
            </div>
        </li -->
        </ul>
    </div>
    </nav>

</template>

<script>
import axios from 'axios';


export default {
  name: 'navbar',
  data () {
    return {
    }
  }, 

  methods: {
    logout() {
        axios.get('/logout')
        .then(response => {
            localStorage.removeItem('token');
            localStorage.removeItem('role')
            window.location.href = '/'
        })
    }
  }

}


</script>