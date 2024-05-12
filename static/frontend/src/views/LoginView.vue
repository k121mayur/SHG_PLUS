<template>
    <h1 class="my-3">Welcome</h1>
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