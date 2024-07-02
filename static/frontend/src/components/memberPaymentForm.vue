<template>
    <div class="container" style="overflow: auto">
        <form @submit.prevent="submitForm">
        <div class="mb-3 d-flex justify-content-start" style="margin-left: 10%; margin-top: 5%;">
            <label for="memberName" class="form-label">Member Name</label>
            <select class="form-select mx-3" id="memberName" v-model="receiptData.member_id" style="width: max-content;">
                <option v-for="member in members_list" :value="member.value">{{member.name}}</option>
            </select>
            <!-- <input type="text" class="form-control" id="memberName" v-model="receiptData.member_name" required> -->
        </div>

        <div class="mb-3 d-flex justify-content-start">
            <label for = "paymentType" class="form-label col-md-3">Payment Type</label>
            <select class="form-select mx-3" id="paymentType" style="width: max-content;" v-model="receiptData.paymentType">
                <option value="0" selected>Loan</option>
                <option value="1">Savings Return</option>
            </select>
        </div>

        <div class="d-flex flex-row flex-wrap" v-if="receiptData.paymentType == 0" >
            
            <div class="mb-3 col-md-6">
                <label for="loanPurpose" class="form-label">Loan Purpose</label>
                <select class="form-select mx-3" id="loanPurpose" v-model="receiptData.loan_purpose" style="width: max-content;">
                    <option v-for="purpose in this.loanPurposeList" :value="purpose.value">{{purpose.name}}</option>
                </select>
            </div>

            <div class="mb-3 col-md-6">
                <label for="loanAmount" class="form-label">Loan Amount</label>
                <input type="number" class="form-control short mx-3" id="loanAmount" v-model="receiptData.loan_amount" min="500" required>
            </div>
        </div>

        <div class="d-flex flex-row flex-wrap" v-if="receiptData.paymentType == 1" >
            
            <div class="mb-3 col-md-12">
                <label for="savingsReturnReason" class="form-label">Savings Return Reason</label>
                <select class="form-select mx-3" id="savingsReturnReason" v-model="receiptData.savingsReturnReason" style="width: max-content;">
                    <option value="Medical Emergency">Medical Emergency</option>
                    <option value="Education Emergency">Education Emergency</option>
                    <option value="Member Death / Death of Family Member">Member Death / Death of Family Member</option>

                </select>
            </div>
            
            <div class="mb-3 col-md-12 ">
                    <label for="savings" class="form-label">Savings Return Amount</label>
                    <input type="number" class="form-control short mx-3" id="savings" v-model="receiptData.savings_return_amount">
            </div>
        </div>
        <button type="submit" class="btn btn-primary">Submit</button>
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
    name: 'memberPaymentForm', 
    props: {
        meeting_id: { 
            type: Number,
            required: true
        }, 

        members_list:{
            type: Array,
            required: true
        }

    },
    data() {
    return {
        loanPurposeList : [],
        receiptData: {
            paymentType: 0,
            meeting_id: this.meeting_id,
            member_id: '',
            loan_amount: 0,
            savings_return_amount: 0,
            savingsReturnReason : '',
            loan_purpose : ''

        }
    }
    },
    methods : {
        submitForm() {  
            if (this.receiptData.paymentType == 0) {
                console.log("0")
                axios.post('/api/v1/memberLoanPayments', this.receiptData ,  { headers:{ 'Token': localStorage.getItem('token') } } ).then((response) => {
                    if(response.status == 200){
                        alert("Receipt added Successfully!")
                    }else{
                        alert("Problem")
                    }
                }).catch((error) => {
                    alert(error.data)
                })



            }
            else if (this.receiptData.paymentType == 1) {
                console.log("1")
                axios.post('/api/v1/memberSavingsPayments', this.receiptData ,  { headers:{ 'Token': localStorage.getItem('token') } } ).then((response) => {
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

    getLoanPurposeList(){
        axios.get('/api/v1/loanPurposeList',  { headers:{ 'Token': localStorage.getItem('token') } } ).then((response) => {
            this.loanPurposeList =  response.data
        })
    }
}, 
created(){
    this.getLoanPurposeList()
}
    
}
</script>