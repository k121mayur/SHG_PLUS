<template>
    <div class="container border mx-auto custom">
        <form class=" p-3 flex">
            <div class="form-group my-3 d-flex flex-row justify-content-end">
                <label for="role" style="text-wrap: nowrap;" class="m-3" >Role</label>
                <select type="email" class="form-control" id="role" style="width: 70%;" required > 
                    <option value="admin" >Admin</option>
                    <option value="operator" selected>Data Entry Operator</option>
                    <option value="manager" >Project Manager</option>
                    </select>

            </div>
            <div class="form-group my-3 d-flex flex-row justify-content-end">
                <label for="exampleInputEmail1" style="text-wrap: nowrap;" class="m-3" >Email address</label>
                <input type="email" class="form-control" id="exampleInputEmail1" style="width: 70%;" aria-describedby="emailHelp" placeholder="Enter email" required>

            </div>
            <div class="form-group d-flex flex-row justify-content-end">
                <label for="exampleInputPassword1" style="text-wrap: nowrap;" class="m-3">Password</label>
                <input type="password" class="form-control" style="width: 70%;" id="exampleInputPassword1" placeholder="Password" required>
            </div>
       
            <button type="submit" class="btn btn-primary my-3">Login</button>
        </form>
    </div>
</template>

<style>
    .custom {
        width: 40%;
        border-radius: 20px;

    }
</style>


<script>
export default {
  name: 'loginForm',
}
</script>