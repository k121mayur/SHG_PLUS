<template>
    <div class="d-flex flex-row m-0 col-md-12 panel"> 
        <SidePanel class="col-md-3"/>
        <addBankAccount class="main-panel col-md-9"/>
    </div>


</template>

<script>
import SidePanel from "@/components/SidePanel.vue"
import addBankAccount from "@/components/addBankAccount.vue"

export default {
    name: 'addAccountView', 

    components: {
        SidePanel, 
        addBankAccount
    }
}
</script>