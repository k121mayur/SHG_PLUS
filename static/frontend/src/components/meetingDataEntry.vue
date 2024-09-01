<template>
    <div>
    <h1 class="text-center bg-light p-3 text-warning rounded-3"> Data Entry</h1>

        <form @submit.prevent="addMeeting">
        <div class="d-flex flex-row align-items-center justify-content-center">
            <label for="shg" class="m-3">Select SHG</label>
            <VueMultiselect
            @focusout="fetchMembers(); fetchMeetings();"
            id="shg"
            class="custom m-3"
            label="name"
            :options="shg_list"
            v-model="shg_name"
            placeholder="Type to search or select SHG"
            >
            
            </VueMultiselect>
        </div>

       
        <div class="form-group d-flex flex-row align-items-center justify-content-center">
            
            <label for="date" >Date of Meeting</label>
            <input type="date" :max="new Date().toISOString().split('T')[0]" id="date" class="form-control mx-3" name="date" v-model="meeting_date" required/>
        </div>

        <div class="mt-3 mx-3 d-flex flex-row col-md-12">
         <!-- List of meetings -->
            <div id="meetings_list" class=" col-md-4" v-if="!meetings_list.length == 0" >
                <ul class="list-group mx-3" style="max-height: 30vh; border-radius: 20px; border : saddlebrown solid 1px; overflow: auto">
                    <li class="list-group-item" style="background-color: antiquewhite;">List of Meetings</li>
                    <li  class="list-group-item" v-for="meet in meetings_list">{{meet.name}} <RouterLink class="btn btn-primary mx-3" :to="`/meetingWorkflow/${meet.value}`" >Edit</RouterLink></li>
                </ul>
            </div>

            <!-- list of members -->
            <div class="col-md-7 "  style="border-radius: 20px; overflow: auto" v-if ="!members_list.length == 0" > 
                <ul class="list-group d-flex flex-column align-items-left justify-content-start mx-3" style="max-height: 30vh; border-radius: 20px; border : saddlebrown solid 1px; overflow: auto">
                    <li class="list-group-item" style="background-color: antiquewhite; text-align: center; padding-top: 3px; color: darkblue">Member Attendence</li>
                    <li v-for="member in members_list" class="list-group-item d-flex flex-row justify-content-start align-items-center"  style="padding-left: 3rem;">
                        <input type="checkbox" id ="member"  class="m-3" :name="member.name" :value="member.value" v-model="member.present"/>
                        <label>{{member.name}}</label>
                    </li>
                    
                </ul>
            
            </div>
    </div>

        <!-- Create meeting Button -->
        <div> 
              <button class="btn btn-primary my-3 mx-3" type="submit">Add Meeting</button>
        </div>
        </form>
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
            members_list : [],
            status : false, 
            meeting_date: new Date().toISOString().slice(0, 10)

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
            
            this.members_list = response.data.map(member => ({
          ...member,
          present: false // Add a 'present' property to track checkbox state
        }));
        
        })
  }, 

  fetchMeetings(){

    axios.get("/api/v1/meeting/" + this.shg_name.value, { headers: { 'Token': localStorage.getItem('token') } } ).then((response) =>{
        this.meetings_list =  response.data
  })
},

  addMeeting(){
    if (this.attendece < (this.members_list.length) /2){
        alert("Meeting should have atleast 50% members present")
    } else {
    let data = {}
    data.shg = this.shg_name
    data.attendece = this.members_list
    data.date = this.meeting_date
    axios.post('/api/v1/meeting', data, {headers: {'Token': localStorage.getItem('token')}}).then( (response ) => {
        console.log(response);
        if(response.status == 200){
            console.log(response.data)
            this.$router.push('/meetingWorkflow/' + response.data.meeting_id)
            alert("Meeting Successfully added")
        }

        if(response.status == 400){
            alert("You can't add meeting with no members")
        }

        if(response.status == 500){
            alert(response.data.message)

        }

    }).catch((error) => {
        alert(error.response.data.message)
    })
    }

  }
},
 created() {
  this.fetchSHG();
}, 
computed: {
    attendece () {
        return this.members_list.filter(member => member.present).length
    }


}}

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