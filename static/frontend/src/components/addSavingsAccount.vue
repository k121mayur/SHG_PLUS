<template>
    <div class="container compressed-form">
      <div class="card p-1" style="background-color: bisque;">
        <form @submit.prevent="addLoanAccount">
  
          <!-- SHG Selection -->
          <div class="form-group row align-items-center">
            <label for="shg" class="col-4 col-form-label text-right">SHG</label>
            <div class="col-7">
              <VueMultiselect 
                id="shg"
                class="form-control-sm w-100"
                label="name"
                :options="shg_list"
                v-model="shg_name"
                placeholder="Select SHG">
              </VueMultiselect>
            </div>
          </div>
  
          <!-- Bank Name -->
          <div class="form-group row my-1">
            <label for="bankName" class="col-4 col-form-label text-right pr-1">Bank Name</label>
            <div class="col-8">
              <input 
                type="text"
                class="w-100 form-control-sm"
                id="bankName"
                v-model="new_loan_account.bank_name"
                required
                placeholder="Enter Bank Name">
            </div>
          </div>
  
          <!-- Branch Name -->
          <div class="form-group row my-1">
            <label for="branchName" class="col-4 col-form-label text-right pr-1">Branch</label>
            <div class="col-8">
              <input 
                type="text"
                class="w-100 form-control-sm"
                id="branchName"
                v-model="new_loan_account.branch_name"
                required
                placeholder="Branch Name">
            </div>
          </div>
  
          <!-- Account Number -->
          <div class="form-group row my-1">
            <label for="accountNumber" class="col-4 col-form-label text-right pr-1">Account No.</label>
            <div class="col-8">
              <input 
                type="text"
                class="w-100 form-control-sm"
                id="accountNumber"
                v-model="new_loan_account.account_number"
                required
                placeholder="Account Number">
            </div>
          </div>
  
          <!-- Confirm Account Number -->
          <div class="form-group row my-1">
            <label for="confirmAccountNumber" class="col-4 col-form-label text-right pr-1">Confirm A/c No</label>
            <div class="col-8">
              <input 
                type="text"
                class="w-100 form-control-sm"
                id="confirmAccountNumber"
                v-model="new_loan_account.confirm_account_number"
                required
                placeholder="Confirm Account Number">
              <small v-if="new_loan_account.account_number !== new_loan_account.confirm_account_number && new_loan_account.confirm_account_number" class="text-danger">
                Numbers don't match.
              </small>
            </div>
          </div>
  
          <!-- IFSC Code -->
          <div class="form-group row my-1">
            <label for="ifscCode" class="col-4 col-form-label text-right pr-1">IFSC</label>
            <div class="col-8">
              <input 
                type="text"
                minlength="11"
                maxlength="11"
                class="form-control-sm w-100 form-control-light-outline"
                id="ifscCode"
                v-model="new_loan_account.ifsc_code"
                required
                placeholder="IFSC Code">
            </div>
          </div>
  
          <!-- Submit Button -->
          <div class="form-group row my-1">
            <div class="col-8 offset-2 my-2">
              <button 
                type="submit" 
                :class=" new_loan_account.account_number !== new_loan_account.confirm_account_number ? 'btn btn-sm btn-dark w-100' : 'btn btn-sm btn-primary w-100' "
                :disabled="new_loan_account.account_number !== new_loan_account.confirm_account_number">
                Add Account
              </button>
            </div>
          </div>
  
          <!-- Info message -->
          <div class="form-group row my-1">
            <div class="col-12 text-center">
              <small v-if="!new_loan_account.account_number" class="text-danger">
                <strong>Enter Account Number to add Bank Account.</strong>
              </small>
            </div>
          </div>
  
        </form>
      </div>
    </div>
  </template>
  
  

<script>
import axios from 'axios'
import VueMultiselect from 'vue-multiselect'

export default {
    name: 'addSavingsAccount',

    components: {
        VueMultiselect
    },
    data() {
        return {
            shg_list: [],
            shg_name: null,
            new_loan_account: {
                account_number: '',
                account_name: '',
                account_type: 'savings',
                bank_name: '',
                branch_name: '',
                ifsc_code: '',
                shg_id: null
            }
        }
    },

    methods: {
        fetchSHG() {
            axios.get('/api/v1/shg', { headers: { 'Token': localStorage.getItem('token') } }).then((response) => {
                this.shg_list = response.data
                if (this.shg_list.length == 0) {
                    alert('No SHG found. Please add SHG first')
                }
            })
        },
        addLoanAccount() {
            this.new_loan_account.shg_id = this.shg_name.value
            axios.post('/api/v1/ShgAccount', this.new_loan_account, { headers: { 'Token': localStorage.getItem('token') } }).then((response) => {
                if (response.status == 200) {

                    alert("Savings Account added Successfully!");
                    this.new_loan_account ={
                account_number: '',
                account_name: '',
                account_type: 'loan',
                bank_name: '',
                branch_name: '',
                ifsc_code: '',
                shg_id: null
            }
                }
            }).catch((error) => {
                alert(error.data)
            })
        }


    },
    mounted() {
        this.fetchSHG()
    }
}
</script>

<style scoped>
.compressed-form {
  max-width: 400px;
  margin: auto;
  background-color: #f7f7f7;
}

.card {
  background-color: #fff;
  border-radius: 8px;
  padding: 15px;
}

.form-control-sm {
  font-size: 0.875rem;
  padding: 5px 10px;
  border-radius: 4px;
}

.btn-sm {
  padding: 6px 12px;
  font-size: 0.875rem;
}

label {
  font-size: 0.875rem;
  padding-top: 5px;
}

small {
  font-size: 0.75rem;
}


</style>