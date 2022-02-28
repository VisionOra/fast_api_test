import pytest
from app import schemas

# This test to be able to retrive all posts and see if they are returned in the
# right format
def test_get_all_posts(authorized_client, test_posts):
    res = authorized_client.get("/posts/")

    # Validation Using the Schmas, if we want to actually test the respose
    # we need to work with the List which is the reponse model from the all
    # posts api. Which needs to be unpacked to work
    # List of Dictonaries to a List of Schema Models
    # Really powerful because all the validations are done for us, plus easy to
    # create useful assert statements

    def validate(post):
        return schemas.PostVote(**post)
    posts_map = map(validate, res.json())
    posts_list = (list(posts_map))

    assert len(res.json()) == len(test_posts)
    assert res.status_code == 200

# Test to confirm that an unauthenticated user cannot retrieve all
# posts.

def test_unauthorized_get_all_posts(client, test_posts):
    res = client.get("/posts/")
    assert res.status_code == 401

def test_unauthorized_get_one_post(client, test_posts):
    res = client.get(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401

def test_get_one_post_not_exist(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/{234235}")
    assert res.status_code == 404
def test_get_one_post(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/{test_posts[0].id}")
    post = schemas.PostVote(**res.json())
    assert post.Post.id == test_posts[0].id
    assert post.Post.content == test_posts[0].content
    assert post.Post.title == test_posts[0].title

@pytest.mark.parametrize("title, content, published", [
    ("awesome new title", "awesome new content", True),
    ("favorite pizza", "i love pepperoni", False),
    ("tallest skyscrapers", "wahoo", True),
])
def test_create_post(authorized_client,test_user, test_posts,title, content, published):
    res= authorized_client.post("/posts/", json={"title": title, "content": content, "published": published})

    created_post = schemas.PostResponse(**res.json())
    assert res.status_code == 201
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.published == published
    assert created_post.owner_id == test_user['id']

def test_create_post_default_publish_working(authorized_client,test_user, test_posts):
    res= authorized_client.post("/posts/", json={"title": "testPost", "content": "bull"})

    created_post = schemas.PostResponse(**res.json())
    assert res.status_code == 201
    assert created_post.title == "testPost"
    assert created_post.content == "bull"
    assert created_post.published == True
    assert created_post.owner_id == test_user['id']

def test_unauthorized_user_create_post(client, test_posts):
    res= client.post("/posts/", json={"title": "testPost", "content": "bull"})
    assert res.status_code == 401

def test_unauthorized_user_delete_post(client,test_user, test_posts):
    res= client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401

def test_delete_post_success(authorized_client,test_user, test_posts):
    res= authorized_client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 204

def test_delete_post_non_exist(authorized_client,test_user, test_posts):
    res= authorized_client.delete("/posts/25345245")
    assert res.status_code == 404

def test_delete_other_user_post(authorized_client,test_user, test_posts):
    res= authorized_client.delete(f"/posts/{test_posts[3].id}")
    assert res.status_code == 403

def test_update_post(authorized_client, test_user, test_posts):
    data = {
        "title": "updated title",
        "content": "updatd content",
        "id": test_posts[0].id

    }
    res = authorized_client.put(f"/posts/{test_posts[0].id}", json=data)
    updated_post = schemas.PostResponse(**res.json())
    assert res.status_code == 200
    assert updated_post.title == data['title']
    assert updated_post.content == data['content']

def test_update_other_user_post(authorized_client, test_user, test_posts):
    data = {
        "title": "updated title",
        "content": "updatd content",
        "id": test_posts[3].id

    }
    res = authorized_client.put(f"/posts/{test_posts[3].id}", json=data)
    assert res.status_code == 403

def test_update_unauthenticated_user_post(client, test_user, test_posts):
    res = client.put(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401
def test_update_post_non_exist(authorized_client,test_user, test_posts):
    data = {
        "title": "updated title",
        "content": "updatd content",
        "id": test_posts[3].id
    }
    res= authorized_client.put("/posts/25345245",json=data)
    assert res.status_code == 404