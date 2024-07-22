<template>
            <div class="d-flex flex-row m-0 col-md-12 panel">
                <adminSidePanel class="col-md-3"/>
                <div class="main-panel col-md-9 ">
                    <h1 class="text-center text-danger bg-light p-3 rounded" >Admin Dashboard</h1>
                    <div class="col-md-12">
                    </div>
                </div>
            </div>
            
</template>

<script>
import axios from 'axios';
import adminSidePanel from './adminSidePanel.vue';


export default {
    name: 'adminDashboard', 
    components: {
        adminSidePanel
    }
}

</script>