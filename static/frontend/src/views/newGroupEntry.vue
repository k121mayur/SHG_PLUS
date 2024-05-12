<template>

    <div class="d-flex flex-row m-0 col-md-12 panel"> 
        <SidePanel class="col-md-2"/>
        <div class="main-panel col-md-10">
        <h1>SHG Registration Form</h1>

        <form class="m-1 d-flex flex-row">
            <div class="col-md-6 border-end m-3">
                <h4>Section 1: SHG Details</h4>
                <div class="mb-3">
                    <label for="name_of_shg" class="form-label">Name of SHG:</label>
                    <input type="text" id="name_of_shg" name="name_of_shg" class="form-control" required>
                </div>
                <div class="mb-3">
                    <label for="project_name" class="form-label">Project Name:</label>
                    <input type="text" id="project_name" name="project_name" class="form-control" required>
                </div>
                <div class="mb-3">
                    <label for="village_name" class="form-label">Village Name:</label>
                    <input type="text" id="village_name" name="village_name" class="form-control" required>
                </div>
                <div class="mb-3">
                    <label for="panchyat_name" class="form-label">Panchayat Name:</label>
                    <input type="text" id="panchyat_name" name="panchyat_name" class="form-control" required>
                </div>
                <div class="mb-3">
                    <label for="group_address" class="form-label">Group Address:</label>
                    <textarea id="group_address" name="group_address" rows="4" cols="50" class="form-control"></textarea>
                </div>
                <div class="mb-3">
                    <label for="formation_date" class="form-label">Formation Date:</label>
                    <input type="date" id="formation_date" name="formation_date" class="form-control" required>
                </div>
                <div class="mb-3">
                    <label for="total_no._of_members" class="form-label">Total Number of Members:</label>
                    <input type="number" id="total_no._of_members" name="total_no._of_members" min="1" class="form-control" required>
                </div>

                <div class="mb-3">
                    <label for="saving_day" class="form-label">Saving Day (Day of the Month):</label>
                    <input type="number" id="saving_day" name="saving_day" min="1" max="31" class="form-control" required>
                </div>
                <div class="mb-3">
                    <label for="place_of_meeting" class="form-label">Place of Meeting:</label>
                    <input type="text" id="place_of_meeting" name="place_of_meeting" class="form-control" required>
                </div>
            </div>
            <div class="col-md-6 m-3">
                

                <h4>Section 2: Staff Details</h4>
                <div class="mb-3">
                    <label for="staff_name" class="form-label">Staff Name:</label>
                    <input type="text" id="staff_name" name="staff_name" class="form-control" required>
                </div>
                <div class="mb-3">
                    <label for="samuh_sakhi_name" class="form-label">Samuh Sakhi Name:</label>
                    <input type="text" id="samuh_sakhi_name" name="samuh_sakhi_name" class="form-control" required>
                </div>
                <h4>Section 3: Financial Details</h4>
                <h5>Savings Account Details</h5>
                <div class="mb-3">
                <label for="bank_name" class="form-label">Bank Name:</label>
                <input type="text" id="bank_name" name="bank_name" class="form-control" required>
                </div>
                <div class="mb-3">
                <label for="branch" class="form-label">Branch Name:</label>
                <input type="text" id="branch" name="branch" class="form-control" required>
                </div>
                <div class="mb-3">
                    <label for="account_name" class="form-label">Account Name:</label>
                    <input type="text" id="account_name" name="account_name" class="form-control" required>
                </div>
                <div class="mb-3">
                    <label for="accoun_number" class="form-label">Account Number:</label>
                    <input type="text" id="accoun_number" name="accoun_number" class="form-control" required>
                </div>
                <div class="mb-3">
                <label for="IFSC_code" class="form-label">IFSC Code:</label>
                <input type="text" id="IFSC_code" name="IFSC_code" class="form-control" required>
                </div>

                <h4>Share Details</h4>
                <div class="mb-3">
                <label for="per_share_size_in_INR" class="form-label">Per Share Size (INR):</label>
                <input type="number" id="per_share_size_in_INR" name="per_share_size_in_INR" min="1" class="form-control" required>
                </div>

                <div class="d-grid gap-2 d-md-flex justify-content-md-end">
                <button type="submit" class="btn btn-primary">Register SHG</button>
                </div>

            </div>
            </form>

        </div>
    </div>

</template>

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

<script>
import SidePanel from "@/components/SidePanel.vue"


export default {
    name: 'newGroupEntry', 
    components: {
        SidePanel
}
}
</script>