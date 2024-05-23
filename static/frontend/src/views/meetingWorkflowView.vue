<template>

<div class="d-flex flex-row m-0 col-md-12 panel"> 
        <SidePanel class="col-md-3"/>
        <meetingWorkflow class="main-panel col-md-9"/>
    </div>


</template>

<script>
import SidePanel from "@/components/SidePanel.vue"
import meetingWorkflow from "@/components/meetingWorkflow.vue"

export default {
    name: 'meetingWorkflowView',
    components: { 
        SidePanel,
        meetingWorkflow
}
}
</script>

<style>

</style>