<template>
    <div>
        <h1 class="text-center bg-success p-3 text-light rounded-3">Shareout Report</h1>
        <div>
            <form @submit.prevent="fetchGroupReport"> 
                <div class="d-flex flex-row align-items-center justify-content-center">
                    <label for="shg" class="m-3">Select SHG</label>
                    <VueMultiselect
                    @focusout="fetchShareoutReport();"
                    id="shg"
                    class="custom m-3"
                    label="name"
                    :options="shg_list"
                    v-model="shg_name"
                    placeholder="Type to search or select SHG"
                    >
                    </VueMultiselect>
                </div>
            </form>
        </div>


        <div v-if="loading">
            <img src="https://media.giphy.com/media/3oEjI6SIIHBdRxXI40/giphy.gif" alt="Loading..." class="mx-auto d-block">
            <p>We are generating your report please wait...</p>
        </div>
        <div id="shg_data" class="container" v-if="data.length > 0">
            
            <table class="table table-bordered">
                <tr>
                    <th>SHG Name</th>
                    <th>Total Savings</th>
                    <th>Bank Loan Outstanding</th>
                    <th>Total Payable</th>
                    <th>Total Shares</th>
                    <th>Net Profit</th>
                    <th>Net Profit per share</th>
                </tr>
                <tr>
                    <td>{{ data[0].shg.name }}</td>
                    <td>₹{{ data[0].shg.total_member_savings }}</td>
                    <td>₹{{ data[0].shg.bank_loan_outstanding }}</td>
                    <td>₹{{ data[0].shg.payable }}</td>
                    <td>{{ data[0].shg.total_number_of_shares }}</td>
                    <td>₹{{ data[0].shg.net_profit }}</td>
                    <td>₹{{ Number(data[0].shg.net_profit) / Number(data[0].shg.total_number_of_shares) }}</td>
                </tr>
            </table>
    
        </div>


        <div id="member_data" v-if="data.length > 0">
            <table class="table table-striped table-bordered">
                <thead>
                    <tr>
                        <th>Member Name</th>
                        <th>Total Savings</th>
                        <th>Loan Outstanding</th>
                        <th>Balance</th>
                        <th>Profit</th>
                        <th>Take Home</th> 
                        <th>Payable to Group</th>
                    </tr>
                </thead>

                <tbody>
                    <tr v-for="member in data[0].members">
                        <td>{{ member.name }}</td>
                        <td>₹{{ member.total_savings }}</td>
                        <td>₹{{ member.member_loan_outstanding }}</td>
                        <td>₹{{ member.savings_after_loan }}</td>
                        <td>₹{{ member.profit }}</td>
                        <td >₹{{ member.savings_after_loan >= member.profit ? member.savings_after_loan + member.profit : '0'  }}</td>
                        <td>₹{{ member.savings_after_loan <= member.profit ? member.profit + member.savings_after_loan : '0'  }}</td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
</template>

<script>
import VueMultiselect from 'vue-multiselect'
import axios from 'axios';



export default {
    name: 'shareoutReport',
    components: {
        VueMultiselect
    }, 

    data() {
        return {
            data: [],
            shg_list: [],
            shg_name: null,
            shg_id: null,
            shg_foundation_date: null,
            groups_list: [],
            month: null,
            loading: false
        }
    },

    methods: {

        fetchShareoutReport() {
            this.data = []
            this.loading = true
            setTimeout(() => {
                axios.get('/shareout_report/'+ this.shg_name.value, {headers: {'Token': localStorage.getItem('token')}}).then((response) => {
                if (response.data == false){
                    alert('SHG has not completed 52 weeks for shareout')
                }else{
                    this.data = response.data
                    console.log(this.data)
                }

            })
            .catch((error) => {
                console.log(error)
            })  
                this.loading = false
            }, 3000)
            

            
        }, 

        fetchSHG(){
            axios.get('/api/v1/shg', { headers: { 'Token': localStorage.getItem('token') } } ).then((response) =>{
            this.shg_list = response.data
            if (this.shg_list.length == 0){
                alert('No SHG found. Please add SHG first')
            }
            })
    }

    }, 

    mounted() {
        this.fetchSHG()
    }
}
</script>

<style src="vue-multiselect/dist/vue-multiselect.css"></style>