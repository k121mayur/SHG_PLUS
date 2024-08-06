<template>


    <div class="container d-flex flex-column mt-3" >

        <h1 class="text-center bg-success py-3 text-light rounded-3 m-1">Saving Report</h1>
        <div class="d-flex flex-row justify-content-end">
            <label for="month" class="form-label m-3">Select the Month</label>
            <select id="month" name="month" v-model="month" class="form-select" @change="fetchData">
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

        <div id="savingReport" v-if = "data" style="overflow: auto;" class="d-flex flex-column align-items-center justify-content-center">
            <h1 v-if="data.length == 0" class="text-center bg-light p-3 text-danger rounded-3 m-1" style="width: 90%;">No Entry Found For Selected Month</h1>
            <h4 v-if="data.length == 0" class="text-center py-3 text-dark rounded-3 m-1" style="width: 70%;">Change month or Complete data entry</h4>
            <div class="d-flex flex-row justify-content-end"> 
                <button @click="exportToExcel" v-if="data.length > 0" class="btn btn-warning m-0">Export to Excel</button>
            </div>
            
            
            <table ref="table" class="table table-bordered table-hover mt-1" v-if="data.length > 0">
                <thead class="thead-dark">
                    <tr class="bg-dark text-light">
                        <th class="bg-dark text-light">Sr. No.</th>
                        <th class="bg-dark text-light">SHG Name</th>
                        <th class="bg-dark text-light">Meeting Date</th>
                        <th class="bg-dark text-light">Expected Attendence</th>
                        <th class="bg-dark text-light">Actual Attendence</th>
                        <th class="bg-dark text-light">Expected Savings</th>
                        <th class="bg-dark text-light">Actual Savings</th>
                        <th class="bg-dark text-light">Total Non-Savers</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="(saving, index) in data">
                        <td>{{ index+1 }}</td>
                        <td>{{ saving.name }}</td>
                        <td>{{ saving.meeting_date }}</td>
                        <td>{{ saving.expected_attendence }}</td>
                        <td>{{ saving.actual_attendence }}</td>
                        <td>{{ saving.expected_savings }}</td> 
                        <td>{{ saving.actual_savings }}</td>
                        <td>{{ saving.number_of_non_savers }}</td>
                    </tr>
                </tbody>
            </table>
        </div>


    </div>
</template>

<script>
import axios from 'axios'
import * as XLSX from 'xlsx';



export default {
    name: 'savingReport', 

    data() {
        return {
            data: null,
            month: new Date().getMonth() + 1,
        }
    }, 

    methods: {
        fetchData() {
            axios.get('/savingsReport/byMonth/' + this.month, { headers: { 'Token': localStorage.getItem('token') } } )
            .then(response => {
                this.data = response.data
            })
        }, 

        exportToExcel() {
      // Reference the table element
      const table = this.$refs.table;

      // Convert the table to a worksheet
      const worksheet = XLSX.utils.table_to_sheet(table);

      // Create a new workbook and append the worksheet
      const workbook = XLSX.utils.book_new();
      XLSX.utils.book_append_sheet(workbook, worksheet, "Sheet1");

      // Export the workbook to an Excel file
      XLSX.writeFile(workbook, "Savings-Report-" + this.month + ".xlsx");
    }
    },

    mounted() {
        this.fetchData()
    }

}
</script>

<style scoped>
#month {
    width: max-content;
}

</style>