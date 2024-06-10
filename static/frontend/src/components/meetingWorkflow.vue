<template>
    <div class="container" >
        <h1 
        class="mb-3 mx-0 p-3"
        style="background-color: bisque; width: 100%; text-align: center; border-radius: 10px;"
        > Meeting Workflow</h1>
        <div class="d-flex flex-row flex-wrap" style="width: 100%;">
            <div 
                @click="toggleMemberReceiptsForm()"
                class="border col-md-4 d-flex flex-row justify-content-center align-items-center" 
                style="height: 25vh; text-align: center; border-radius: 10px; background-color: green; color: white; "> 
                <h4>Member Receipts</h4>
            </div>

            <div
                @click="toggleOtherReceiptsForm()" 
                class="border col-md-4 d-flex flex-row justify-content-center align-items-center" 
                style="height: 25vh; text-align: center; border-radius: 10px; background-color: green; color: white; "> 
                <h4>Other Receipts</h4>
            </div>

            <div
                @click="toggleMemberPaymentsForm()" 
                class="border col-md-4 d-flex flex-row justify-content-center align-items-center" 
                style="height: 25vh; text-align: center; border-radius: 10px; background-color: green; color: white; "> 
                <h4>Member Payments</h4>
            </div>

            <div 
            @click="toggleOtherPaymentsForm()"
                class="border col-md-4 d-flex flex-row justify-content-center align-items-center my-3" 
                style="height: 25vh; margin-left: 10%; text-align: center; border-radius: 10px; background-color: green; color: white; "> 
                <h4>Other Payments</h4>
            </div>

            <!-- <div 
                class="border col-md-4 d-flex flex-row justify-content-center align-items-center my-3" 
                style="height: 25vh; margin-left: 10%; text-align: center; border-radius: 10px; background-color: green; color: white; "> 
                <h4>Member Payments</h4>
            </div> -->
        </div>

        <div class="m-3 border p-2"> 
            <h3>Meeting Status :</h3> 
        </div>

        <div v-if ="memberReceiptsForm" style="position: absolute; top:24%; width: inherit; height: inherit; background-color: white; z-index: 1">
            <a @click="toggleMemberReceiptsForm()" class="close" style="margin-left: 60%; margin-top: 20%;">Close</a>
            <div   
            style="position: absolute; top: 12%; left: 20%; background-color: white; width: 60%; 
                    height: 60%; border-radius: 10px; z-index: 2; border: solid 1px black; overflow: auto">
                    
                <h1 style="border-bottom: solid 1px black; padding: 1%;">Member Receipts </h1> 
                <memberReceiptForm :meeting_id = "meeting_id" :members_list = "members_list">
                </memberReceiptForm>
            </div>
        </div>

        <div v-if ="otherReceiptForm" style="position: absolute; top:24%; width: inherit; height: inherit; background-color: white; z-index: 1">
            <a @click="toggleOtherReceiptsForm()" class="close" style="margin-left: 60%; margin-top: 20%;">Close</a>
            <div   
            style="position: absolute; top: 12%; left: 20%; background-color: white; width: 60%; 
                    height: 70%; border-radius: 10px; z-index: 2; border: solid 1px black; overflow: auto">
                <h1 style="border-bottom: solid 1px black; padding: 1%;">Other Receipts </h1> 
                <otherReceiptForm :meeting_id = "meeting_id" :members_list = "members_list">
                </otherReceiptForm>
            </div>
        </div>

        <div v-if ="memberPaymentsForm" style="position: absolute; top:24%; width: inherit; height: inherit; background-color: white; z-index: 1">
            <a @click="toggleMemberPaymentsForm()" class="close" style="margin-left: 60%; margin-top: 20%;">Close</a>
            <div   
            style="position: absolute; top: 12%; left: 20%; background-color: white; width: 60%; 
                    height: 60%; border-radius: 10px; z-index: 2; border: solid 1px black; overflow: auto">
                    
                <h1 style="border-bottom: solid 1px black; padding: 1%;">Member Payments </h1> 
                <memberPaymentForm :meeting_id = "meeting_id" :members_list = "members_list">
                </memberPaymentForm>
            </div>
        </div>

        <div v-if ="otherPaymentsForm" style="position: absolute; top:24%; width: inherit; height: inherit; background-color: white; z-index: 1">
            <a @click="toggleOtherPaymentsForm()" class="close" style="margin-left: 60%; margin-top: 20%;">Close</a>
            <div   
            style="position: absolute; top: 12%; left: 20%; background-color: white; width: 60%; 
                    height: 60%; border-radius: 10px; z-index: 2; border: solid 1px black; overflow: auto">
                    
                <h1 style="border-bottom: solid 1px black; padding: 1%;">Other Payments </h1> 
                <otherPaymentForm :meeting_id = "meeting_id" :members_list = "members_list">
                </otherPaymentForm>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios'

import memberReceiptForm from '@/components/memberReceiptForm.vue'
import otherReceiptForm from '@/components/otherReceiptForm.vue'
import memberPaymentForm from '@/components/memberPaymentForm.vue'
import otherPaymentForm from '@/components/otherPaymentForm.vue'


export default {
    name: 'meetingWorkflow',
    components :{
        memberReceiptForm, 
        otherReceiptForm,
        memberPaymentForm,
        otherPaymentForm
    },
    data() {
        return {
            meeting_id: this.$route.params.meeting_id,
            memberReceiptsForm: false,
            otherReceiptForm : false, 
            memberPaymentsForm : false, 
            otherPaymentsForm : false, 

            members_list: []
        }
    },
    methods: {
        toggleMemberReceiptsForm() {
            console.log(this.memberReceiptsForm)

            this.memberReceiptsForm = !this.memberReceiptsForm
        },

        toggleOtherReceiptsForm() {
            console.log("Function Called")
            this.otherReceiptForm = !this.otherReceiptForm
        },

        toggleMemberPaymentsForm(){
            this.memberPaymentsForm = !this.memberPaymentsForm
        },
        toggleOtherPaymentsForm(){
            this.otherPaymentsForm = !this.otherPaymentsForm
        },

        fetchMembers(meeting_id){
            axios.get('/api/v1/meeting/member/' + this.meeting_id,  {headers: { 'Token': localStorage.getItem('token') }} ).then((response) => {
                this.members_list = response.data
        })
    }, 
    

},
mounted() {
        console.log(this.meeting_id)
        this.fetchMembers(this.meeting_id)
    }
}
</script>

<style>

</style>