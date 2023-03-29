<template>
    <div class="fill-space bg-light">
        <div class="forum-body pb-5">
            <!-- LOADING CARDS -->
            <div v-if="loading_posts" aria-hidden="true">
                <div class="card mx-3 mx-md-auto my-3 placeholder-wave" v-for="e_id in 3" :key="e_id">
                    <!-- HEADER -->
                    <div class="card-header bg-dark text-light">
                        <div class="post-title">
                            <span class="placeholder col-10"></span>
                            <span class="placeholder placeholder-xs col-5"></span>
                        </div>
                    </div>
            
                    <!-- BODY -->
                    <div class="card-body bg-extra-light">
                        <span class="placeholder col-10"></span>
                        <span class="placeholder placeholder-xs col-7"></span>
                        <span class="placeholder placeholder-xs col-6"></span>
                    </div>
                </div>
            </div>

            <!-- LOADED CARDS -->
            <div class="card mx-3 mx-md-auto text-dark my-3" v-for="e_post in forum_data" :key="e_post.forum_id">
                <!-- HEADER -->
                <div class="card-header bg-dark text-extra-light">
                    <div class="d-flex">
                        <div class="post-user-img">
                            <font-awesome-icon icon="fa-solid fa-circle-user" size="2xl" />
                        </div>
        
                        <div class="post-title">
                            <h6 class="my-0">{{ e_post.title }}</h6>
                            <small><span class="fw-semibold">@{{ e_post.username }}</span> {{ convert_datetime_to_readable(e_post.datetime) }}</small>
                        </div>
                    </div>
                </div>
        
                <!-- BODY -->
                <div class="card-body bg-extra-light">
                    <p class="card-text">{{ e_post.description }}</p>
        
                    <button class="btn btn-main py-1 px-2" type="button" data-bs-toggle="collapse" :data-bs-target="`#collapse-${e_post.forum_id}`" aria-expanded="false" :aria-controls="`#collapse-${e_post.forum_id}`">
                        <small class="fw-bold"><font-awesome-icon icon="fa-solid fa-comments" />&nbsp;{{ e_post.comments.length }}</small>
                    </button>
                </div>
                
                <!-- COMMENTS -->
                <div class="collapse bg-extra-light" :id="`collapse-${e_post.forum_id}`">
                    <div v-for="(e_comment, index) in e_post.comments" :key="index">
                        <div class="card-footer d-flex">
                            <div class="post-user-img">
                                <font-awesome-icon icon="fa-solid fa-circle-user" size="2xl" />
                            </div>
            
                            <div class="post-title">
                                <p class="my-0"><span class="fw-semibold">@{{ e_comment.username }}</span> {{ convert_datetime_to_readable(e_comment.datetime) }}</p>
                                <p class="mt-1 mb-0">{{ e_comment.description }}</p>
                            </div>
                        </div>
                    </div>
        
                    <div class="card-footer">
                        <div class="input-group my-2">
                            <input type="text" class="form-control" placeholder="Add comment" :aria-describedby="`forum-${e_post.forum_id}-add-comment`">
                            <button class="btn btn-dark" type="button" :id="`forum-${e_post.forum_id}-add-comment`">Reply</button>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <button class="btn btn-main-fixed post-btn" data-bs-toggle="modal" :data-bs-target="isAuthenticated ? `#new-comment` : ``" @click="redirect_to_login()"><font-awesome-icon icon="fa-solid fa-plus" /><span> Create Thread</span></button>
        <!-- <button class="btn btn-main-fixed post-btn" data-bs-toggle="modal" data-bs-target="#new-comment" @click="redirect_to_login()"><font-awesome-icon icon="fa-solid fa-plus" /><span> Create Thread</span></button> -->
    </div>

    <div class="modal fade" id="new-comment" tabindex="-1" aria-labelledby="modal-title" aria-hidden="true">
        <div class="modal-dialog">
            <div class="modal-content bg-light text-dark">
                <div class="modal-header bg-dark text-extra-light">
                    <h5 class="modal-title" id="modal-title"><font-awesome-icon icon="fa-solid fa-comments" /> Create Forum Post</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>

                <div class="modal-body">
                    <div class="form-floating">
                        <input type="text" class="form-control" id="post-title" placeholder=" " v-model="create_post_title">
                        <label for="post-title">Title</label>
                    </div>

                    <div class="form-floating mt-4">
                        <textarea class="form-control" placeholder=" " id="post-content" v-model="create_post_desc"></textarea>
                        <label for="post-content">What do you want to tell people about?</label>
                    </div>

                    <div class="d-flex justify-content-center mt-3">
                        <button class="btn btn-main" @click="submit_new_post()" :disabled="loading_post_button">
                            <font-awesome-icon icon="fa-solid fa-paper-plane" v-if="!loading_post_button" />
                            <font-awesome-icon :icon="['fas', 'spinner']" v-if="loading_post_button" spin />&nbsp;&nbsp;Post
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>


<script>
import router from '@/router';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import axios from 'axios';

    export default{
    data() {
        return {
            create_post_title: "",
            create_post_desc: "",
            forum_data: [],
            loading_posts: true,
            loading_post_button: false,

            // PRESET FORUM DATA
            // [
            //     {
            //         forum_id: 0,
            //         username: "adambft",
            //         title: "Free Food @ Salesforce Event!",
            //         description: "Come down to Saleforce office at 123 Bugis Street 25 to enjoy free drinks and food on 30 Apr 2023 2-4pm!",
            //         datetime: "2023-03-12T08:30:00",
            //         comments: [
            //             { username: "sethyap", description: "Fk you Salesforce sucks", datetime: "2023-03-12T09:12:00" },
            //             { username: "angkengboon", description: "No, fk you I love Salesforce. SF is bae <3 uwu", datetime: "2023-03-12T10:20:00" }
            //         ]
            //     }
            // ]
        };
    },
    methods: {
        convert_datetime_to_readable(date_time_str) {
            let x = new Date(date_time_str);
            let res = `${x.getDate()} ${x.toLocaleString("default", { month: "short" })} ${x.getFullYear()} | ${x.toLocaleString("default", { timeStyle: "short" })}`;

            return res;
        },

        redirect_to_login() {
            //check if user logged in, redirect if not
            if (!this.isAuthenticated) {
                router.push({path: '/login'})
            }
        },

        submit_new_post() {
            this.loading_post_button = true

            axios.post("http://localhost:5100/create_post", {
                "username": this.$store.state.user_details.username,
                "title": this.create_post_title,
                "description": this.create_post_desc,
                "datetime": new Date()
            })
            .then(function (response) {
                console.log(response)
                location.reload()
            })
            .catch(function(error) {
                console.log(error)
            })
        },

        update_posts() {
            axios.get('http://localhost:5100/posts')
            .then(response => {
                // console.log("HERE U GO: ", response.data.data.forum)
                let response_data = response.data.data.forum

                //FOR TESTING: REPLACE/ DELETE ONCE RACHAEL FINISH ADDING COMMENTS TO JSON RESPONSE
                for (let e_post of response_data) {
                    if (!('comments' in e_post)) {
                        e_post.comments = []
                    }
                }

                this.forum_data = response_data
                this.loading_posts = false
            })
            .catch(error => {
                console.log("Error on Forum.vue API call to get all posts: ", error.message);
            });
        }
    },
    computed: {
        isAuthenticated() {
            return this.$store.state.isAuthenticated
        }
    },
    components: { FontAwesomeIcon },
    created() {
        this.update_posts()
    },
}
</script>


<style scoped>
    #post-content{
        height: 100px;
    }

    .fill-space{
        height: 100%;
        position: relative;
    }

    .post-btn{
        position: absolute;
        bottom: 0;
        right: 0;
        margin: 20px 30px;
        z-index: 2;
    }

    .forum-body{
        height: 100%;
        overflow-y: scroll;
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
    }

    .post-user-img{
        flex: 0 1 auto;
        display: flex;
        justify-content: center;
        align-items: center;
        flex-direction: column;
    }

    .post-title{
        flex: 1 1 auto;
        margin-left: 20px;
    }

    /* SMALLER THAN 769 */
    @media (max-width: 769px) {
        .post-btn{
            border-radius: 50%;
        }

        .post-btn > span{
            display: none;
        }
    }

    /* LARGER THAN 769 */
    @media (min-width: 769px) {
        .card{
            width: 80vw;
        }
    }
</style>