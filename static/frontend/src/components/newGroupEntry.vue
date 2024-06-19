<template>

        <div class="main-panel col-md-10">
            <h1>SHG Registration Form</h1>

            <form class="m-1 d-flex flex-row" @submit.prevent="createGroup">
                <div class="col-md-6 border-end m-3">
                    <h4>Section 1: SHG Details</h4>
                    <div class="mb-3">
                        <label for="name_of_shg" class="form-label">Name of SHG:</label>
                        <input type="text" id="name_of_shg" name="name_of_shg" class="form-control" v-model="formData.name_of_shg" required>
                    </div>
                    <div class="mb-3">
                        <label for="project_name" class="form-label">Project Name:</label>
                        <input type="text" id="project_name" name="project_name" class="form-control" v-model="formData.project_name" required>
                    </div>
                    <div class="mb-3">
                        <label for="village_name" class="form-label">Village Name:</label>
                        <input type="text" id="village_name" name="village_name" class="form-control" v-model="formData.village_name" required>
                    </div>
                    <div class="mb-3">
                        <label for="panchyat_name" class="form-label">Panchayat Name:</label>
                        <input type="text" id="panchyat_name" name="panchyat_name" class="form-control" v-model="formData.panchyat_name" required>
                    </div>
                    <div class="mb-3">
                        <label for="group_address" class="form-label">Group Address:</label>
                        <textarea id="group_address" name="group_address" rows="4" cols="50" class="form-control" v-model="formData.group_address"></textarea>
                    </div>
                    <div class="mb-3">
                        <label for="formation_date" class="form-label">Formation Date:</label>
                        <input type="date" id="formation_date" name="formation_date" class="form-control" v-model="formData.formation_date" required>
                    </div>
                    <div class="mb-3">
                        <label for="total_no._of_members" class="form-label">Total Number of Members:</label>
                        <input type="number" id="total_no._of_members" name="total_no._of_members" min="1" max="20" class="form-control" v-model="formData.total_no_of_members" required>
                    </div>
                    <div class="mb-3">
                        <label for="saving_day" class="form-label">Saving Day (Day of the Month):</label>
                        <select  id="saving_day" name="saving_day" class="form-select" v-model="formData.saving_day" required>
                            <option value="1">Monday</option>
                            <option value="2">Tuesday</option>
                            <option value="3">Wednesday</option>
                            <option value="4">Thursday</option>
                            <option value="5">Friday</option>
                            <option value="6">Saturday</option>
                            <option value="7">Sunday</option>
                        </select>
                    </div>
                </div>
                <div class="col-md-6 m-3">
                    <h4>Section 2: Staff Details</h4>
                    <div class="mb-3">
                        <label for="staff_name" class="form-label">Staff Name:</label>
                        <input type="text" id="staff_name" name="staff_name" class="form-control" v-model="formData.staff_name" required>
                    </div>
                    <div class="mb-3">
                        <label for="samuh_sakhi_name" class="form-label">Samuh Sakhi Name:</label>
                        <input type="text" id="samuh_sakhi_name" name="samuh_sakhi_name" class="form-control" v-model="formData.samuh_sakhi_name" required>
                    </div>
                    <h4>Section 3: Financial Details</h4>
                    <h5>Savings Account Details</h5>
                    <div class="mb-3">
                        <label for="bank_name" class="form-label">Bank Name:</label>
                        <input type="text" id="bank_name" name="bank_name" class="form-control" v-model="formData.bank_name" >
                    </div>
                    <div class="mb-3">
                        <label for="branch" class="form-label">Branch Name:</label>
                        <input type="text" id="branch" name="branch" class="form-control" v-model="formData.branch" >
                    </div>
                    <div class="mb-3">
                        <label for="account_name" class="form-label">Account Name:</label>
                        <input type="text" id="account_name" name="account_name" class="form-control" v-model="formData.account_name" >
                    </div>
                    <div class="mb-3">
                        <label for="account_number" class="form-label">Account Number:</label>
                        <input type="text" id="account_number" name="account_number" class="form-control" v-model="formData.account_number" >
                    </div>
                    <div class="mb-3">
                        <label for="IFSC_code" class="form-label">IFSC Code:</label>
                        <input type="text" id="IFSC_code" name="IFSC_code" class="form-control" maxlength="11" minlength="11" v-model="formData.IFSC_code" >
                    </div>
                    <h4>Share Details</h4>
                    <div class="mb-3">
                        <label for="per_share_size_in_INR" class="form-label">Per Share Size (INR):</label>
                        <input type="number" id="per_share_size_in_INR" name="per_share_size_in_INR" min="1" class="form-control" v-model="formData.per_share_size_in_INR" required>
                    </div>
                    <div class="d-flex flex-row justify-content-between">
                        <div class="text-danger">Share Out Date: {{ shareOutDate }}</div>
                        <div class="d-grid gap-2 d-md-flex justify-content-md-end">
                            <button type="submit" class="btn btn-primary">Register SHG</button>
                        </div>
                    </div>
                </div>
            </form>

        </div>
</template>

<script>
import axios from "axios";


export default {
    name: 'newGroupEntry', 
    data (){
        return {
            formData: {
                shareOutDate : "",
                name_of_shg: '',
                project_name: '',
                village_name: '',
                panchyat_name: '',
                group_address: '',
                formation_date: '',
                total_no_of_members: '',
                saving_day: '',
                place_of_meeting: '',
                staff_name: '',
                samuh_sakhi_name: '',
                bank_name: '',
                branch: '',
                account_name: '',
                account_number: '',
                IFSC_code: '',
                per_share_size_in_INR: ''
            }
        }
    },
    methods: {
        createGroup() {

            axios.post('/api/v1/shg', this.formData, { headers: { 'Token': localStorage.getItem('token') } } ).then((response) => {
                if (response.status === 200) {
                    alert("Group Successfully created")
                }
            }).catch(e => {
                console.log(e)
            })
            // Construct an object with all input values
            
        }
    }, 
    computed: {
        shareOutDate() {
            if (!this.formData.formation_date) return ''; // Return empty string if formation_date is not set

            // Convert formation_date to Date object
            const formationDate = new Date(this.formData.formation_date);
            // Calculate shareOutDate by adding 52 weeks to formation_date
            const shareOutDate = new Date(formationDate.getTime() + (52 * 7 * 24 * 60 * 60 * 1000)); // 52 weeks in milliseconds

            // Format the shareOutDate to a readable string
            const options = { year: 'numeric', month: 'long', day: 'numeric' };
            return shareOutDate.toLocaleDateString('en-US', options);
        }
    }
}
</script>

<style scoped>
.main-panel {
    height: 85vh;
    border: solid 1px black;
    margin-left: 2px;
    margin-right: 0%;
    border-radius : 10px;
    margin-top: 1%;
    overflow: auto;
}

.mb-3 {
    display: flex;
    flex-direction: row;
    width: 100;
    text-wrap: nowrap;
    margin: 1%;
}

form {
    width: 90%;
}   

h4 {
    text-align: center;
    color: blueviolet;
    font-family: 'Franklin Gothic Medium', 'Arial Narrow', Arial, sans-serif;
    background-color: gold;
    border-radius: 10px;
    padding: 1%;
}

h1 {
    color: green;
    background-color: whitesmoke;
    padding: 1%;
}
</style>