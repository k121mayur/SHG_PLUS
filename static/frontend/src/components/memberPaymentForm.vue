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

        <!-- <div class="mb-3 d-flex justify-content-start">
            <label for = "paymentType" class="form-label col-md-3">Payment Type</label>
            <select class="form-select mx-3" id="paymentType" style="width: max-content;" v-model="receiptData.paymentType">
                <option value="0" selected>Loan</option>
                <option value="1">Savings Return</option>
            </select>
        </div> -->

        <div class="d-flex flex-row flex-wrap justify-content-start" v-if="receiptData.paymentType == 0" >
            
            <div class="mb-3 col-md-12 d-flex justify-content-start">
                <label for="loanPurpose" class="form-label">Loan Purpose</label>
                <select class="form-select mx-3" id="loanPurpose" v-model="receiptData.loan_purpose" style="width: max-content;">
                        <option value="A">Livelihood/Investment </option>
                        <option value="B">Health</option>
                        <option value="C">Education</option>
                        <option value="D">Repayment of High interest loan</option>
                        <!-- <option value="01-E">Purchasing Land</option>
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
                        <option value="04-M">Other</option> -->
                </select>
            </div>

            <div class="mb-3 col-md-12 d-flex justify-content-start">
                <label for="loanDate" class="form-label">Loan Date</label>
                <input type="date" :max="new Date().toISOString().split('T')[0]" class="form-control short mx-3"  id="loanDate" v-model="receiptData.loan_date" required>
            </div>

            <div class="mb-3 col-md-12 d-flex justify-content-start">
                <label for="loanAmount" class="form-label">Loan Amount</label>
                <input type="number" class="form-control short mx-3" id="loanAmount" v-model="receiptData.loan_amount" min="500" required>
            </div>
        </div>

        <!-- <div class="d-flex flex-row flex-wrap" v-if="receiptData.paymentType == 1" >
            
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
        </div> -->
            <button type="submit" class="btn btn-primary">Submit</button> 
            <button type="button" class="btn btn-warning m-1" @click="list_member_payments(0)">List</button>
        </form>

        <div v-if="toggle_payments_list && payments_list.length > 0" style="position: absolute; top: 0; left: 0; width: 100%; height: 110%; background-color: white;">
            <div class="d-flex flex-row flex-wrap justify-content-end">
                <button type="button" class="btn btn-danger justify-content-end" @click="toggle_payments_list = false">Close</button>
            </div>
                <div>
                    <h1>Payments List</h1>
                    <table class="table table-striped table-bordered table-hover">
                        <thead>
                            <tr>
                                <th>Sr. No.</th>
                                <th>Member Name</th>
                                <th>Payment Type</th>
                                <th>Payment Amount</th>
                                <th>Action</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="(payment, index) in payments_list">
                                <td>{{ index+1 }}</td>
                                <td>{{ payment.name }}</td>
                                <td>{{ payment.payment_type }}</td>
                                <td>{{ payment.payment_amount }}</td>
                                <td><button class="btn btn-primary" @click="delete_payment(payment.id)">Delete</button></td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            
        </div>
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
            loan_date: '',
            savings_return_amount: 0,
            savingsReturnReason : '',
            loan_purpose : ''

        },
        payments_list : [],
        toggle_payments_list : false
        
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
                    alert("Per member only one loan can be disbursed. Please select another member.")
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
    },

    list_member_payments(paymentType){ 
        this.toggle_payments_list = true
        if (paymentType == 0) {
            axios.get('/api/v1/memberLoanPayments/' + this.meeting_id,  { headers:{ 'Token': localStorage.getItem('token') } } ).then((response) => {
                this.payments_list =  response.data
                if (this.payments_list.length == 0) {
                    alert("No payments found")
                }
            }).catch((error) => {
                alert(error.data)
            })
        } else if (paymentType == 1) {
            axios.get('/api/v1/memberSavingsPayments/' + this.meeting_id,  { headers:{ 'Token': localStorage.getItem('token') } } ).then((response) => {
                this.payments_list =  response.data 
                if (this.payments_list.length == 0) {
                    alert("No payments found")
                }
            }).catch((error) => {
                alert(error.data)
            })
        }
    },

    delete_payment(payment_id){
        if (this.receiptData.paymentType == 0) {
            axios.delete('/api/v1/memberLoanPayments',  { headers:{ 'Token': localStorage.getItem('token') } , data: {"id": payment_id} }).then((response) => {
                if(response.status == 200){
                    alert("Receipt deleted Successfully!") 
                    this.list_member_payments(this.receiptData.paymentType);

                }else{
                    alert("Problem")
                }
            }).catch((error) => {
                alert(error.data)
            })
        } else if (this.receiptData.paymentType == 1) {
            axios.delete('/api/v1/memberSavingsPayments',  { headers:{ 'Token': localStorage.getItem('token') } , data: {"id": payment_id} } ).then((response) => {
                if(response.status == 200){ 
                    alert("Receipt deleted Successfully!")
                    this.list_member_payments(this.receiptData.paymentType);
                }else{
                    alert("Problem")
                }
            }).catch((error) => {
                alert(error.data)
            })
        }
    }
}, 
created(){
    this.getLoanPurposeList()
}
    
}
</script>