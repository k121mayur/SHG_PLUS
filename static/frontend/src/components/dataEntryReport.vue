<template>
<div>
    <h1 class="text-center bg-success p-3 text-light rounded-3"> Data Entry Report</h1>
    
    <div class="d-flex flex-row align-items-center justify-content-end">
        <label class="form-label m-3 text-primary"><strong>Select Month</strong></label>
        <select @change="fetchGroups" id="month" v-model="month" class="form-select" style="width: max-content;">
            <option value="1">January</option>
            <option value="2">February</option>
            <option value="3">March</option>
            <option value="4">April</option>
            <option value="5">May</option>
            <option value="6">June</option>
            <option value="7">July</option>
            <option value="8">August</option>
            <option value="9">September</option>
            <option value="10">October</option>
            <option value="11">November</option>
            <option value="12">December</option>
        </select>
    </div>
    <div v-if="groups_list.length > 0 ">  
        <table class="table table-hover table-responsive max-100"  style="overflow: auto">
            <thead class="thead-dark">
                <tr>
                    <th scope="col">Group Name</th>
                    <th scope="col">Meeting Date</th>
                    <th scope="col">Status</th>
                    <th scope="col">Action</th>
                </tr>
            </thead>

            <tbody>
                <tr scope="row" v-for="group in groups_list">
                    <td>{{group.name}}</td>
                    <td>{{ group.date }}</td>
                    <td>{{ group.status }}</td>
                    <td v-if="group.action == 'Entry'">
                        <a :href="'/meetingWorkflow/' +  group.id " ><button class="btn btn-primary">Data Entry</button></a>
                    </td>
                </tr>``
            </tbody>
        </table>
    </div>


</div>
</template>

<script>
import axios from 'axios'

export default { 
    name: 'dataEntryReport',

    data() {
        return {
            month: new Date().getMonth() + 1,
            groups_list: []
        }
    }, 

    methods: {
        fetchGroups() {
            axios.get('/api/v1/shgs/byMonth/' + this.month)
            .then(response => {
                this.groups_list = response.data
            })
        }
    }, 
    mounted(){
        this.fetchGroups()
    }
}

</script>