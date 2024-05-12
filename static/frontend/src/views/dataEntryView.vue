<template>


    
    <div class="d-flex flex-row m-0 col-md-12 panel"> 
        <SidePanel class="col-md-3"/>
        <div class="main-panel col-md-9">
            <h1>Data Entry Here</h1>
        </div>

    </div>
    
    

</template>


<style>
     .main-panel {
        height: 85vh;
        border: solid 1px black;
        margin-left: 2px;
        margin-right: 0%;
        border-radius : 10px;
        margin-top: 1%;
    }
    .panel {
        width: 98vw;
    }

</style>

<script>

import SidePanel from "@/components/SidePanel.vue"

export default {
    name: 'dataEntryView', 
    components: {
        SidePanel
    }
}

</script>