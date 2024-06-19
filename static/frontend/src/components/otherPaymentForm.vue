<template>
    <div class="container" style="overflow: auto">
        <form @submit.prevent="submitForm">
        
        <div class="d-flex flex-row flex-wrap" >
            <!-- Loan Repayment -->
            <label for="transactionType" class="form-label m-3">Select Payment Type</label>
            <select class="form-select m-3" @change="fetchAccounts" id="transactionType" v-model="receiptData.transactionType" style="width: max-content;">
                <option value="0">EMI to Bank</option>
                <option value="1">Deposit to Savings Account</option>
                <option value="2">Service Charge to Federation</option>                
                <option value="3">Cash in hand</option>
            </select>

            <label for="loanAccount" class="form-label m-3" v-if="receiptData.transactionType === '0'">Select Loan Account</label>
            <select class="form-select m-3" id="loanAccount" v-model="receiptData.loanAccount" style="width: max-content;" v-if="receiptData.transactionType === '0'">
                <option v-for="account in Account_list" :value="account.id">{{account.bank_name}}-{{ account.account_number }}</option>
            </select>

            <div class="mb-3 col-md-6" v-if="receiptData.transactionType === '0'">
                <label for="principal" class="form-label"> Principal Amount </label>
                <input type="number" class="form-control short mx-3" id="principal" v-model="receiptData.principalAmount">
            </div>

            <div class="mb-3 col-md-6" v-if="receiptData.transactionType === '0'">
                <label for="interest" class="form-label"> Interest Amount </label>
                <input type="number" class="form-control short mx-3" id="interest" v-model="receiptData.interestAmount">
            </div>

            <!-- Savings Deposit -->
            <label for="loanAccount" class="form-label m-3" v-if="receiptData.transactionType === '1'">Select Savings Account</label>
            <select class="form-select m-3" id="memberName" v-model="receiptData.savingsAccountId" style="width: max-content;" v-if="receiptData.transactionType === '1'">
                <option v-for="account in Account_list" :value="account.id">{{account.bank_name}}-{{ account.account_number }}</option>
            </select>


            <div class="mb-3 col-md-6 " v-if="receiptData.transactionType == 1">
                <label for="depositDate" class="form-label">Date of Deposit</label>
                <input type="date" class="form-control  mx-3" id="depositDate" v-model="receiptData.depositDate">
            </div>

            <div class="mb-3 col-md-6" v-if="receiptData.transactionType == 1">
                <label for="interest" class="form-label">Amount</label>
                <input type="number" class="form-control short mx-3" id="interest" v-model="receiptData.depositAmount">
            </div>

            <!-- Service Charge to Federation -->

            

            <div class="mb-3 d-flex justify-content-start" style="margin-left: 10%; margin-top: 2%;" v-if="receiptData.transactionType == 2">
                <label for="memberName" class="form-label">Member Name</label>
                <select class="form-select mx-3" id="memberName" v-model="receiptData.service_charge_member_id" style="width: max-content;">
                    <option v-for="member in members_list" :value="member.value">{{member.name}}</option>
                </select>
            <!-- <input type="text" class="form-control" id="memberName" v-model="receiptData.member_name" required> -->
            </div>

            <div class="mb-3 col-md-6" v-if="receiptData.transactionType == 2">
                <label for="service_charge_amount" class="form-label">Amount</label>
                <input type="number" class="form-control short mx-3" id="service_charge_amount" v-model="receiptData.service_charge_amount">
            </div>


            <div class="mb-3 d-flex justify-content-start" style="margin-left: 10%; margin-top: 2%;" v-if="receiptData.transactionType == 3">
                <label for="memberName" class="form-label">Member Name</label>
                <select class="form-select mx-3" id="memberName" v-model="receiptData.cash_in_hand_member_id" style="width: max-content;">
                    <option v-for="member in members_list" :value="member.value">{{member.name}}</option>
                </select>
            <!-- <input type="text" class="form-control" id="memberName" v-model="receiptData.member_name" required> -->
            </div>

            <div class="mb-3 col-md-6" v-if="receiptData.transactionType == 3">
                <label for="cash_in_hand_amount" class="form-label">Amount</label>
                <input type="number" class="form-control short mx-3" id="cash_in_hand_amount" v-model="receiptData.cash_in_hand_amount">
            </div>
        </div>

        <button type="submit" class="btn btn-primary" v-if="receiptData.transactionType">Submit</button>
        </form>
    </div>
</template>

<style scoped>
.mb-3 {
    display: flex;
    flex-direction: row;
    justify-content: center;
    align-items: center;
}
.short {
    width: 30%;
}

</style>
    

<script>
import axios from 'axios'


export default {
    name: 'otherPaymentForm', 
    props: {
        meeting_id: { 
            type: Number,
            required: true
        }, 

        members_list:{
            type: Array,
            required: false
        }

    },
    data() {
    return {
        shg_id: null,
        Account_list: [],
        receiptData: {
            meeting_id: this.meeting_id,
            transactionType: '',
            loanAccount: '',   
            principalAmount: 0,
            interestAmount: 0,

            savingsAccountId: '', 
            depositDate: '',
            depositAmount: 0,

            service_charge_amount: 0,
            service_charge_member_id : null,

            cash_in_hand_amount: 0, 
            cash_in_hand_member_id: null

        },
        


    }
    },
    methods : {
        submitForm() {
            
            if (this.receiptData.transactionType == 0) {
                axios.post('/api/v1/bankEmiPayments', this.receiptData ,  { headers:{ 'Token': localStorage.getItem('token') } } ).then((response) => {
                if(response.status == 200){
                    alert("Receipt added Successfully!")
                }else{
                    alert("Problem")
                }
            }).catch((error) => {
                alert(error.data)
            })
            }
            else if (this.receiptData.transactionType == 1) {
                axios.post('/api/v1/savingsAccountPayments', this.receiptData ,  { headers:{ 'Token': localStorage.getItem('token') } } ).then((response) => {
                if(response.status == 200){
                    alert("Receipt added Successfully!")
                }else{
                    alert("Problem")
                }
                }).catch((error) => {
                    alert(error.data)
                })
            }else if (this.receiptData.transactionType == 2) {
                axios.post('/api/v1/serviceChargePayments', this.receiptData ,  { headers:{ 'Token': localStorage.getItem('token') } } ).then((response) => {
                if(response.status == 200){
                    alert("Receipt added Successfully!")
                }else{
                    alert("Problem")
                }
                }).catch((error) => {
                    alert(error.data)
                })
            }else if (this.receiptData.transactionType == 3) {
                axios.post('/api/v1/cashInHandPayments', this.receiptData ,  { headers:{ 'Token': localStorage.getItem('token') } } ).then((response) => {
                if(response.status == 200){
                    alert("Receipt added Successfully!")
                }else{
                    alert("Problem")
                }
                }).catch((error) => {
                    alert(error.data)
                })
            }
            
    }, 

    fetchAccounts() {
        if (this.receiptData.transactionType == 0 || this.receiptData.transactionType == 1) {
            axios.get('/api/v1/ShgAccount/' + this.shg_id + '/' + this.receiptData.transactionType,  { headers:{ 'Token': localStorage.getItem('token') } } ).then((response) => {
            this.Account_list = response.data
            }).catch((error) => {
                alert(error.data)
            })
            
        }
        //here the idea is to fetch the list of loan accounts from the server using meeting id to identify the SHG Id
        
    }, 

    fetchShgId() {
        axios.get('/shgID/' + this.meeting_id,  { headers:{ 'Token': localStorage.getItem('token') } } ).then((response) => {
            console.log(response.data.shg_id)
            this.shg_id = response.data.shg_id
        })
}
}, 

created(){
    this.fetchShgId()
}
}
</script>