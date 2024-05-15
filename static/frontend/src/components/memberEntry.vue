<template>
  <div class="container">
    <h1>Member Registration Form</h1>
    <form @submit.prevent="addMember">
      <div class="row">
        <div class="col-md-6">
          <h2>Member Information</h2>
          <div class="form-group">
            <label for="shg_id">SHG Name:</label>
            <input type="text" class="form-control" id="shg_name" v-model="formData.shg_name" required>
            <!-- <div v-if="shg_list and show_shg" class="mt-3">
              <ul>
                <li> Test SHG Name</li>
              </ul> 
            </div> -->
          </div>
          <div class="form-group">
            <label for="village">Village:</label>
            <input type="text" class="form-control" id="village" v-model="formData.village">
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
            <input type="text" class="form-control" id="father_husband_name" v-model="formData.father_husband_name" required>
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
            <select class="form-control" id="category" v-model="formData.category" >
              <option value="General">General</option>
              <option value="ST">ST</option>
              <option value="SC">SC</option>
              <option value="OBC">OBC</option>
            </select>
          </div>
          <div class="form-group">
            <label for="caste">Caste:</label>
            <!-- Add options here -->
            <select class="form-control" id="caste" v-model="formData.caste">
              <option value='Yadav (Ahir, Gowala, Gora, Ghasi, Mehar and Sadgop)' >Yadav (Ahir, Gowala, Gora, Ghasi, Mehar and Sadgop)</option>
              <option value='Dushadh (Dhari, Dharahi)' >Dushadh (Dhari, Dharahi)</option>
              <option value='Ravidas (Mochi, Ravidas, Rohidas, Charmkar)' >Ravidas (Mochi, Ravidas, Rohidas, Charmkar)</option>
              <option value='Kushwaha (Koeri)' >Kushwaha (Koeri)</option>
              <option value='Shaikh (caste) (Muslim)' >Shaikh (caste) (Muslim)</option>
              <option value='Brahmin' >Brahmin</option>
              <option value='Momin (Muslim)/Julaha/Ansari (Muslim)' >Momin (Muslim)/Julaha/Ansari (Muslim)</option>
              <option value='Rajput' >Rajput</option>
              <option value='Musahar' >Musahar</option>
              <option value='Kurmi' >Kurmi</option>
              <option value='Bhumihar' >Bhumihar</option>
              <option value='Teli' >Teli</option>
              <option value='Mallah (Nishad)' >Mallah (Nishad)</option>
              <option value='Bania(Sudhi, Modak/Mamas, Roniyar, Pansari, Modi, Karora, Kesharvani, Thathera, Kalwar (Kalal/Iraqi), (Vigahut Kalwar), Kamlapuri Vaishya, Mahuri Vaishya, Bangi Vaishya (Bangali Baniya), Baranwal Vaishya, Agrahari Vaishya, Vaishya Poddar, Kasaudhan, Gandhbanik, Batham Vaishya, Goldar (East/Wesh Champaran)' >Bania(Sudhi, Modak/Mamas, Roniyar, Pansari, Modi, Karora, Kesharvani, Thathera, Kalwar (Kalal/Iraqi), (Vigahut Kalwar), Kamlapuri Vaishya, Mahuri Vaishya, Bangi Vaishya (Bangali Baniya), Baranwal Vaishya, Agrahari Vaishya, Vaishya Poddar, Kasaudhan, Gandhbanik, Batham Vaishya, Goldar (East/Wesh Champaran)</option>
              <option value='Kanu' >Kanu</option>
              <option value='Dhanuk' >Dhanuk</option>
              <option value='Nonia' >Nonia</option>
              <option value='Surjapuri Muslim ( except Sheikh, Syed, Mullick, Mughal, Pathan) (Muslim)' >Surjapuri Muslim ( except Sheikh, Syed, Mullick, Mughal, Pathan) (Muslim)</option>
              <option value='Pan, Sawasi, Panar' >Pan, Sawasi, Panar</option>
              <option value='Nai' >Nai</option>
              <option value='Chandravanshi (Kahar, Kamkar)' >Chandravanshi (Kahar, Kamkar)</option>
              <option value='Barhai (carpenter)' >Barhai (carpenter)</option>
              <option value='Dhuniya (Muslim)' >Dhuniya (Muslim)</option>
              <option value='Kumhar (Prajapati)' >Kumhar (Prajapati)</option>
              <option value='Rayeen or Kunjra (Muslim)' >Rayeen or Kunjra (Muslim)</option>
              <option value='Shershahbadi (Muslim)' >Shershahbadi (Muslim)</option>
              <option value='Pasi' >Pasi</option>
              <option value='Bind' >Bind</option>
              <option value='Kulhaiya (Muslim)' >Kulhaiya (Muslim)</option>
              <option value='Bhuiya' >Bhuiya</option>
              <option value='Dhobi (Rajak)' >Dhobi (Rajak)</option>
              <option value='Pathan (Khan) (Muslim)' >Pathan (Khan) (Muslim)</option>
              <option value='Sonar' >Sonar</option>
              <option value='Kayastha' >Kayastha</option>
              <option value='Sai/Faqeer/Diwan/Madar (Muslim)' >Sai/Faqeer/Diwan/Madar (Muslim)</option>
              <option value='Gangota (Gangaputra)' >Gangota (Gangaputra)</option>
              <option value='Barai, Tamoli, Chaurasiya' >Barai, Tamoli, Chaurasiya</option>
              <option value='Dhobi (Muslim)' >Dhobi (Muslim)</option>
              <option value='Pal (Bhedihar,gaderi, gaderiya)' >Pal (Bhedihar,gaderi, gaderiya)</option>
              <option value='Mali' >Mali</option>
              <option value='Dangi' >Dangi</option>
              <option value='Idrisi or Darzi (Muslim)' >Idrisi or Darzi (Muslim)</option>
              <option value='Syed (Muslim)' >Syed (Muslim)</option>
              <option value='Dom, Dhangadh, Bansfor, Dharikar, Dharkar, Domra' >Dom, Dhangadh, Bansfor, Dharikar, Dharkar, Domra</option>
              <option value='Hari Mehtar, Bhangi' >Hari Mehtar, Bhangi</option>
              <option value='Rajbhar' >Rajbhar</option>
              <option value='Chudihar (Muslim)' >Chudihar (Muslim)</option>
              <option value='Thakurai (Muslim)' >Thakurai (Muslim)</option>
              <option value='Qasab (Qasai) (Muslim)' >Qasab (Qasai) (Muslim)</option>
              <option value='Mullick (Muslim)' >Mullick (Muslim)</option>
              <option value='Nat' >Nat</option>
              <option value='Bhat (Muslim)' >Bhat (Muslim)</option>
              <option value='Madariya (Only for Sanhaul block of Bhagalpur and Dhoriya block of Banka) (Muslim)' >Madariya (Only for Sanhaul block of Bhagalpur and Dhoriya block of Banka) (Muslim)</option>
              <option value='Daphali (Muslim)' >Daphali (Muslim)</option>
              <option value='Mehtar, Lalbegi, Halalkhor, Bhangi (Muslim)' >Mehtar, Lalbegi, Halalkhor, Bhangi (Muslim)</option>
              <option value='Morshikar(Muslim)' >Morshikar(Muslim)</option>
              <option value='Pamaria (Muslim)' >Pamaria (Muslim)</option>
              <option value='Nat (Muslim)' >Nat (Muslim)</option>
              <option value='Gaddi (Muslim)' >Gaddi (Muslim)</option>
              <option value='Mukairi (Muslim)' >Mukairi (Muslim)</option>
              <option value='Cheeq (Muslim)' >Cheeq (Muslim)</option>
              <option value='Jat (Muslim (Madhubani, Darbhanga, Sitamadhi, Khagaria & Araria) (Muslim)' >Jat (Muslim (Madhubani, Darbhanga, Sitamadhi, Khagaria & Araria) (Muslim)</option>
              <option value='Rangrez (Muslim)' >Rangrez (Muslim)</option>
              <option value='Bakho (Muslim)' >Bakho (Muslim)</option>
              <option value='Bhathiyara (Muslim)' >Bhathiyara (Muslim)</option>
              <option value='Sainthwar' >Sainthwar</option>
              <option value='Saikalgarg (Muslim)' >Saikalgarg (Muslim)</option>
              <option value='Qadar (Muslim)' >Qadar (Muslim)</option>
              <option value='Miriyasin (Muslim)' >Miriyasin (Muslim)</option>
              <option value='Nalband (Muslim)' >Nalband (Muslim)</option>
              <option value='Christian Convert (EBC)' >Christian Convert (EBC)</option>
              <option value='Madari (Muslim)' >Madari (Muslim)</option>
              <option value='Abdal (Muslim)' >Abdal (Muslim)</option>
              <option value='Christian Convert (Harijan)' >Christian Convert (Harijan)</option>
              <option value='Itfarosh/Itafarosh/Gadheri/Itpaz Ibrahimi (Muslim)' >Itfarosh/Itafarosh/Gadheri/Itpaz Ibrahimi (Muslim)</option>
              <option value='Qalandar (Muslim)' >Qalandar (Muslim)</option>
              <option value='Qaghzi(Muslim)' >Qaghzi(Muslim)</option>
            </select>
          </div>
        </div>
        <div class="col-md-6">
          <!-- Household Information -->
          <h2>Household Information</h2>
          <div class="form-group">
            <label for="number_of_family_members">Number of Family Members:</label>
            <input type="number" class="form-control" id="number_of_family_members" v-model="formData.number_of_family_members">
          </div>
          <div class="form-group">
            <label for="mobile_number">Mobile Number:</label>
            <input type="text" class="form-control" id="mobile_number" v-model="formData.mobile_number" required pattern="[0-9]{10}">
          </div>
          <div class="form-group">
            <label for="total_land_kattha">Total Land (Kattha):</label>
            <input type="number" class="form-control" id="total_land_kattha" v-model="formData.total_land_kattha">
          </div>
          <div class="form-group">
            <label for="total_irrigated_land_kattha">Total Irrigated Land (Kattha):</label>
            <input type="number" class="form-control" id="total_irrigated_land_kattha" v-model="formData.total_irrigated_land_kattha">
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
            <input type="number" class="form-control" id="total_no_of_members_migrated" v-model="formData.total_no_of_members_migrated">
          </div>
          <div class="form-group">
            <label for="main_source_of_income">Main Source of Income:</label>
            <input type="text" class="form-control" id="main_source_of_income" v-model="formData.main_source_of_income">
          </div>
          <div class="form-group">
            <label for="head_of_the_family_name">Head of the Family Name:</label>
            <input type="text" class="form-control" id="head_of_the_family_name" v-model="formData.head_of_the_family_name">
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
      </div>
      <button type="submit" class="btn btn-primary">Submit</button>
    </form>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'memberEntry',

  data() {
    return {
      shg_list: [],
      formData: {
        member_id: null,
        shg_name: null,
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
        IFSC_code: ''
      }
    };
  },
  methods: {
    addMember() {

      axios.post('http://127.0.0.1:8000/api/member/', this.formData, { headers: { 'Token': localStorage.getItem('token') } } 
    ).then((response) => {
      if (response === 200){
        alert("Member Added Successfully")

      }
    })
  }, 

  fetchSHG(){
    axios.get('http://127.0.0.1:8000/api/shg', { headers: { 'Token': localStorage.getItem('token') } } ).then((response) => {
      this.shg_list = response.data
  })
}
  },
 created() {
  this.fetchSHG();
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

.form-group {
    display: flex;
    flex-direction: row;
    width: 100;
    text-wrap: nowrap;
    margin: 1%;
}

.form-group > * {
    margin-right: 1%;
    margin-left: 1%;
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