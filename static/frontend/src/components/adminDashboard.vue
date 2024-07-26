<template>
            <div class="d-flex flex-row m-0 col-md-12 panel ">
                <div class=" col-md-3 mt-2 mx-auto">
                    <div class="side-panel card d-flex flex-column justify-content-start" >
                        <div class="card-header custom-card-format">
                            Actions
                        </div>
                        
                        <div class="element" > 
                            <button type="button" class="btn mx-1 col-md-12" @click="change_view_to('dashboard')">Home</button>
                            <!-- <a href="">Group Data Entry</a> -->
                        </div>
                        
                        <div class="element"> 
                            <button type="button" class="btn mx-1 col-md-12" @click="change_view_to('createUser')">Create New User</button>
                            <!-- <a href="">Group Data Entry</a> -->
                        </div>
                        
                        <div class="element"> 
                            <button type="button" class="btn mx-1 col-md-12" @click="change_view_to('adminDeleteUser')">Delete User</button>
                        </div>

                        <div class="element"> 
                            <button type="button" class="btn mx-1 col-md-12" @click="change_view_to('adminChangePassword')">Change Password</button>
                        </div>
                    
                    </div>
                </div>
                <div class="main-panel col-md-9 ">
                    
                    <div class="col-md-12 m-3">
                        <component :is="current_view" class="d-flex justify-content-start align-items-center"> </component>
                    </div>
                </div>
            </div>
            
</template>

<script>
import axios from 'axios';
import adminSidePanel from './adminSidePanel.vue';
import adminAddUser from '../components/adminAddUser.vue'
import adminDeleteUser from '../components/adminDeleteUser.vue'
import adminChangePassword from '../components/adminChangePassword.vue'




export default {
    name: 'adminDashboard', 
    data() {
        return {
            current_view : adminAddUser 
        }
    },
    components: {
        adminSidePanel,
        adminAddUser,
        adminDeleteUser,
        adminChangePassword
    }, 
    methods: {
        change_view_to(view) {
            if (view === 'createUser') {
                this.current_view = adminAddUser
        }else if (view === 'adminDeleteUser') {
                this.current_view = adminDeleteUser
        }else if (view === 'adminChangePassword') {
                this.current_view = adminChangePassword
        }else {
                this.current_view = adminDashboardData
        }
    }
}
}
</script>

<style scoped>
    .side-panel {
        height: 85vh;
        border: solid 1px black;
        margin-left: 0;
        border-radius : 10px;
        overflow: auto;
        margin-top: 1%;

    }

    .element {
        background-color: white;
        color: black;
        padding : 4%;
        border-radius: 5px;
        font-family: Verdana, Geneva, Tahoma, sans-serif;
        
        
    }

    .element > a {
        text-decoration: none;
        color: black;
        width: 100%;
        height: 10px;
        padding: 4%;
    }

    a:hover {
        color : white;
    }

    .element:hover {
        background-color: green;
        color : white;
        cursor: pointer;
    }

    .custom-card-format {
        background-color: maroon;
        color: white;
        font-family: 'Times New Roman', Times, serif;
        font: 1.5em sans-serif;
    }


</style>