<template>
    <div class="container-fluid bg-extra-light text-dark" id="user-profile-body">
        <!-- IMG, FULLNAME AND USERNAME -->
        <div class="row justify-content-center py-5">
            <div class="rounded-circle profile-circle col-auto">
                {{ first_name.slice(0,1) }}
            </div>

            <div class="col-auto d-flex justify-content-center flex-column">
                <h1>{{ first_name }} {{ last_name }}</h1>
                <h4 class="fst-italic fw-semibold">@{{ username }}</h4>
            </div>
        </div>

        <!-- DISPLAY: ALL USER DETAILS -->

        <!-- First Name -->
        <div class="row justify-content-center">
            <div class="col-6">
                <p class="fw-bold text-end">
                    First Name:
                </p>
            </div>

            <div class="col-6">
                <p>
                    {{ first_name }}
                </p>
            </div>
        </div>

        <!-- Last Name -->
        <div class="row justify-content-center">
            <div class="col-6">
                <p class="fw-bold text-end">
                    Last Name:
                </p>
            </div>

            <div class="col-6">
                <p>
                    {{ last_name }}
                </p>
            </div>
        </div>

        <!-- Default Adress -->
        <div class="row justify-content-center">
            <div class="col-6">
                <p class="fw-bold text-end">
                    Default Adress:
                </p>
            </div>

            <div class="col-6">
                <p>
                    {{ address }}
                </p>
            </div>
        </div>

        <!-- Phone Number -->
        <div class="row justify-content-center">
            <div class="col-6">
                <p class="fw-bold text-end">
                    Phone Number:
                </p>
            </div>

            <div class="col-6">
                <p>
                    {{ number }}
                </p>
            </div>
        </div>

        <!-- Email -->
        <div class="row justify-content-center">
            <div class="col-6">
                <p class="fw-bold text-end">
                    Email:
                </p>
            </div>

            <div class="col-6">
                <p>
                    {{ email }}
                </p>
            </div>
        </div>

        <!-- Travel Appetite -->
        <div class="row justify-content-center">
            <div class="col-6">
                <p class="fw-bold text-end">
                    Travel Appetite:
                </p>
            </div>

            <div class="col-6">
                <p>
                    {{ travel_appetite }}
                </p>
            </div>
        </div>

        <!-- Dietary Restrictions -->
        <div class="row justify-content-center">
            <div class="col-6">
                <p class="fw-bold text-end">
                    Dietary Restrictions:
                </p>
            </div>

            <div class="col-6">
                <p>
                    {{ dietary_res.join(', ') }}
                </p>
            </div>
        </div>

    </div>
</template>


<script>
    export default{
        data() {
            return {
                first_name: '',
                last_name: '',
                username: '',
                number: '',
                address: '',
                dietary_res: [],
                email: '',
                travel_appetite: '',
            }
        },

        methods: {
            update_user_details() {
                var user_deets = this.$store.state.user_details

                this.first_name = user_deets.first_name,
                this.last_name = user_deets.last_name,
                this.username = user_deets.username,
                this.number = user_deets.number,
                this.address = user_deets.address,
                this.email = user_deets.email,
                this.travel_appetite = user_deets.travel_appetite,
                this.username = user_deets.username

                var str_dietres = user_deets.dietary_type
                if (str_dietres == '') {
                    return
                } else {
                    for (var e_diet_res of str_dietres.split(",")) {
                        this.dietary_res.push(e_diet_res.toLowerCase())
                    }
                }
            }
        },

        created() {
            this.update_user_details()
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