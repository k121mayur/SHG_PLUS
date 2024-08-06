<template>
    <div class="d-flex flex-row m-0 col-md-12 panel">

        <managerSidePanel class="col-md-3"/>
        <creditReport class="main-panel col-md-9 m-2"/>
    
    </div>
    
</template>

<script>
import axios from 'axios'
import managerSidePanel from '../components/managerSidePanel.vue'
import creditReport from '../components/creditReport.vue'


export default {
    name: 'creditReportView',
    components: { 
        managerSidePanel,
        creditReport
    } 
}
</script>