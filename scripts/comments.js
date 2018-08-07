/*
* Code from: http://donw.io/post/github-comments/
*/

// use of ajax vs getJSON for headers use to get markdown (body vs body_htmml)
// todo: pages, configure issue url, open in new window?

var CurrentPage = 0;
var repo_name = "davamix/davamix.github.io";

function ParseLinkHeader(link) {
    var entries = link.split(",");
    var links = {};
    for (var i in entries) {
        var entry = entries[i];
        var link = {};
        link.name = entry.match(/rel=\"([^\"]*)/)[1];
        link.url = entry.match(/<([^>]*)/)[1];
        link.page = entry.match(/page=(\d+).*$/)[1];
        links[link.name] = link;
    }
    return links;
}

function GetTotalComments(comment_id, page_id){
    if (page_id === undefined)
        page_id = 1;


    var api_url = "https://api.github.com/repos/" + repo_name;
    var api_issue_url = api_url + "/issues/" + comment_id;
    var api_comments_url = api_url + "/issues/" + comment_id + "/comments" + "?page=" + page_id;

    var url = "https://github.com/" + repo_name + "/issues/" + comment_id;

    $(document).ready(function () {
        $.getJSON(api_issue_url, function (data) {
            NbComments = data.comments;
        });

        $.ajax(api_comments_url, {
            headers: { Accept: "application/vnd.github.v3.html+json" },
            dataType: "json",
            success: function (comments, textStatus, jqXHR) {
                var t = comments.length;
                $("#blog-post-date" + comment_id).append("<div>Comments (" + t + ")</div>");
            },error: function () {
                $("#blog-post-date" + comment_id).append("No comment");
            }

            
        });
    });
}

function DoGithubComments(comment_id, page_id) {
    if (page_id === undefined)
        page_id = 1;

    var api_url = "https://api.github.com/repos/" + repo_name;
    var api_issue_url = api_url + "/issues/" + comment_id;
    var api_comments_url = api_url + "/issues/" + comment_id + "/comments" + "?page=" + page_id;

    var url = "https://github.com/" + repo_name + "/issues/" + comment_id;

    $(document).ready(function () {
        $.getJSON(api_issue_url, function (data) {
            NbComments = data.comments;
        });

        $.ajax(api_comments_url, {
            headers: { Accept: "application/vnd.github.v3.html+json" },
            dataType: "json",
            success: function (comments, textStatus, jqXHR) {

                // Add post button to first page
                // if (page_id == 1)
                //     $("#gh-comments-list").append("<a href='" + url + "#new_comment_field' rel='nofollow' class='btn btn-comment float-right'>Post a comment on Github</a>");

                // Individual comments
                $.each(comments, function (i, comment) {

                    var date = new Date(comment.created_at);

                    var t = "<div id='gh-comment' class='comment-box'>";
                    t += "<div class='d-flex align-items-start comment-data-box'>"; // Picture + Username + date 
                    t += "<div class='align-self-center comment-picture'><img src='" + comment.user.avatar_url + "'></div>";
                    t += "<div class='align-self-center comment-user-date'>"; // Username + date
                    t += "<b><a href='" + comment.user.html_url + "' class='comment-username'>" + comment.user.login + "</a></b><br />";
                    // t += " posted at ";
                    t += "<span class='comment-date'>" + date.toUTCString() + "</span>";
                    t += "</div>"; // Username + date
                    t += "</div>"; // Picture + Username + date
                    t += "<div id='gh-comment-hr'></div>";
                    t += "<div class='comment-value'>" + comment.body_html + "</div>";
                    t += "</div>"; // gh-comment
                    $("#gh-comments-list").append(t);
                });

                // Setup comments button if there are more pages to display
                var links = ParseLinkHeader(jqXHR.getResponseHeader("Link"));
                if ("next" in links) {
                    $("#gh-load-comments").attr("onclick", "DoGithubComments(" + comment_id + "," + (page_id + 1) + ");");
                    $("#gh-load-comments").show();
                }
                else {
                    $("#gh-load-comments").hide();
                }
            },
            error: function () {
                $("#gh-comments-list").append("Comments are not open for this post yet.");
            }
        });
    });
}