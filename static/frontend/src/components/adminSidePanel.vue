<template>
    <div class="side-panel card d-flex flex-column justify-content-start" >
        <div class="card-header custom-card-format">
             Actions
        </div>
        
        <div class="element" > 
            <RouterLink to="/dashboard">Home</RouterLink>
            <!-- <a href="">Group Data Entry</a> -->
        </div>
        
        <div class="element"> 
            <RouterLink to="/newUser">Create New User</RouterLink>
            <!-- <a href="">Group Data Entry</a> -->
        </div>
        
        <div class="element"> 
            <RouterLink to="/deleteUser">Delete User</RouterLink>
        </div>

        <div class="element"> 
            <RouterLink to="/changePassword">Change Password</RouterLink>
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