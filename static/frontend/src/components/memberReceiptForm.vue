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
        <div class="d-flex flex-row flex-wrap" >
            <div class="mb-3 col-md-6">
                <label for="savings" class="form-label">Savings</label>
                <input type="number" class="form-control short mx-3" id="savings" v-model="receiptData.savings">
            </div>
            <div class="mb-3 col-md-6 ">
                <label for="principal" class="form-label">Principal</label>
                <input type="number" class="form-control short mx-3" id="principal" v-model="receiptData.principal">
            </div>
            <div class="mb-3 col-md-6">
                <label for="interest" class="form-label">Interest</label>
                <input type="number" class="form-control short mx-3" id="interest" v-model="receiptData.interest">
            </div>
            <div class="mb-3 col-md-6">
                <label for="fine" class="form-label">Fine</label>
                <input type="number" class="form-control short mx-3" id="fine" v-model="receiptData.fine">
            </div>
        </div>
        <button type="submit" class="btn btn-primary">Submit</button>
        <button type="button" class="btn btn-warning m-1" @click="list_member_recipts()">List</button>
        </form>
    </div>
    <div v-if="toggle_receipts_list " class="receipts_list" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; background-color: white;" >
        
    <h1> Receipts List </h1>
    <table class="table table-hover table-responsive" style="overflow: auto;">
        <thead>
            <tr>
                <th>Member Name</th>
                <th>Savings</th>
                <th>Principal</th>
                <th>Interest</th>
                <th>Fine</th>
                <th>Action</th>
            </tr>
        </thead>
        <tbody>
            <tr v-for="receipt in receipts_list">
                <td>{{ receipt.name }}</td>
                <td>{{ receipt.savings[0]}}</td>
                <td>{{ receipt.principal[0] }}</td>
                <td>{{ receipt.interest[0] }}</td>
                <td>{{ receipt.fine[0] }}</td>
                <td><button class="btn btn-primary" @click="delte_receipt(receipt.savings[1], receipt.principal[1], receipt.interest[1], receipt.fine[1], receipt.id)">Delete</button></td>
            </tr>
        </tbody>
    </table>
    
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
    name: 'memberReceiptForm', 
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
            meeting_id: this.meeting_id,
            member_id: '',
            receipt_date: '',
            receipt_amount: 0,
            savings: 0,
            principal: 0,
            interest: 0,
            fine: 0 
        }, 
        receipts_list: false,
        toggle_receipts_list: false
    }
    },
    methods : {
        submitForm() { 
            if (this.receiptData.member_id == '') {
                alert("Please select member")
            }else if( this.receiptData.savings == 0 && this.receiptData.principal == 0 && this.receiptData.interest == 0 && this.receiptData.fine == 0 ){
                alert("Please enter receipt amount")
            } else{
            axios.post('/api/v1/memberReceipt', this.receiptData ,  { headers:{ 'Token': localStorage.getItem('token') } } ).then((response) => {
                if(response.status == 200){
                    this.receiptData.savings = 0
                    this.receiptData.principal = 0
                    this.receiptData.interest = 0 
                    this.receiptData.fine = 0
                    alert(response.data.message)
                }else{
                    alert("Problem")
                }
            }).catch((error) => {
                alert(error.data)
            })
        }
    },
    list_member_recipts() {
        axios.get('/api/v1/memberReceipts/' + this.meeting_id ,  { headers:{ 'Token': localStorage.getItem('token') } } ).then((response) => {
            if (response.data.length == 0) {
                alert("No receipts found")
            }else{
                this.toggle_receipts_list = true;
                this.receipts_list = response.data
            }
            
    })
    }, 

    delte_receipt(savings, principal, interest, fine, mem_id) {
        axios.delete('/api/v1/memberReceipt',  { headers:{ 'Token': localStorage.getItem('token') },
         data: {savings: savings, principal: principal, interest: interest, fine: fine, member_id: mem_id} } ).then((response) => {
            if(response.status == 200){
                alert(response.data.message)
                this.list_member_recipts()
            }else{
                alert("Problem")
            }
        })  
    }
}
}
</script>