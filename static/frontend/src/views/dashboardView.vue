<template>

    <adminDashboard v-if="this.role === 'admin'"  />
    <operatorDashboard v-if="this.role === 'operator'"  />
    <managerDashboard v-if="this.role === 'manager'"  />


</template>

<script>
import adminDashboard  from "@/components/adminDashboard.vue"
import operatorDashboard  from "@/components/operatorDashboard.vue"
import managerDashboard  from "@/components/managerDashboard.vue"



export default {
    name: 'dashboardView', 
    components: {
        adminDashboard,
        operatorDashboard,
        managerDashboard
    }, 
    data() {
        return {
            role: ""
        }
    }, 
    created() {

        this.role = localStorage.getItem('role')
    },
}
</script>