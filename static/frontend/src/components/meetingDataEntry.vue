<template>
    <div>
    <h1> Data Entry</h1>
        <div class="d-flex flex-row align-items-center justify-content-center">
            <label for="shg" class="m-3">Select SHG</label>
            <VueMultiselect
            @focusout="fetchMembers"
            id="shg"
            class="custom m-3"
            label="name"
            :options="shg_list"
            v-model="shg_name"
            placeholder="Type to search or select SHG"
            >
            
            </VueMultiselect>
        </div>
        <div id="meetings_list" v-if="!meetings_list.length == 0" >
            <ul class="list-group mx-3" style="max-height: 30vh; border-radius: 20px; border : saddlebrown solid 1px; overflow: auto">
                <li class="list-group-item" style="background-color: antiquewhite;">List of Meetings</li>
                <li  class="list-group-item" v-for="meet in meetings_list">{{meet.name}}</li>

            </ul>
        </div>
        <div class="form-group d-flex flex-row align-items-center justify-content-center">
            
            <label for="date" >Date of Meeting</label>
            <input type="date" id="date" class="form-control mx-3" name="date">
        </div>

        <!-- list of members -->
        <div class="m-3 mx-3" v-if ="!members_list.length == 0" > 
            <ul>
                <li class="list-group-item" style="background-color: antiquewhite;">Member Attendence</li>
                <li v-for="member in members_list" class="list-group-item" >
                    <input type="checkbox" id ="member"  class="m-3" name="{{member.name}}" value="{{member.name}}">
                    <label>{{member.name}}</label>
                </li>
            </ul>
        
        </div>

    </div>


</template>

<script>
import VueMultiselect from 'vue-multiselect'
import axios from 'axios';

export default {
    name: 'meetingDataEntry',

    components: {  
        VueMultiselect
    },

    data () {
        return {
            shg_list: [],
            shg_name:'',
            meetings_list : [], 
            members_list : [{name:"Mayur"}],
            status : false
        }
    }, 

    methods : {
        fetchSHG(){
            axios.get('/api/v1/shg', { headers: { 'Token': localStorage.getItem('token') } } ).then((response) =>{
            this.shg_list = response.data
            if (this.shg_list.length == 0){
                this.showError()
            }
            })
    }, 
    fetchMembers(){
        axios.get("/api/v1/member/" + this.shg_name.value, { headers: { 'Token': localStorage.getItem('token') } } ).then((response) =>{
        this.members_list = response.data
        
        })
  }
},
 created() {
  this.fetchSHG();
}


}

</script>

<style>
.custom {
    max-width: 50%;
    border-radius: 10px;

}

.form-control {
    max-width: 50%;
}
</style>
<style src="vue-multiselect/dist/vue-multiselect.css"></style>