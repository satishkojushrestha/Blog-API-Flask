# Blog API - Flask

# Endpoints

User Authentication
/user/registration [POST]
- Registering user into the system

/login [POST]
- Logging into the system

/logout [GET]
- To logout from the system

Create, Read, Update, and Delete Post/Blog (for admin)
/admin/post [GET]
- Returns all the blogs

/admin/post/create [POST]
- For creating a blog post

/admin/post/update/<int:post_id> [PATCH]
- For updating blog post

/admin/post/delete/<int:post_id> [DELETE]
- For deleting

Read Blog post on homepage
/blog/all [GET]
/blog/<int:post_id> [GET]

Paginated
/blog [GET]
- if nothing is passed the default page for paginated blog would be 1
- it can be useful to see how many pages and items are there....

/blog/paginate/<int:page_number> [GET]
- can be used to directly move to a certain page or after selecting a page number...

# Demonstration on PostMan
## Registering a user
![image](https://user-images.githubusercontent.com/54971497/229271816-0907ad79-dab9-41da-90d9-a1b9e1a2e84e.png)

## Logging in
![image](https://user-images.githubusercontent.com/54971497/229271835-13a09660-1715-4f91-8a6b-4c72937d8e26.png)

## Creating Blog
![image](https://user-images.githubusercontent.com/54971497/229271868-4ff34166-d9ad-4c20-9ba1-54d5d7dce0db.png)

## View blog post (Admin)
![image](https://user-images.githubusercontent.com/54971497/229271983-2795fc1f-e55a-413c-bd35-a318178507cc.png)

## Update blog
![image](https://user-images.githubusercontent.com/54971497/229272009-efe07a23-8017-4dff-abab-b56b5489e9cc.png)

## Delete blog
![image](https://user-images.githubusercontent.com/54971497/229272031-0cc89fc1-6257-4666-8386-8aa0dc36df95.png)

## View blog on homepage
![image](https://user-images.githubusercontent.com/54971497/229272074-45d5b89a-b6e9-4cd2-b092-a60910268909.png)

## View blog on seperate page
![image](https://user-images.githubusercontent.com/54971497/229272125-596168b1-9a8c-4440-af74-768c1d3f2214.png)

## Pagination
![image](https://user-images.githubusercontent.com/54971497/229272224-0de5c29b-1118-435c-9fde-2f4ac9071317.png)

![image](https://user-images.githubusercontent.com/54971497/229272248-86f336c1-c73f-440f-b4a6-d2ac12b452b8.png)

