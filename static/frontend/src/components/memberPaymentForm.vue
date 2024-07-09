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

        <div class="d-flex flex-row flex-wrap justify-content-start" v-if="receiptData.paymentType == 0" >
            
            <div class="mb-3 col-md-12 d-flex justify-content-start">
                <label for="loanPurpose" class="form-label">Loan Purpose</label>
                <select class="form-select mx-3" id="loanPurpose" v-model="receiptData.loan_purpose" style="width: max-content;">
                    <option value="01-A">Dhan, Wheat, and Other Agriculture Seeds</option>
                        <option value="01-B">Vegetable Cultivation</option>
                        <option value="01-C">Livestock</option>
                        <option value="01-D">Motor, Engine, and Others</option>
                        <option value="01-E">Purchasing Land</option>
                        <option value="01-F">Taking Land on Lease</option>
                        <option value="01-G">Deepening the Well, Borewell, etc.</option>
                        <option value="01-H">Other Production Work</option>
                        <option value="02-A">Children's Education</option>
                        <option value="02-B">Health</option>
                        <option value="03-A">Health of Livestock</option>
                        <option value="03-B">Goat Rearing</option>
                        <option value="03-C">Business</option>
                        <option value="03-D">Poultry</option>
                        <option value="04-A">Worshipping</option>
                        <option value="04-B">Vehicle</option>
                        <option value="04-C">Housing</option>
                        <option value="04-D">T.V., Mixture Machine, and Others</option>
                        <option value="04-E">Repaying Old Outside Loan</option>
                        <option value="04-F">Festival and Enjoyment</option>
                        <option value="04-G">Marriage, Funeral, etc.</option>
                        <option value="04-H">Shopping</option>
                        <option value="04-I">Ration</option>
                        <option value="04-J">Traveling</option>
                        <option value="04-K">Case, Police, and Others</option>
                        <option value="04-L">Purchasing Property</option>
                        <option value="04-M">Other</option>
                </select>
            </div>

            <div class="mb-3 col-md-12 d-flex justify-content-start">
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
        receiptData: {
            paymentType: 0,
            meeting_id: this.meeting_id,
            member_id: '',
            loan_amount: 0,
            savings_return_amount: 0,
            savingsReturnReason : '',
            loan_purpose : ''

        },
        loanPurposeList : [
        { value: '01-A', name: 'Dhan, Wheat, and Other Agriculture Seeds' },
        { value: '01-B', name: 'Vegetable Cultivation' },
        { value: '01-C', name: 'Livestock' },
        { value: '01-D', name: 'Motor, Engine, and Others' },
        { value: '01-E', name: 'Purchasing Land' },
        { value: '01-F', name: 'Taking Land on Lease' },
        { value: '01-G', name: 'Deepening the Well, Borewell, etc.' },
        { value: '01-H', name: 'Other Production Work' },
        { value: '02-A', name: 'Children\'s Education' },
        { value: '02-B', name: 'Health' },
        { value: '03-A', name: 'Health of Livestock' },
        { value: '03-B', name: 'Goat Rearing' },
        { value: '03-C', name: 'Business' },
        { value: '03-D', name: 'Poultry' },
        { value: '04-A', name: 'Worshipping' },
        { value: '04-B', name: 'Vehicle' },
        { value: '04-C', name: 'Housing' },
        { value: '04-D', name: 'T.V., Mixture Machine, and Others' },
        { value: '04-E', name: 'Repaying Old Outside Loan' },
        { value: '04-F', name: 'Festival and Enjoyment' },
        { value: '04-G', name: 'Marriage, Funeral, etc.' },
        { value: '04-H', name: 'Shopping' },
        { value: '04-I', name: 'Ration' },
        { value: '04-J', name: 'Traveling' },
        { value: '04-K', name: 'Case, Police, and Others' },
        { value: '04-L', name: 'Purchasing Property' },
        { value: '04-M', name: 'Other' }
      ]
        
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