<template>

    <div>

        <h1 class="text-center bg-success p-3 text-light rounded-3">Add Bank Account</h1>
        <div class="form-group d-flex flex-row justify-content-center align-items-center"> 
            <label for="accountType" class="form-label m-1 text-primary" ><strong>Select Account Type:</strong></label>
        <select class="form-select m-3" id="accountType" v-model="accountType" style="width: max-content;">
            <option value="1">Savings Account</option>
            <option value="2">Loan Account</option>
        </select>
        </div>
        
        <addLoanAccount v-if="accountType == 2"/>
        <addSavingsAccount v-if="accountType == 1" />
    
    </div>


</template>

<script>
import addLoanAccount from '@/components/addLoanAccount.vue'
import addSavingsAccount from './addSavingsAccount.vue';


export default {
    name: 'addBankAccount',
    components: {
        addLoanAccount, 
        addSavingsAccount
    }, 
    data() {
        return {
            accountType: 1
    }
}

}

</script>