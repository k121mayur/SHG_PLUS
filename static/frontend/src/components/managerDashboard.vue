<template>
    

    <div class="container d-flex flex-row my-1 mx-0 col-md-12 com-lg-12 col-xl-12" >
        <managerSidePanel class="col-md-3 col-lg-3 col-xl-3"/>
        <div class="main-panel col-md-12 com-lg-12 col-xl-11 bordered"> 
            <h1> Welcome </h1>
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