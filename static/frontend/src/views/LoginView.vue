<template>
    <h1 class="my-5 gradient-text">Welcome to SHG PLUS</h1>
    <loginForm/>

</template>
<script>
import loginForm  from "@/components/loginForm.vue"

export default {
    name: 'loginView',
    components: {
        loginForm
    }
}
</script>

<style scoped>
.gradient-bg-horizontal {
    color: linear-gradient(to right, #006400, #ffa500);
}

.gradient-text {
    background: linear-gradient(to right, #006400, #32cd32, #ffa500, #ff4500);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}



</style>