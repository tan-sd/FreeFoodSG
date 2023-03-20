<template>
    <div class="fill-space bg-light">
        <div class="forum-body">
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
        
                    <button class="btn btn-main py-1 px-2" type="button" data-bs-toggle="collapse" :data-bs-target="`#collapse-${e_post.forum_id}`" aria-expanded="false" :aria-controls="`#collapse-${e_post.forum_id}`" :disabled="e_post.comments.length <= 0">
                        <small class="fw-bold"><font-awesome-icon icon="fa-solid fa-comments" /> {{ e_post.comments.length }}</small>
                    </button>
                </div>
                
                <!-- COMMENTS -->
                <div class="collapse" :id="`collapse-${e_post.forum_id}`">
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
                            <button class="btn btn-secondary" type="button" :id="`forum-${e_post.forum_id}-add-comment`">Reply</button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>


<script>
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'

    export default{
    data() {
        return {
            forum_data: [
                {
                    forum_id: 0,
                    username: "adambft",
                    title: "Free Food @ Salesforce Event!",
                    description: "Come down to Saleforce office at 123 Bugis Street 25 to enjoy free drinks and food on 30 Apr 2023 2-4pm!",
                    datetime: "2023-03-12T08:30:00",
                    comments: [
                        { username: "sethyap", description: "Fk you Salesforce sucks", datetime: "2023-03-12T09:12:00" },
                        { username: "angkengboon", description: "No, fk you I love Salesforce. SF is bae <3 uwu", datetime: "2023-03-12T10:20:00" }
                    ]
                },
                {
                    forum_id: 1,
                    username: "rachsng",
                    title: "SMU Open House got Buffet",
                    description: "Come down to SMU at 123 SMU Street 69 to enjoy free drinks and food on 26 Mar 2023 4-10pm!",
                    datetime: "2023-03-01T15:30:00",
                    comments: []
                },
                {
                    forum_id: 2,
                    username: "juns",
                    title: "Free Food @ Ballare Event!",
                    description: "Come down to Ballare office at 123 Ballare Street 25 to enjoy free drinks and food on 1 May 2023 1-2pm!",
                    datetime: "2023-03-04T23:30:00",
                    comments: [
                        { username: "ardiente", description: "Fk you Ballare sucks", datetime: "2023-03-05T09:23:00" },
                        { username: "samba_masala", description: "^ I agree", datetime: "2023-03-05T10:11:00" },
                        { username: "adambft", description: "guys, pls...", datetime: "2023-03-05T10:15:00" }
                    ]
                },
            ]
        };
    },
    methods: {
        convert_datetime_to_readable(date_time_str) {
            let x = new Date(date_time_str);
            let res = `${x.getDate()} ${x.toLocaleString("default", { month: "short" })} ${x.getFullYear()} | ${x.toLocaleString("default", { timeStyle: "short" })}`;

            return res;
        }
    },
    components: { FontAwesomeIcon }
}
</script>


<style scoped>
    .fill-space{
        height: 100%;
        position: relative;
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

    /* @media (max-width: 769px) {
        .card{
            width: 80vw;
        }
    } */

    @media (min-width: 769px) {
        .card{
            width: 80vw;
        }
    }
</style>