<template>
    <div class="d-flex flex-row m-0 col-md-12 panel"> 
            <SidePanel class="col-md-3"/>
            <shareoutReport
            class="main-panel col-md-9" />
    </div>
</template>

<style scoped>

</style>

<script>
import SidePanel from "@/components/SidePanel.vue"
import shareoutReport from "@/components/shareoutReport.vue"
export default {    
    name: 'shareoutView',
    components: {
        SidePanel,
        shareoutReport
    }
}
</script>
