<template>
    

    <div class="container d-flex flex-row my-1 mx-0" >
        <managerSidePanel class="col-md-3 mx-2"/>
        <div class="main-panel col-md-10 bordered"> 
            <h1> Welcome Manager </h1>
        </div>
        
    </div>
    

</template>

<script>

import managerSidePanel  from "@/components/managerSidePanel.vue"

export default {
    name: 'managerDashboard', 
    components: {
        managerSidePanel
    }
}
</script>