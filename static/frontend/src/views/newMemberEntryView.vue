<template> 
        <div class="d-flex flex-row m-0 col-md-12 panel"> 
            <SidePanel class="col-md-2"/>
            <memberEntry
            class="main-panel col-md-10" />
        </div>

</template>

<script>
import SidePanel from "@/components/SidePanel.vue"
import memberEntry from "@/components/memberEntry.vue"


export default {
    name: 'newMemberEntryView',
    components: {
        SidePanel, 
        memberEntry 
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