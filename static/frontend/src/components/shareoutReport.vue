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
            shg_list: [],
            shg_name: null,
            shg_id: null,
            shg_foundation_date: null,
            groups_list: [],
            month: null
        }
    },

    methods: {

        fetchShareoutReport() {
            axios.get('/shareoutReport/'+ this.shg_name.value, {headers: {'Token': localStorage.getItem('token')}}).then((response) => {
                if (response.data == false){
                    alert('SHG has not completed 52 weeks for shareout')
                }else{
                    alert('SHG has completed 52 weeks for shareout')
                }

            })
            .catch((error) => {
                console.log(error)
            })  
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