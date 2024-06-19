<template>
    <div class="d-flex flex-row m-0 col-md-12 panel"> 
        <SidePanel class="col-md-3"/>
        <dataEntryReport class="main-panel col-md-9"/>
    </div>


</template>

<style>

</style>

<script>
import SidePanel from "@/components/SidePanel.vue"
import dataEntryReport from "@/components/dataEntryReport.vue"

export default {
    name: 'dataEntryReportView', 
    components: {
        SidePanel, 
        dataEntryReport
    }
}

</script>