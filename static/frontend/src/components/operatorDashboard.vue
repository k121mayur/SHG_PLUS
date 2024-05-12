<template>

    <div class="container d-flex flex-column my-1 mx-0">
        <!-- <div> 
            <h1 style="width: 100%;"> Welcome Operator </h1> 
        </div> -->

        <div class="d-flex flex-row m-0 col-md-12 panel">

            <SidePanel class="col-md-3"/>

            <div class="main-panel col-md-9 ">
            
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


export default {
    name: 'operatorDashboard', 
    components: {
        SidePanel
    }
}
</script>