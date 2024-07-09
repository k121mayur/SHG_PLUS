<template>
    <div class="container" style="overflow: auto">
        <form @submit.prevent="addOtherReceipt">

            <div class="d-flex flex-row flex-wrap">

                <label for="transactionType" class="form-label m-3">Select Receipt Type</label>
                <select class="form-select m-3" @change="fetchAccounts" id="transactionType"
                    v-model="receiptData.transactionType" style="width: max-content;">
                    <option value="0">Loan</option>
                    <option value="1">Withdrawal from Savings Account</option>
                </select>

                <label for="loanAccount" class="form-label m-3" v-if="receiptData.transactionType === '0'">Select Loan
                    Account</label>
                <select class="form-select m-3" id="loanAccount" v-model="receiptData.loanAccountId"
                    style="width: max-content;" v-if="receiptData.transactionType === '0'" required>
                    <option v-for="account in Account_list" :value="account.id">{{ account.bank_name }}-{{
                        account.account_number }}</option>
                    <option value="0">New Account</option>
                </select>
                <!-- <div> Balance : </div> -->

                <div class="mb-3 col-md-6" v-if="receiptData.transactionType === '0'">
                    <label for="loan" class="form-label"> Loan Type </label>
                    <select class="form-select mx-3" id="loan" v-model="receiptData.loanType" required>
                        <option value="CC">CC Loan</option>
                        <option value="Term">Term Loan</option>
                    </select>
                </div>

                <div class="mb-3 col-md-6" v-if="receiptData.transactionType === '0'">
                    <label for="loan" class="form-label"> Loan Amount </label>
                    <input type="number" class="form-control short mx-3" id="loan" v-model="receiptData.loanAmount"
                        required min="1000">
                </div>



                <div class="mb-3 col-md-6" v-if="receiptData.transactionType === '0'">
                    <label for="tenure" class="form-label"> Tenure (in months)</label>
                    <input type="number" class="form-control short mx-3" id="tenure" min="1" max="12"
                        v-model="receiptData.tenure">
                </div>

                <div class="mb-3 col-md-6" v-if="receiptData.transactionType === '0'">
                    <label for="tenure" class="form-label"> Interest Rate (in %)</label>
                    <input type="number" class="form-control short mx-3" id="tenure" min="1" max="24"
                        v-model="receiptData.interestRate">
                </div>

                <label for="savingsAccount" class="form-label m-3" v-if="receiptData.transactionType === '1'">Select
                    Savings Account</label>
                <select class="form-select m-3" id="savingsAccount" v-model="receiptData.savingsAccountId"
                    style="width: max-content;" v-if="receiptData.transactionType === '1'">
                    <option v-for="account in Account_list" :value="account.id">{{ account.bank_name }}-{{
                        account.account_number }}</option>
                </select>

                <div class="mb-3 col-md-12 " v-if="receiptData.transactionType == 1">
                    <label for="interestDate" class="form-label">Date of Withdrawal</label>
                    <input type="date" :max="new Date().toISOString().split('T')[0]" class="form-control short mx-3" id="interestDate"
                        v-model="receiptData.withdrawalDate">
                </div>

                <div class="mb-3 col-md-12" v-if="receiptData.transactionType == 1">
                    <label for="withdrawalAmount" class="form-label">Amount</label>
                    <input type="number" class="form-control short mx-3" id="withdrawalAmount"
                        v-model="receiptData.withdrawalAmount">
                </div>
            </div>
            <div class="d-flex flex-row justify-content-center align-items-center">
                <button type="submit" class="btn btn-primary" v-if="receiptData.transactionType">Submit</button>
                <div class="btn btn-warning m-3" v-if="receiptData.loanAccountId === '0'" @click="toggle_loan_account_form()"> Add Loan Account </div>
            </div>
            <div>
                <div v-if="show_loan_account_form" style="position: absolute;    top: 0%;    left: 0%;    width: 100%;    height: 110%;    background-color: white;    z-index: 1">
                    <form @submit.prevent="addLoanAccount">
                        <h2 class="text-center m-3">Add Loan Account</h2>
                        <div class="mb-3 d-flex justify-content-start" style="margin-left: 10%; margin-top: 2%;">
                            <label for="bankName" class="form-label">Bank Name</label>
                            <input type="text" class="form-control short mx-3" id="bankName"   v-model="new_loan_account.bank_name">
                        </div>
                        
                        <div class="mb-3 d-flex justify-content-start" style="margin-left: 10%; margin-top: 2%;">
                            <label for="branchName" class="form-label">Branch Name</label>
                            <input type="text" class="form-control short mx-3" id="branchName"   v-model="new_loan_account.branch_name">
                        </div>
                        
                        <div class="mb-3 d-flex justify-content-start" style="margin-left: 10%; margin-top: 2%;">
                            <label for="accountName" class="form-label">Account Name</label>
                            <input type="text" class="form-control short mx-3" id="accountName"   v-model="new_loan_account.account_name">
                        </div>
                        <div class="mb-3 d-flex justify-content-start" style="margin-left: 10%; margin-top: 2%;">
                            <label for="accountNumber" class="form-label">Account Number</label>
                            <input type="text" class="form-control short mx-3" id="accountNumber"   v-model="new_loan_account.account_number">
                        </div>
                        <div class="mb-3 d-flex justify-content-start" style="margin-left: 10%; margin-top: 2%;">
                            <label for="accountNumber" class="form-label">Confirm Account Number</label>
                            <input type="text" class="form-control short mx-3" id="accountNumber"   v-model="new_loan_account.confirm_account_number">
                        </div>
                        <div class="mb-3 d-flex justify-content-start" style="margin-left: 10%; margin-top: 2%;">
                            <label for="ifscCode" class="form-label">IFSC Code</label>
                            <input type="text" class="form-control short mx-3" id="ifscCode"   v-model="new_loan_account.ifsc_code">
                        </div>
                        
                        <div class="mb-3 d-flex justify-content-start" style="margin-left: 10%; ">    
                            <button type="button" class="btn btn-primary" @click="addLoanAccount()" v-if="new_loan_account.account_number === new_loan_account.confirm_account_number">Add Account</button>
                        </div>
                    </form>
                </div>   
            </div>
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
    name: 'otherReceiptForm',
    props: {
        meeting_id: {
            type: Number,
            required: true
        },

        members_list: {
            type: Array,
            required: false
        }

    },
    data() {
        return {
            shg_id: null,
            Account_list: [],
            show_loan_account_form: false,
            new_loan_account: {
                account_number: '',
                account_name: '',
                confirm_account_number: '',
                ifsc_code: '',
                branch_name: ''
            },
            receiptData: {
                meeting_id: this.meeting_id,
                transactionType: '',
                loanAccountId: '',
                loanType: '',
                loanAmount: 0,
                tenure: 0,
                interestRate: 0,

                savingsAccountId: '',
                withdrawalDate: '',
                withdrawalAmount: 0
            },



        }
    },
    methods: {
        addOtherReceipt() {
            console.log("Other receipt function is called")
            console.log(this.receiptData.transactionType)
            if (this.receiptData.transactionType === '0') {
                if (this.receiptData.loanAccountId === '0') {
                    alert("Please select Loan Account")
                    return
                }
                axios.post('/api/v1/otherLoanReceipts', this.receiptData, { headers: { 'Token': localStorage.getItem('token') } }).then((response) => {
                    if (response.status == 200) {
                        this.receiptData.transactionType = ''
                        this.receiptData.loanAccountId = ''
                        this.receiptData.loanAmount = 0
                        this.receiptData.loanType = ''
                        this.receiptData.tenure = 0
                        this.receiptData.interestRate = 0

                        
                        alert("Receipt added Successfully!")

                    } else {
                        alert("Problem")
                    }
                }).catch((error) => {
                    alert(error.data)
                })
            } else if (this.receiptData.transactionType === '1') {
                console.log(this.transactionType)
                axios.post('/api/v1/otherSavingsReceipts', this.receiptData, { headers: { 'Token': localStorage.getItem('token') } }).then((response) => {
                    if (response.status == 200) {
                        this.receiptData.savingsAccountId = ''
                        this.receiptData.withdrawalDate = ''
                        this.receiptData.withdrawalAmount = 0
                    }
            })}
        },

                    fetchAccounts() {
                    //here the idea is to fetch the list of loan accounts from the server using meeting id to identify the SHG Id
                    axios.get('/api/v1/ShgAccount/' + this.shg_id + '/' + this.receiptData.transactionType, { headers: { 'Token': localStorage.getItem('token') } }).then((response) => {
                        this.Account_list = response.data
                    }).catch((error) => {
                        alert(error.data)
                    })
                },

                    fetchShgId() {
                    axios.get('/shgID/' + this.meeting_id, { headers: { 'Token': localStorage.getItem('token') } }).then((response) => {
                        console.log(response.data.shg_id)
                        this.shg_id = response.data.shg_id
                    })
                }, 

                toggle_loan_account_form() {
                    this.show_loan_account_form = !this.show_loan_account_form
                }
            },

            created(){
                this.fetchShgId()
            }
        }
</script>