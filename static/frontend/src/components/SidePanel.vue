<template>
    <div class="side-panel card d-flex flex-column justify-content" >
        <div class="card-header custom-card-format">
             Actions
        </div>
        <div class="element"> 
            <RouterLink to="/">Home</RouterLink>
            <!-- <a href="">Group Data Entry</a> -->
        </div>
        <div class="element"> 
            <RouterLink to="/dataEntry">Group Data Entry</RouterLink>
            <!-- <a href="">Group Data Entry</a> -->
        </div>
        <div class="element"> 
           <a href="#"> Data Entry Report </a>
        </div>
        <div class="element"> 
            <a href="#">Shareout</a>
        </div class="element">
        <div class="element"> 
            <a href="/newMember">Add / Remove Member</a>
        </div class="element">

        <div class="element"> 
            <a href="/newGroup">New Group Entry </a>
        </div>

        <div class="element"> 
            <a href="#">Edit Group Details</a>
        </div class="element">
    
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