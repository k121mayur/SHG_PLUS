<template>
    <div class="side-panel card d-flex flex-column justify-content" >
        <div class="card-header custom-card-format">
             Actions
        </div>
        
        <div class="element"> 
            <RouterLink to="/dashboard">Home</RouterLink>
            <!-- <a href="">Group Data Entry</a> -->
        </div>
        
        <div class="element"> 
            <RouterLink to="/dataEntryReport">Data Entry Report</RouterLink>
        </div>

        <div class="element"> 
            <RouterLink to="/savingsReport">Monthly Report</RouterLink>
        </div>
        
        <div class="element"> 
            <RouterLink to="/creditReport">Monthly Credit Report</RouterLink>
        </div class="element">

        <div class="element"> 
            <RouterLink to="/dissolveGroupReport">dissolved Group Report</RouterLink>
        </div>
    
    </div>



</template>

<script>



export default {
    name: 'managerSidePanel'
}



</script>

<style>
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