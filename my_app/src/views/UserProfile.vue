<template>
    <div class="container-fluid bg-dark text-light" id="user-profile-body">
        <div class="row">
            <div class="col-12 col-xl-3 d-flex mx-auto">
                <div class="rounded-circle profile-circle">
                    S
                </div>
                <div class="">Tan Sheng Da</div>
                <div class="">@shengdaa</div>
            </div>
            <div class="col-9">
                
            </div>
        </div>

        <div class="">Travel Appetite</div>
        <div class="">My Saved Addresses</div>
        <div class="">My Food Post</div>
        <div class="">My Forum Post</div>
       
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
    #user-profile-body{
        height: 100%;
        /* display: flex;
        justify-content: center;
        align-items: center;
        flex-direction: column; */
    }

    .profile-circle {
        background: white;
        color: #f3704b;
        width: 150px;
        height: 150px;
        border-radius: 50%;
        font-size: 90px;
        display: flex;
        align-items: center;
        justify-content: center;
    }
</style>