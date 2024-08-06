<template>
    <div class="d-flex flex-row m-0 col-md-12 panel"> 
            <managerSidePanel class="col-md-3"/>
            <savingReport
            class="main-panel col-md-9 m-2" />
    </div>  
</template>

<script>
import managerSidePanel from "@/components/managerSidePanel.vue"
import savingReport from "@/components/savingReport.vue"

export default {
    name: 'savingReportView',
    components: { 
        managerSidePanel,
        savingReport
    }
}
</script>

<style scoped>
</style>