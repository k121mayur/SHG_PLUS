<template>
    <div>
        <h1 class="text-center bg-success py-3 text-light rounded-3">Saving Report</h1>

    <div class="container d-flex flex-column" >

        
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

        <div id="savingReport" style="overflow: auto;" class="d-flex flex-column align-items-center justify-content-center">
            <div v-if="data"> 
                <h1 v-if="data.length == 0" class="text-center bg-light p-3 text-danger rounded-3 m-1" style="width: 90%;">No Entry Found For Selected Month</h1>
                <h4 v-if="data.length == 0" class="text-center py-3 text-dark rounded-3 m-1" style="width: 70%;">Change month or Complete data entry</h4>
                <div class="d-flex flex-row justify-content-end"> 
                    <button @click="exportToExcel" v-if="data.length > 0" class="btn btn-warning m-0 mb-3">Export to Excel</button>
                </div>
            </div>
            <div v-if="loading">
                <img src="https://media.giphy.com/media/3oEjI6SIIHBdRxXI40/giphy.gif" alt="Loading..." class="mx-auto d-block">
                <p>We are generating your report please wait...</p>
            </div>
            
            <div v-if="data" class="table-responsive" style="overflow-x: auto; max-height: 500px; width: 100%;">
                <table id="table-data" ref="table" class="table table-hover table-bordered table-striped" style="min-width: 1500px;">
                <thead>
                    <tr>
                        <th>S.N</th>
                        <th>Group Name</th>
                        <th>District</th>
                        <th>Block</th>
                        <th>Panchayat</th>
                        <th>Village</th>
                        <th>Tola</th>
                        <th>Ward No.</th>
                        <th>MIN</th>
                        <th>Gen</th>
                        <th>SC</th>
                        <th>OBC</th>
                        <th>Total Member</th>
                        <th>First Training Meeting Date</th>
                        <th>Saving Starting Date of the Cycle</th>
                        <th>Share out Date</th>
                        <th>Meeting Day</th>
                        <th>Meeting Time</th>
                        <th>Name of Group Leader</th>
                        <th>Mobile No.</th>
                        <th>Stamp Value of the Cycle (Rs)</th>
                        <th>Monthly Loan Meeting Date</th>
                        <th>Present Total Member in the Loan Meeting</th>
                        <th>No. of total Share for this month</th>
                        <th>Cumulative Saving till Previous Month</th>
                        <th>Saving for the Month</th>
                        <th>Cumulative savings of this cycle Rs</th>
                        <th>No. of loans outstanding till Previous Month</th>
                        <th>Cumulative Loan amount till Previous Month</th>
                        <th>No. of Loan for the Month</th>
                        <th>Loan amount for the month</th>
                        <th>Total No. of Loan till this Month</th>
                        <th>Lone Reseved in this lon meatting</th>
                        <th>Value of Loan Repaid (Interest)</th>
                        <th>Value of loans outstanding Rs</th>
                        <th>Loan fund: Cash in Box (Rs)</th>
                        <th>Bank Account Openend (Y/N)</th>
                        <th>Loan fund: Cash in Bank (Rs)</th>
                        <th>Bank Account Date</th>
                        <th>Bank Account No.</th>
                        <th>Name of the Bank</th>
                        <th>Branch</th>
                        <th>No of BPL</th>
                        <th>Date Submitted</th>
                        <th>Name of CRP</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="item in data" :key="item.sn">
                    <td>{{ item.sn }}</td>
                    <td>{{ item.group_name }}</td>
                    <td>{{ item.district }}</td>
                    <td>{{ item.block }}</td>
                    <td>{{ item.panchayat }}</td>
                    <td>{{ item.village }}</td>
                    <td>{{ item.tola }}</td>
                    <td>{{ item.ward_no }}</td>
                    <td>{{ item.min }}</td>
                    <td>{{ item.gen }}</td>
                    <td>{{ item.sc }}</td>
                    <td>{{ item.obc }}</td>
                    <td>{{ item.total_member }}</td>
                    <td>{{ item.first_training_meeting_date }}</td>
                    <td>{{ item.saving_starting_date_of_the_cycle }}</td>
                    <td>{{ item.share_out_date }}</td>
                    <td>{{ item.meeting_day }}</td>
                    <td>{{ item.meeting_time }}</td>
                    <td>{{ item.name_of_group_leader }}</td>
                    <td>{{ item.mobile_no }}</td>
                    <td>{{ item.stamp_value_of_the_cycle_rs }}</td>
                    <td>{{ item.monthly_loan_meeting_date }}</td>
                    <td>{{ item.present_total_member_in_the_loan_meeting }}</td>
                    <td>{{ item.no_of_total_share_for_this_month }}</td>
                    <td>{{ item.cumulative_saving_till_previous_month }}</td>
                    <td>{{ item.saving_for_the_month }}</td>
                    <td>{{ item.cumulative_savings_of_this_cycle_rs }}</td>
                    <td>{{ item.no_of_loans_outstanding_till_previous_month }}</td>
                    <td>{{ item.cumulative_loan_amount_till_previous_month }}</td>
                    <td>{{ item.no_of_loan_for_the_month }}</td>
                    <td>{{ item.loan_amount_for_the_month }}</td>
                    <td>{{ item.total_no_of_loan_till_this_month }}</td>
                    <td>{{ item.lone_reseved_in_this_lon_meatting }}</td>
                    <td>{{ item.value_of_loan_repaid_interest }}</td>
                    <td>{{ item.value_of_loans_outstanding_rs }}</td>
                    <td>{{ item.loan_fund_cash_in_box_rs }}</td>
                    <td>{{ item.bank_account_openend__y_n }}</td>
                    <td>{{ item.loan_fund_cash_in_bank_rs }}</td>
                    <td>{{ item.bank_account_date }}</td>
                    <td>'{{ item.bank_account_no }}</td>
                    <td>{{ item.name_of_the_bank }}</td>
                    <td>{{ item.branch }}</td>
                    <td>{{ item.no_of_bpl }}</td>
                    <td>{{ item.date_submitted }}</td>
                    <td>{{ item.name_of_crp }}</td>
                    </tr>
                </tbody>
                </table>
            </div>

        </div>

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
            loading: true
        }
    }, 

    methods: {
        fetchData() {
            this.loading = true;  // Set loading to true

            // Make API request
            axios.get('/savingsReport/byMonth/' + this.month, {
                headers: { 'Token': localStorage.getItem('token') }
            })
            .then(response => {
                this.data = response.data;  // Store the response data
                this.loading = false;  // Set loading to false after data is fetched
            })
            .catch(error => {
                console.error('Error fetching data:', error);
                this.loading = false;  // Ensure loading is false in case of error
            });
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
      XLSX.writeFile(workbook, "MIS-Report-" + this.month + ".xlsx");
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