<template>
    <div class="container-fluid bg-dark text-light" id="login-body">
        <img src="../assets/images/logos/large_logos/MakanBoleh_logo_stacked_light_large.png" class="logo_img">

        <form class="register-form" style="width: 350px">
            <div class="form-row mt-5">
                <div class="row">
                    <div class="col-md-6">
                        <div class="small form-floating mb-3 text-dark">
                            <input type="text" class="form-control" id="floatingInput" placeholder="First Name">
                            <label for="floatingInput">First Name</label>
                        </div>
                    </div>
                    <div class="col-md-6">
                        <div class="small form-floating mb-3 text-dark">
                            <input type="text" class="form-control" id="floatingInput" placeholder="Last Name">
                            <label for="floatingInput">Last Name</label>
                        </div>
                    </div>
                </div>
                <div class="small form-floating mb-3 text-dark">
                    <input type="text" class="form-control" id="floatingInput"
                    placeholder="name@example.com">
                    <label for="floatingInput">Username</label>
                </div>

                <div class="small form-floating mb-3 text-dark">
                    <input type="password" class="form-control" id="floatingPassword" placeholder="Password">
                    <label for="floatingPassword">Password</label>
                </div>

                <div class="small form-floating text-dark">
                    <input type="password" class="form-control" id="floatingPassword" placeholder="Password">
                    <label for="floatingPassword">Confirm Password</label>
                </div>
            </div>
        </form>

        <div class="d-flex justify-content-center">
            <button class="btn btn-main mt-3">Sign up</button>
        </div>

        <hr class="mt-3" style="width: 340px">
        <div class="mt-3 text-center">
            Have an account? <router-link to="/login">Log in</router-link>
        </div>

        <!-- <form action="" class="d-flex flex-column mt-3">
            <small>Username</small>
            <input type="text">

            <small>Password</small>
            <input type="password">

            <div class="d-flex justify-content-center">
                <button class="btn btn-main mt-3">Login</button>
            </div>
        </form> -->
    </div>
</template>


<script>

    export default{
        data() {
            return {

            }
        }
    }
</script>


<style scoped>
    #login-body{
        height: 100%;
        display: flex;
        justify-content: center;
        align-items: center;
        flex-direction: column;
    }

    .logo_img{
        width: 250px
    }

    hr {
        margin: 0px 15px;
        border-top: 2px solid;
        width: 145px;
    }

    #text-divider {
        flex: 0.3 1 0%;
    }

    /* .form-floating {
        width: 340px;
    } */
</style>