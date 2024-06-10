<template>

    <div class="container d-flex flex-column my-1 mx-0">
        <!-- <div> 
            <h1 style="width: 100%;"> Welcome Operator </h1> 
        </div> -->

        <div class="d-flex flex-row m-0 col-md-12 panel">

            <SidePanel class="col-md-3"/>

            <div class="main-panel col-md-9 ">
                <h1>Operator Dashboard</h1>
                <div class="d-flex flex-row justify-content-between m-3">
                    <div class ="col-md-6 d-flex flex-column">
                        <div class="text-warning m-2 col-md-6"><h3>{{ total_groups }}</h3></div>
                        <div class="text-info m-2 col-md-6"> <h4>Total Number of Groups</h4> </div>
                    </div>

                    <div class ="col-md-6 d-flex flex-column">
                        <div class="text-warning m-2 col-md-6"><h3>{{ data_entry }}</h3></div>
                        <div class="text-info m-2 col-md-6"> <h4>This month data entry</h4> </div>
                    </div>

                
                
                </div>
            </div>
        
        </div>

        

    
    
    </div>

</template>

<style scoped>

    .panel {
        width: 95vw;
    }
    

    .main-panel {
        height: 85vh;
        border: solid 1px black;
        margin-left: 2px;
        margin-right: 0%;
        border-radius : 10px;
        overflow: auto;
    }



</style>



<script>
import SidePanel from './SidePanel.vue';
import axios from 'axios';

export default {
    name: 'operatorDashboard', 
    data () {
        return {
            total_groups: 0, 
            data_entry: 0
        }
    },
    components: {
        SidePanel
    }, 
    methods: {
        fetchGroups() {
            axios.get('/api/operator/dashboard').then(response => {
                this.total_groups = response.data.total_groups
            })
        }

    },
    created() {
        // this.fetchGroups()
    }
}
</script>