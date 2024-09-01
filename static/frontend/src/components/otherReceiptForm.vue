<template>
    <div class="container" style="overflow: auto">
        <form @submit.prevent="addOtherReceipt">

            <div class="d-flex flex-row flex-wrap">

                <label for="transactionType" class="form-label my-1 mx-2">Select Receipt Type</label>
                <select class="form-select m-3" @change="fetchAccounts" id="transactionType"
                    v-model="receiptData.transactionType" style="width: max-content;">
                    <option value="0">Loan</option>
                    <option value="1">Withdrawal from Savings Account</option>
                    <option value="2">Cash in Box</option>
                </select>
                <div class="mb-3 col-md-7 mx-0 my-0"> 
                    <label for="loanAccount" class="form-label my-3 mx-1" v-if="receiptData.transactionType === '0'">Select Loan
                        Account</label>
                    <select class="form-select my-3" id="loanAccount" v-model="receiptData.loanAccountId"
                        style="width: max-content;" v-if="receiptData.transactionType === '0'" required>
                        <option v-for="account in Account_list" :value="account.id">{{ account.bank_name }}-{{
                            account.account_number }}</option>
                        <option value="0">New Account</option>
                    </select>
                </div>
                <!-- <div> Balance : </div> -->

                <div class="mb-3 col-md-5" v-if="receiptData.transactionType === '0'">
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

                <div class="mb-3 col-md-6 d-flex flex-row justify-content-end" v-if="receiptData.transactionType === '0'">
                    <label for="loan" class="form-label"> Loan Date </label>
                    <input type="date" class="form-control mx-3 col-md-8" id="loan" v-model="receiptData.loanDate"
                    :max="new Date().toISOString().split('T')[0]" required>
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
                <div v-if="receiptData.transactionType == 2">
                    <!-- <div class="mb-3 d-flex justify-content-start" style="margin-left: 10%; margin-top: 5%;">
                        <label for="memberName" class="form-label col-md-4">Member Name</label>
                        <select class="form-select mx-3" id="memberName" v-model="receiptData.member_id" style="width: max-content;">
                            <option v-for="member in members_list" :value="member.value">{{member.name}}</option>
                        </select>

            <!-- <input type="text" class="form-control" id="memberName" v-model="receiptData.member_name" required> -->
                    <!-- </div> -->
                    <div class="mb-3 d-flex justify-content-start">
                        <label for="withdrawalAmount" class="form-label col-md-5">Amount</label>
                        <input type="number" min="1" class="form-control short mx-3" id="withdrawalAmount"
                            v-model="receiptData.cash_in_hand_amt">
                    </div>
                </div>


            </div>
            <div class="d-flex flex-row justify-content-center align-items-center">
                <button type="submit" class="btn btn-primary" v-if="receiptData.transactionType">Submit</button>
                <button type="button" class="btn btn-warning mx-3" v-if="receiptData.transactionType" @click="list_other_recipts(receiptData.transactionType)">List</button>
                <div class="btn btn-info m-3 text-light" v-if="receiptData.loanAccountId === '0'" @click="toggle_loan_account_form()"> Add Loan Account </div>
            </div>
            <div>
                <div v-if="show_loan_account_form" style="position: absolute;    top: 0%;    left: 0%;    width: 100%;    height: 110%;    background-color: white;    z-index: 1">
                    <form @submit.prevent="addLoanAccount">
                        
                        <h3 class="text-center bg-dark p-3 text-light rounded-3">Add Loan Account</h3>
                        <div class="d-flex flex-row-reverse">
                            <button class="btn btn-danger" @click="toggle_loan_account_form">Close</button>
                        </div>
                        <div class="mb-3 d-flex justify-content-start" style="margin-left: 10%; margin-top: 2%;">
                            <label for="bankName" class="form-label">Bank Name</label>
                            <input type="text" class="form-control mx-3" id="bankName"   v-model="new_loan_account.bank_name" required>
                        </div>
                        
                        <div class="mb-3 d-flex justify-content-start" style="margin-left: 10%; margin-top: 2%;">
                            <label for="branchName" class="form-label">Branch Name</label>
                            <input type="text" class="form-control short mx-3" id="branchName"   v-model="new_loan_account.branch_name" required>
                        </div>
                        
                        <!-- <div class="mb-3 d-flex justify-content-start" style="margin-left: 10%; margin-top: 2%;">
                            <label for="accountName" class="form-label">Account Name</label>
                            <input type="text" class="form-control short mx-3" id="accountName"   v-model="new_loan_account.account_name">
                        </div> -->
                        <div class="mb-3 d-flex justify-content-start" style="margin-left: 10%; margin-top: 2%;">
                            <label for="accountNumber" class="form-label">Account Number</label>
                            <input type="text" class="form-control  mx-3" id="accountNumber"   v-model="new_loan_account.account_number" required>
                        </div>
                        <div class="mb-3 d-flex justify-content-start" style="margin-left: 10%; margin-top: 2%;">
                            <label for="accountNumber" class="form-label">Confirm Account Number</label>
                            <input type="text" class="form-control mx-3" id="accountNumber"   v-model="new_loan_account.confirm_account_number" placeholder="Must match with Account Number" required >
                        </div>
                        <div class="mb-3 d-flex justify-content-start" style="margin-left: 10%; margin-top: 2%;">
                            <label for="ifscCode" class="form-label">IFSC Code</label>
                            <input type="text" class="form-control  mx-3" id="ifscCode"   v-model="new_loan_account.ifsc_code"required >
                        </div>
                        
                        <div class="mb-3 d-flex justify-content-start" style="margin-left: 10%; ">    
                            <button type="button" class="btn btn-primary" @click="addLoanAccount()" v-if="new_loan_account.account_number === new_loan_account.confirm_account_number">Add Account</button>
                        </div>
                    </form>
                </div> 
                <div v-if="toggle_other_receipt " >
                    <div style="position: absolute;    top: 0%;    left: 0%;    width: 100%;    height: 100%;    background-color: white;    z-index: 4;" v-if="receiptData.transactionType == 0 && this.loan_receipt_list.length > 0">
                        <div class="d-flex justify-content-end"><button class="btn btn-danger" @click="toggle_other_receipt = false">Close</button></div>
                        <h2>Loan Receipts</h2>
                        <table class="table table-bordered table-striped">
                            <thead>
                                <tr>
                                    <th>Sr. No.</th>
                                    <th>Bank Name</th>
                                    <th>Loan Amount</th>
                                    <th>Loan Tenure</th>
                                    <th>Interest Rate</th>
                                    <th>Action</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr v-for="(loan, index) in loan_receipt_list">
                                    <td>{{ index + 1 }}</td>
                                    <td>{{ loan.bank }}</td>
                                    <td>Rs.{{ loan.loanAmount }}/-</td>
                                    <td>{{ loan.tenure }} Months</td>
                                    <td>{{ loan.interestRate }}%</td>
                                    <td><button class="btn btn-primary" @click="deleteLoanReceipt(loan.id)">Delete</button></td>
                                </tr>
                            </tbody>
                        </table>
                    </div>

                    <div style="position: absolute;    top: 0%;    left: 0%;    width: 100%;    height: 100%;    background-color: white;    z-index: 4;" v-if="receiptData.transactionType == 1 && this.saving_receipt_list.length > 0">
                        <div class="d-flex justify-content-end"><button class="btn btn-danger" @click="toggle_other_receipt = false">Close</button></div>
                        <h2>Savings Withdrawals</h2>
                        <table class="table table-bordered table-striped">
                            <thead>
                                <tr>
                                    <th>Sr. No.</th>
                                    <th>Bank Name</th>
                                    <th>Withdrawal Date</th>
                                    <th>Amount</th>
                                    <th>Action</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr v-for="(s, index) in saving_receipt_list">
                                    <td>{{ index + 1 }}</td>
                                    <td>{{ s.bank }}</td>
                                    <td>{{ s.withdrawalDate }}</td>
                                    <td>Rs.{{ s.withdrawalAmount }} /-</td>
                                    <td><button class="btn btn-primary" @click.prevent="deleteSavingReceipt(s.id)">Delete</button></td>
                                </tr>
                            </tbody>
                        </table>
                    </div>


                    <div style="position: absolute;    top: 0%;    left: 0%;    width: 100%;    height: 100%;    background-color: white;    z-index: 4;" v-if="receiptData.transactionType == 2 && this.cash_in_hand_receipt_list.length > 0">
                        <div class="d-flex justify-content-end"><button class="btn btn-danger" @click="toggle_other_receipt = false">Close</button></div>
                        <h2>Cash in Hand Receipts</h2>
                        <table class="table table-bordered table-striped">
                            <thead>
                                <tr>
                                    <th>Sr. No.</th>
                                    <th>Member Name</th>
                                    <th>Amount</th>
                                    <th>Action</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr v-for="(s, index) in cash_in_hand_receipt_list">
                                    <td>{{ index + 1 }}</td>
                                    <td>{{ s.memberName }}</td>
                                    <td>Rs.{{ s.amount }} /-</td>
                                    <td><button class="btn btn-primary" @click.prevent="deleteCashInHandReceipt(s.id)">Delete</button></td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                    
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
            toggle_other_receipt: false,
            loan_receipt_list: [],
            saving_receipt_list: [],
            cash_in_hand_receipt_list: [],
            show_loan_account_form: false,
            new_loan_account: {
                account_number: '',
                account_name: '',
                confirm_account_number: '',
                ifsc_code: '',
                branch_name: '',
                bank_name: '',
                shg_id: localStorage.getItem('shg_id'),
                account_type: 'loan'
            },
            receiptData: {
                meeting_id: this.meeting_id,
                transactionType: '',
                loanAccountId: '',
                loanType: '',
                loanAmount: 0,
                loanDate: '',
                tenure: 0,
                interestRate: 0,

                savingsAccountId: '',
                withdrawalDate: '',
                withdrawalAmount: 0, 

                member_id : null,
                cash_in_hand_amt : 0
            },



        }
    },
    methods: {
        addOtherReceipt() {
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
            })} else if (this.receiptData.transactionType === '2') {
                axios.post('/api/v1/otherCashInHandReceipts', this.receiptData, { headers: { 'Token': localStorage.getItem('token') } }).then((response) => {
                    if (response.status == 200) {
                        this.receiptData.member_id = null,
                        this.receiptData.cash_in_hand_amt = 0
                        alert(response.data.message)
                    }
                }).catch((error) => {
                    alert(error.data)
                })
        } },

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
                        localStorage.setItem('shg_id', response.data.shg_id)
                    })
                }, 

                toggle_loan_account_form() {
                    this.show_loan_account_form = !this.show_loan_account_form
                }, 

                addLoanAccount(){
                    axios.post('/api/v1/ShgAccount', this.new_loan_account, { headers: { 'Token': localStorage.getItem('token') } }).then((response) => {
                        if (response.status == 200) {
                            
                            alert("Loan Account added Successfully!");
                            this.toggle_loan_account_form();
                            this.fetchAccounts()
                        }
                    }).catch((error) => {
                        alert(error.data)
                    })
                },

                list_other_recipts(t_id) {
                    
                    if (t_id == 0) {
                        axios.get('/api/v1/otherLoanReceipts/' + this.meeting_id, { headers: { 'Token': localStorage.getItem('token') } }).then((response) => {
                            this.loan_receipt_list = response.data
                            if (this.loan_receipt_list.length == 0) {
                                alert("No receipts found")
                            } else {
                                this.toggle_other_receipt = true
                            }
                        }).catch((error) => {
                            alert(error.data)
                        })
                        } else if (t_id == 1) {
                        axios.get('/api/v1/otherSavingsReceipts/' + this.meeting_id, { headers: { 'Token': localStorage.getItem('token') } }).then((response) => {
                            this.saving_receipt_list = response.data
                            if (this.saving_receipt_list.length == 0) {
                                alert("No receipts found")
                            } else {
                                this.toggle_other_receipt = true
                            }
                        }).catch((error) => {
                            alert(error.data)
                        })
                    } else if (t_id == 2) {
                        axios.get('/api/v1/otherCashInHandReceipts/' + this.meeting_id, { headers: { 'Token': localStorage.getItem('token') } }).then((response) => {

                            this.cash_in_hand_receipt_list = response.data
                            if (this.cash_in_hand_receipt_list.length == 0) {
                                alert("No receipts found")
                            } else {
                                this.toggle_other_receipt = true
                            }})
                    }
                }, 
                 deleteLoanReceipt(id) {
                    axios.delete('/api/v1/otherLoanReceipts', { headers: { 'Token': localStorage.getItem('token') }, data: {"id": id} }).then((response) => {
                        if (response.status == 200) {
                            alert("Receipt deleted Successfully!")
                            this.toggle_other_receipt = false
                        } else {
                            alert("Problem Occured While Deleting Receipt!")
                        }
                    }).catch((error) => {
                        alert(error.data)
                    })

                }, 

                deleteSavingReceipt(id) {
                    axios.delete('/api/v1/otherSavingsReceipts', { headers: { 'Token': localStorage.getItem('token') }, data: {"id": id} }).then((response) => {
                        if (response.status == 200) {
                            alert("Receipt deleted Successfully!")
                            this.toggle_other_receipt = false
                        } else {
                            alert("Problem Occured While Deleting Receipt!")
                        }
                    }).catch((error) => {
                        alert(error.data)
                    })
                }, 

                deleteCashInHandReceipt(id) {
                    axios.delete('/api/v1/otherCashInHandReceipts', { headers: { 'Token': localStorage.getItem('token') }, data: {"id": id} }).then((response) => {
                        if (response.status == 200) {
                            alert("Receipt deleted Successfully!")
                            this.toggle_other_receipt = false
                        } else {
                            alert("Problem Occured While Deleting Receipt!")
                        }
                    }).catch((error) => {
                        alert(error.data)
                    })
                },

            },

            mounted() {
                this.fetchShgId()
            }
        }
</script>