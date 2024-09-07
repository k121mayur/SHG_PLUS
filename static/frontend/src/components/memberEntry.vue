<template>
  <div>
    <div class="z-100 text-danger" v-if="!shg_status" style="margin: auto; font-size: 20px"> You Can't Add a member
      without adding a SHG</div>
      <h1 class="text-center mx-0 px-0 col-md-12 rounded">Member Registration Form</h1>
    <div class="container" v-if="shg_status">
      
      <form @submit.prevent="addMember">
        <div class="row">

          <div class="col-md-6 border-right">
            <h2>Member Information</h2>
            <div class="form-group">
              <label for="shg_id">SHG Name:</label>
              <VueMultiselect @focusout="fetch_village" v-model="formData.shg_name" label="name" :options="shg_list"
                placeholder="Type to search or select SHG"> </VueMultiselect>
              <!-- <input type="text" class="form-control" id="shg_name" v-model="formData.shg_name" required>
            <div style="z-index: 999; position: absolute; background-color: white;"> <div>SHG 1</div> </div> -->
              <!-- <div v-if="shg_list and show_shg" class="mt-3">
              <ul>
                <li> Test SHG Name</li>
              </ul> 
            </div> -->
            </div>
            <div class="form-group">
              <label for="village">Village:</label>
              <input type="text" class="form-control" id="village" v-model="formData.shg_name.village">
            </div>
            <div class="form-group">
              <label for="household_code">Household Code:</label>
              <input type="text" class="form-control" id="household_code" v-model="formData.household_code" required>
            </div>
            <div class="form-group">
              <label for="first_name">First Name:</label>
              <input type="text" class="form-control" id="first_name" v-model="formData.first_name" required>
            </div>
            <div class="form-group">
              <label for="father_husband_name">Father/Husband Name:</label>
              <input type="text" class="form-control" id="father_husband_name" v-model="formData.father_husband_name"
                required>
            </div>
            <div class="form-group">
              <label for="last_name">Last Name:</label>
              <input type="text" class="form-control" id="last_name" v-model="formData.last_name" required>
            </div>

            <div class="form-group">
              <label for="voter_id">Voter ID:</label>
              <input type="text" class="form-control" id="voter_id" v-model="formData.voter_id">
            </div>
            <div class="form-group">
              <label for="adhar_id">Adhar ID:</label>
              <input type="text" class="form-control" id="adhar_id" v-model="formData.adhar_id">
            </div>
            <div class="form-group">
              <label for="pan_number">PAN Number:</label>
              <input type="text" class="form-control" id="pan_number" v-model="formData.pan_number">
            </div>
            <div class="form-group">
              <label for="ration_card_number">Ration Card Number:</label>
              <input type="text" class="form-control" id="ration_card_number" v-model="formData.ration_card_number">
            </div>
            <div class="form-group">
              <label for="education">Education:</label>
              <select class="form-control" id="education" v-model="formData.education">
                <option value="Illiterate">Illiterate</option>
                <option value="Litrate">Litrate</option>
                <option value="Primary">Primary</option>
                <option value="Secondary">Secondary</option>
                <option value="Higher Secondary">Higher Secondary</option>
                <option value="Degree">Degree</option>
                <option value="Masters">Masters</option>
                <option value="Doctarate">Doctarate</option>
                <option value="Technical Degree">Technical Degree</option>
                <option value="ITI">ITI</option>
                <option value="Diploma">Diploma</option>
              </select>
            </div>
            <div class="form-group">
              <label for="category">Category:</label>
              <!-- Add options here -->
              <select class="form-control" id="category" v-model="formData.category">
                <option value="General">General</option>
                <option value="ST">ST</option>
                <option value="SC">SC</option>
                <option value="OBC">OBC</option>
              </select>
            </div>
            <div class="form-group">
              <label for="caste">Caste:</label>
              <!-- Add options here -->
              <input type="text" class="form-control" id="caste" v-model="formData.caste">
            </div>
          </div>
          <div class="col-md-6">
            <!-- Household Information -->
            <h2>Household Information</h2>
            <div class="form-group">
              <label for="number_of_family_members">Number of Family Members:</label>
              <input type="number" class="form-control" id="number_of_family_members"
                v-model="formData.number_of_family_members">
            </div>
            <div class="form-group">
              <label for="mobile_number">Mobile Number:</label>
              <input type="text" class="form-control" id="mobile_number" v-model="formData.mobile_number" required
                pattern="[0-9]{10}">
            </div>
            <div class="form-group">
              <label for="total_land_kattha">Total Land (Kattha):</label>
              <input type="number" step=".01" class="form-control" id="total_land_kattha"
                v-model="formData.total_land_kattha">
            </div>
            <div class="form-group">
              <label for="total_irrigated_land_kattha">Total Irrigated Land (Kattha):</label>
              <input type="number" step=".01" class="form-control" id="total_irrigated_land_kattha"
                v-model="formData.total_irrigated_land_kattha">
            </div>
            <div class="form-group">
              <label for="total_no_of_goats">Total No. of Goats:</label>
              <input type="number" class="form-control" id="total_no_of_goats" v-model="formData.total_no_of_goats">
            </div>
            <div class="form-group">
              <label for="total_no_of_cattle">Total No. of Cattle:</label>
              <input type="number" class="form-control" id="total_no_of_cattle" v-model="formData.total_no_of_cattle">
            </div>
            <div class="form-group">
              <label for="total_no_of_members_migrated">Total No. of Members Migrated:</label>
              <input type="number" class="form-control" id="total_no_of_members_migrated"
                v-model="formData.total_no_of_members_migrated">
            </div>
            <div class="form-group">
              <label for="main_source_of_income">Main Source of Income:</label>
              <input type="text" class="form-control" id="main_source_of_income"
                v-model="formData.main_source_of_income">
            </div>
            <div class="form-group">
              <label for="head_of_the_family_name">Head of the Family Name:</label>
              <input type="text" class="form-control" id="head_of_the_family_name"
                v-model="formData.head_of_the_family_name">
            </div>

            <div class="form-group">
              <label for="bank_name">Bank Name:</label>
              <input type="text" class="form-control" id="bank_name" v-model="formData.bank_name">
            </div>
            <div class="form-group">
              <label for="branch_name">Branch Name:</label>
              <input type="text" class="form-control" id="branch_name" v-model="formData.branch_name">
            </div>
            <div class="form-group">
              <label for="account_number">Account Number:</label>
              <input type="text" class="form-control" id="account_number" v-model="formData.account_number">
            </div>
            <div class="form-group">
              <label for="IFSC_code">IFSC Code:</label>
              <input type="text" class="form-control" id="IFSC_code" v-model="formData.IFSC_code">
            </div>
          </div>
          <div class="col-md-12 border p-3 m-2 d-flex flex-row custom-scheme-div flex-wrap">
            <div class="col-md-6 d-flex flex-column align-items-start">
              <div class="">
                <input class="m-1" type="checkbox" id="scheme_1" name="scheme_1" value="scheme_1"
                  v-model="formData.Ayushman_Bharat">
                <label for="scheme_1" class="m-1">Ayushman Bharat</label><br>
              </div>
            </div>
            <div class="col-md-6 d-flex flex-column align-items-start">
              <div class="">
                <input class="m-1" type="checkbox" id="scheme_2" name="scheme_2" value="scheme_2"
                  v-model="formData.PMJJBY">
                <label for="scheme_2" class="m-1"> Pradhan Mantri Jivan Jyoti Bima Yojana</label><br>
              </div>

            </div>
            <div class="col-md-6 d-flex flex-column align-items-start">
              <div class="">
                <input class="m-1" type="checkbox" id="scheme_3" name="scheme_3" value="scheme_3"
                  v-model="formData.PMSBY">
                <label for="scheme_3" class="m-1">Pradhan Mantri Surksha Bima Yojana</label><br>
              </div>

            </div>

            <div class="col-md-6 d-flex flex-column align-items-start">
              <div class="">
                <input class="m-1" type="checkbox" id="scheme_4" name="scheme_4" value="scheme_4"
                  v-model="formData.Labour_card">
                <label for="scheme_4" class="m-1">Labour Card</label><br>
              </div>

            </div>

          </div>
        </div>
        <button type="submit" class="btn btn-primary my-3" :disabled="!shg_status">Add Member</button>
      </form>
    </div>
  </div>
</template>

<script>
import VueMultiselect from 'vue-multiselect';
import axios from 'axios';

export default {
  name: 'memberEntry',

  components: {
    VueMultiselect
  },

  data() {
    return {
      shg_list: [],
      shg_status: true,
      formData: {
        member_id: null,
        shg_name: { name: '', village: '' },
        village: '',
        household_code: '',
        first_name: '',
        father_husband_name: '',
        last_name: '',
        number_of_family_members: null,
        voter_id: '',
        adhar_id: '',
        pan_number: '',
        ration_card_number: '',
        education: '',
        category: [],
        caste: '',
        mobile_number: '',
        total_land_kattha: null,
        total_irrigated_land_kattha: null,
        total_no_of_goats: null,
        total_no_of_cattle: null,
        total_no_of_members_migrated: null,
        main_source_of_income: '',
        head_of_the_family_name: '',

        bank_name: '',
        branch_name: '',
        account_number: '',
        IFSC_code: '',

        Ayushman_Bharat: false,
        PMJJBY: false,
        PMSBY: false,
        Labour_card: false
      }
    };
  },
  methods: {
    addMember() {

      axios.post('/api/v1/member', this.formData, { headers: { 'Token': localStorage.getItem('token') } }
      ).then((response) => {
        if (response == 200) {
          alert("Member Added Successfully")
        }
      })
    },

    showError() {
      this.shg_status = false
    },

    fetchSHG() {
      axios.get('/api/v1/shg', { headers: { 'Token': localStorage.getItem('token') } }).then((response) => {
        this.shg_list = response.data
        if (this.shg_list.length == 0) {
          this.showError()
        }
      })
    }
  },
  created() {
    this.fetchSHG();
  }
}

</script>

<style scoped>
.custom-scheme-div {
  border-radius: 10Px;
  background-color: whitesmoke;

}

.main-panel {
  height: 85vh;
  border: solid 1px black;
  margin-left: 2px;
  margin-right: 0%;
  border-radius: 10px;
  margin-top: 1%;
  overflow: auto;
}

.form-group {
  display: flex;
  flex-direction: row;
  width: 100;
  text-wrap: nowrap;
  align-items: center;
  margin: 1%;
}

.form-group>* {
  margin-right: 1%;
  margin-left: 1%;
}

form {
  width: 90%;
}

h2 {
  text-align: center;
  color: rgb(3, 0, 0);
  background-color: rgb(255, 232, 105);
  border-radius: 10px;
  padding: 1%;
}

h1 {
  color: rgb(23, 0, 128);
  background-color: rgb(184, 216, 64);
  padding: 1%;
}
</style>
<style src="vue-multiselect/dist/vue-multiselect.css"></style>