<template>
    <div class="side-panel card d-flex flex-column justify-content" >
        <div class="card-header custom-card-format">
             Actions
        </div>
        
        <div class="element"> 
            <i class="fa fa-house"></i>
            <RouterLink to="/dashboard">Home</RouterLink>
            <!-- <a href="">Group Data Entry</a> -->
        </div>
        
        <div class="element"> 
            <i class="fa-solid fa-database"></i>
            <RouterLink to="/dataEntry">Group Data Entry</RouterLink>
            <!-- <a href="">Group Data Entry</a> -->
        </div>
        
        <div class="element"> 
            <i class="fa-regular fa-file"></i>
            <RouterLink to="/dataEntryReport">Data Entry Report</RouterLink>
        </div>


        <div class="element"> 
            <i class="fa-solid fa-building-columns"></i>
            <a href="#">Add Bank Accounts</a>
        </div class="element">
        
        <div class="element"> 
            <i class="fa-solid fa-user"></i>
            <RouterLink to="/newMember">Add SHG Member</RouterLink>
        </div class="element">

        <div class="element"> 
            <i class="fa-solid fa-people-group"></i>
            <RouterLink to="/newGroup">New SHG (+) Entry</RouterLink>
        </div>

        <div class="element"> 
            <i class="fa-solid fa-group-arrows-rotate"></i>
            <RouterLink to="/shareout">Shareout Report</RouterLink>
        </div>

        
    
    </div>

</template>

<style scoped>
.side-panel {
        height: 85vh;
        border: solid 1px black;
        margin-left: 0;
        border-radius : 10px;
        overflow: auto;
        margin-top: 1%;

    }

    .element {
        background-color: white;
        color: black;
        padding : 4%;
        border-radius: 5px;
        font-family: Verdana, Geneva, Tahoma, sans-serif;
        
    }

    .element > a {
        text-decoration: none;
        color: black;
        width: 100%;
        height: 10px;
        padding: 4%;
    }

    a:hover {
        color : white;
    }

    .element:hover {
        background-color: green;
        color : white;
        cursor: pointer;
    }

    .custom-card-format {
        background-color: maroon;
        color: white;
        font-family: 'Times New Roman', Times, serif;
        font: 1.5em sans-serif;
    }

    
</style>