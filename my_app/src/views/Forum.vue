<template>
    <div class="fill-space bg-light">
        <div class="forum-body pb-5">
            <!-- LOADING CARDS -->
            <div v-if="loading_posts" aria-hidden="true">
                <div
                    class="card mx-3 mx-md-auto my-3 placeholder-wave"
                    v-for="e_id in 3"
                    :key="e_id"
                >
                    <!-- HEADER -->
                    <div class="card-header bg-dark text-light">
                        <div class="post-title">
                            <span class="placeholder col-10"></span>
                            <span
                                class="placeholder placeholder-xs col-5"
                            ></span>
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
            <div
                class="card mx-3 mx-md-auto text-dark my-3"
                v-for="e_post in forum_data"
                :key="e_post.forum_id"
            >
                <!-- HEADER -->
                <div class="card-header bg-dark text-extra-light">
                    <div class="d-flex">
                        <div class="post-user-img">
                            <font-awesome-icon
                                icon="fa-solid fa-circle-user"
                                size="2xl"
                            />
                        </div>

                        <div class="post-title">
                            <h6 class="my-0">{{ e_post.title }}</h6>
                            <small
                                ><span class="fw-semibold"
                                    >@{{ e_post.username }}</span
                                >
                                {{
                                    convert_datetime_to_readable(
                                        e_post.datetime
                                    )
                                }}</small
                            >
                        </div>

                        <div class="btn btn-main-dark-fixed h-50 fw-semibold" v-if=" this.forumList.includes(e_post.forum_id)" @click="removePost(e_post.forum_id)"><font-awesome-icon icon="fa-solid fa-trash" /></div>
                    </div>
                </div>

                <!-- BODY -->
                <div class="card-body bg-extra-light">
                    <p class="card-text">{{ e_post.description }}</p>

                    <button
                        class="btn btn-main py-1 px-2"
                        type="button"
                        data-bs-toggle="collapse"
                        :data-bs-target="`#collapse-${e_post.forum_id}`"
                        aria-expanded="false"
                        :aria-controls="`#collapse-${e_post.forum_id}`"
                    >
                        <small class="fw-bold"
                            ><font-awesome-icon
                                icon="fa-solid fa-comments"
                            />&nbsp;{{ e_post.comments.length }}</small
                        >
                    </button>
                </div>

                <!-- COMMENTS -->
                <div
                    class="collapse bg-extra-light"
                    :id="`collapse-${e_post.forum_id}`"
                >
                    <!-- CURRENT COMMENTS -->
                    <div
                        v-for="(e_comment, index) in e_post.comments"
                        :key="index"
                    >
                        <div class="card-footer d-flex">
                            <div class="post-user-img">
                                <font-awesome-icon
                                    icon="fa-solid fa-circle-user"
                                    size="2xl"
                                />
                            </div>

                            <div class="post-title">
                                <p class="my-0">
                                    <span class="fw-semibold"
                                        >@{{
                                            e_comment.commentor_username
                                        }}</span
                                    >
                                    {{
                                        convert_datetime_to_readable(
                                            e_comment.datetime
                                        )
                                    }}
                                </p>
                                <p class="mt-1 mb-0">{{ e_comment.comment }}</p>
                            </div>
                        </div>
                    </div>

                    <!-- ADD NEW COMMENT -->
                    <div
                        class="card-footer"
                        v-if="this.$store.state.isAuthenticated"
                    >
                        <div class="input-group my-2">
                            <input
                                type="text"
                                class="form-control"
                                placeholder="Add comment"
                                :aria-describedby="`forum-${e_post.forum_id}-add-comment`"
                                v-model="comment_input_data[e_post.forum_id]"
                            />
                            <button
                                class="btn btn-dark"
                                type="button"
                                :disabled="sending_comment_id"
                                :id="`forum-${e_post.forum_id}-add-comment`"
                                @click="submit_new_comment(e_post.forum_id)"
                            >
                                <font-awesome-icon
                                    :icon="['fas', 'spinner']"
                                    v-if="sending_comment_id == e_post.forum_id"
                                    class="me-2"
                                    spin
                                />Reply
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <button
            class="btn btn-main-fixed post-btn"
            data-bs-toggle="modal"
            :data-bs-target="isAuthenticated ? `#new-comment` : ``"
            @click="redirect_to_login()"
        >
            <font-awesome-icon icon="fa-solid fa-plus" /><span>
                Create Thread</span
            >
        </button>
    </div>

    <div
        class="modal fade"
        id="new-comment"
        tabindex="-1"
        aria-labelledby="modal-title"
        aria-hidden="true"
    >
        <div class="modal-dialog">
            <div class="modal-content bg-light text-dark">
                <div class="modal-header bg-dark text-extra-light">
                    <h5 class="modal-title" id="modal-title">
                        <font-awesome-icon icon="fa-solid fa-comments" /> Create
                        Forum Post
                    </h5>
                    <button
                        id="forum_create_close_btn"
                        type="button"
                        class="btn-close"
                        data-bs-dismiss="modal"
                        aria-label="Close"
                    ></button>
                </div>

                <div class="modal-body">
                    <div class="form-floating">
                        <input
                            type="text"
                            class="form-control"
                            id="post-title"
                            placeholder=" "
                            v-model="create_post_title"
                        />
                        <label for="post-title">Title</label>
                    </div>

                    <div class="form-floating mt-4">
                        <textarea
                            class="form-control"
                            placeholder=" "
                            id="post-content"
                            v-model="create_post_desc"
                        ></textarea>
                        <label for="post-content"
                            >What do you want to tell people about?</label
                        >
                    </div>

                    <div class="d-flex justify-content-center mt-3">
                        <button
                            class="btn btn-main"
                            @click="submit_new_post()"
                            :disabled="loading_post_button"
                        >
                            <font-awesome-icon
                                icon="fa-solid fa-paper-plane"
                                v-if="!loading_post_button"
                            />
                            <font-awesome-icon
                                :icon="['fas', 'spinner']"
                                v-if="loading_post_button"
                                spin
                            />&nbsp;&nbsp;Post
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import router from "@/router";
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import axios from "axios";
const filteredResult = 'http://localhost:1115/search'
const removePost = 'http://localhost:1115/edit'

export default {
    data() {
        return {
            create_post_title: "",
            create_post_desc: "",
            forum_data: [],
            loading_posts: true,
            loading_post_button: false,
            comment_input_data: {},
            sending_comment_id: null,
            forumList: [],
        };
    },
    methods: {
        removePost(forum_id) {
            var vm = this
            axios.put(`${removePost}/${forum_id}`)
            .then(response => {
                console.log(response.data)
                if (response.data.code == 200) {
                    console.log("Successfully removed post.")
                    vm.update_posts(false)
            }
        })
            .catch(error => {
                console.log(error.message)
            })
        },
        listOfPost() {
            console.log(this.$store.state.user_details)
            axios.get(`${filteredResult}/${this.$store.state.user_details.username}`)
            .then(response => {
                console.log(response.data)
                this.forumList = response.data.data
                // this.forumList = response
            })
            .catch(error => {
                console.log(error.message)
            })
        },
        convert_datetime_to_readable(date_time_str) {
            let x = new Date(date_time_str);
            let res = `${x.getDate()} ${x.toLocaleString("default", {
                month: "short",
            })} ${x.getFullYear()} | ${x.toLocaleString("default", {
                timeStyle: "short",
            })}`;

            return res;
        },

        redirect_to_login() {
            //check if user logged in, redirect if not
            if (!this.isAuthenticated) {
                router.push({ path: "/login" });
            }
        },

        clear_form() {
            this.create_post_title = "";
            this.create_post_desc = "";
        },

        submit_new_post() {
            this.loading_post_button = true;
            var vm = this;

            var submit_params = {
                "username": this.$store.state.user_details.username,
                "title": this.create_post_title,
                "description": this.create_post_desc,
                "datetime": (new Date()).toISOString().split(".")[0],
                "is_available": 1
            }

            axios.post("http://127.0.0.1:5103/create_post", submit_params)
            .then(function (response) {
                console.log(response)
                document.getElementById("forum_create_close_btn").click()
                vm.update_posts(true)
                vm.clear_form()
                vm.listOfPost()
                vm.loading_post_button = false
            })
            .catch(function(error) {
                console.log(error)
            })
        },

        update_posts(hard_reload) {
            // hard reload specifies whether to clear entire forum posts while reloading
            if (hard_reload) {
                this.forum_data = [];
                this.loading_posts = true;
            }

            axios
                .get("http://localhost:1115/all")
                .then((response) => {
                    let response_data = response.data.data.forum;

                    // sorts list by datetime (latest first)
                    response_data.sort(function (a, b) {
                        return Date.parse(b.datetime) - Date.parse(a.datetime);
                    });

                    this.forum_data = response_data;
                    this.loading_posts = false;

                    // CREATES OBJECT W [Key:Forum_ID, Value: ""]
                    let temp_comment_input_data = {};
                    for (let e_post of response_data) {
                        temp_comment_input_data[e_post.forum_id] = "";
                    }

                    this.comment_input_data = temp_comment_input_data;

                    if (!hard_reload) {
                        this.sending_comment_id = null;
                    }
                })
                .catch((error) => {
                    console.log(
                        "Error on Forum.vue API call to get all posts: ",
                        error.message
                    );
                });
        },

        submit_new_comment(forumid) {
            var vm = this;
            var comment = this.comment_input_data[forumid];
            var curr_datetime = new Date().toISOString().split(".")[0];
            this.sending_comment_id = forumid;

            // RETURN FALSE IF NO COMMENT
            if (comment.length == 0) {
                this.sending_comment_id = null;
                return false;
            }

            // ELSE SUBMIT COMMENT
            axios.post("http://127.0.0.1:5103/create_comment", {
                "forum_id": forumid,
                "commentor_username": this.$store.state.user_details.username,
                "comment": comment,
                "datetime": curr_datetime
            })
            .then(function (response) {
                console.log(response)

                    vm.update_posts(false);
                    return true;
                })
                .catch(function (error) {
                    console.log(error);

                    vm.sending_comment_id = null;
                    return false;
                });
        },
    },
    computed: {
        isAuthenticated() {
            return this.$store.state.isAuthenticated;
        },
    },
    components: { FontAwesomeIcon },
    created() {
        this.update_posts(true);
        this.listOfPost();
    },
};
</script>

<style scoped>

.deleteBtn:hover {
    color: black;
}

#post-content {
    height: 100px;
}

.fill-space {
    height: 100%;
    position: relative;
}

.post-btn {
    position: absolute;
    bottom: 0;
    right: 0;
    margin: 20px 30px;
    z-index: 2;
}

.forum-body {
    height: 100%;
    overflow-y: scroll;
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
}

.post-user-img {
    flex: 0 1 auto;
    display: flex;
    justify-content: center;
    align-items: center;
    flex-direction: column;
}

.post-title {
    flex: 1 1 auto;
    margin-left: 20px;
}

/* SMALLER THAN 769 */
@media (max-width: 769px) {
    .post-btn {
        border-radius: 50%;
    }

    .post-btn > span {
        display: none;
    }
}

/* LARGER THAN 769 */
@media (min-width: 769px) {
    .card {
        width: 80vw;
    }
}
</style>
