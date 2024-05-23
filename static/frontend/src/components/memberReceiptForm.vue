<template>
    <div class="container" style="overflow: auto">
        <form @submit.prevent="submitForm">
        <div class="mb-3 d-flex justify-content-start" style="margin-left: 10%; margin-top: 5%;">
            <label for="memberName" class="form-label">Member Name</label>
            <select class="form-select mx-3" id="memberName" v-model="receiptData.member_name" style="width: max-content;">
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
            member_name: '',
            receipt_date: '',
            receipt_amount: 0,
            savings: 0,
            principal: 0,
            interest: 0,
            fine: 0
        }
    }
    },
    methods : {
        submitForm() {  
            axios.post('/api/v1/memberReceipt', this.receiptData ,  { headers:{ 'Token': localStorage.getItem('token') } } ).then((response) => {
                if(response.status == 200){
                    alert("Receipt added Successfully!")
                }else{
                    alert("Problem")
                }
            }).catch((error) => {
                alert(error.data)
            })
    }
    }
}
</script>